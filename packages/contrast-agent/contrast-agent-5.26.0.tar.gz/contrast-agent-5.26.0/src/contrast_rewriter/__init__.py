# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
"""
Implements AST rewriter for Contrast Agent
"""
import importlib.abc
import importlib.machinery
import importlib.util
import sys
import ast
import copy
import operator
import os

# Seems like it is necessary to import this prior to rewriting to avoid some weird partial import state
import tokenize  # pylint: disable=unused-import

from contrast_vendor.wrapt.importer import _ImportHookChainedLoader

# NOTE: It is extremely important to limit the number of imports used by this
# module. It should be restricted to only those imports that are absolutely
# necessary for the operation of the rewriter, and ideally should include only
# built-in or standard library modules that are already imported by the
# interpreter prior to the evaluation of this module. It is *very* important
# that this module does *not* import the core `contrast` package since that
# would introduce a huge number of dependencies that we do not want.
# By limiting the number of dependencies for the rewriter module, we can ensure
# that a minimal number of modules are already imported prior to the
# application of the rewriter, which means we maximize the coverage of our
# rewriter in application and library code.

ENABLE_REWRITER: str = "__CONTRAST_APPLY_REWRITER"
REWRITE_FOR_PYTEST: str = "__CONTRAST_REWRITE_FOR_PYTEST"

_CONTRAST_MODULES = ["contrast", "contrast_vendor", "contrast_rewriter"]
_CONTRAST_OPERATOR_NAME: str = "contrast__operator"


class _ContrastImportHookChainedLoader(_ImportHookChainedLoader):
    def __init__(self, loader) -> None:
        super().__init__(loader)

        if hasattr(loader, "get_code"):
            self.get_code = self.loader.get_code


class DeferredLogger:
    def __init__(self):
        self.messages = []

    def debug(self, message, *args, **kwargs):
        self.messages.append(("debug", message, args, kwargs))


# Can't use our Namespace here since we don't want to import contrast package yet
class rewriter_module:
    logger = DeferredLogger()
    enabled: bool = False
    registry = set()


def _load_module(source, module, filename):
    """
    Convenience method to compile and execute the given module source

    It seems like we do not need any exception handling here since any
    exception that occurs gets handled further up by the import machinery and
    causes it to fall back on the original loader. This is definitely good for
    us since it means that even if we mess up here somehow, it shouldn't
    prevent the original module from being loaded. It will just be loaded
    without our rewrites.
    """
    code = compile(source, filename, "exec", dont_inherit=True)
    exec(code, module.__dict__)


def populate_operator_module(obj):
    obj.setdefault(_CONTRAST_OPERATOR_NAME, operator)


def _is_contrast_module_name(fullname: str) -> bool:
    fullname_split = fullname.split(".")
    if len(fullname_split) == 0:
        return False
    top_level_name = fullname_split[0]
    return top_level_name in _CONTRAST_MODULES


class ContrastMetaPathFinder(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        """
        The finder is in charge of finding a module's "spec". The spec includes import
        machinery metadata about the module - including its name, source file path, and
        the loader, among others.

        Here, we first use importlib's default machinery to get the spec for the module
        about to be imported. The problem with this spec is that it also uses the
        default loader, which isn't what we want. To get around this, we reuse some
        metadata and generate a new spec that points at our loader.
        """
        if _is_contrast_module_name(fullname):
            return None

        spec = importlib.machinery.PathFinder.find_spec(fullname, path)

        if (
            spec is None
            or spec.origin is None
            or not isinstance(spec.loader, importlib.machinery.SourceFileLoader)
        ):
            rewriter_module.logger.debug(
                "Skipping non-source module - fullname=%s, path=%s",
                fullname,
                getattr(spec, "origin", "<unknown>"),
            )
            return None

        new_spec = importlib.util.spec_from_file_location(
            fullname,
            spec.origin,
            loader=ContrastRewriteLoader(fullname, spec.origin),
            submodule_search_locations=spec.submodule_search_locations,
        )
        if new_spec is None:
            return new_spec

        loader = getattr(new_spec, "loader", None)

        if loader and not isinstance(loader, _ContrastImportHookChainedLoader):
            new_spec.loader = _ContrastImportHookChainedLoader(loader)

        rewriter_module.logger.debug(
            "Updated spec for module: fullname=%s, path=%s",
            fullname,
            spec.origin,
        )
        return new_spec


class ContrastRewriteLoader(importlib.machinery.SourceFileLoader):
    def exec_module(self, module) -> None:
        """
        This method is responsible for actually doing the module `exec`-ing. We take
        control of this system and do the following:
        - read the original source file. We require pyc caching to be disabled for this
        - parse the source file into an AST
        - rewrite the AST
        - compile the AST into a code object
        - exec the code object

        Note that we add our custom add function to the module's globals. This prevents
        the need for import rewriting entirely
        """
        original_source_code = None
        filename = self.path

        # May be None in some cases such as for namespace packages
        if filename is None:
            return

        try:
            original_source_code = self.get_source(self.name)
            tree = ast.parse(original_source_code)
        except Exception as ex:
            rewriter_module.logger.debug(
                "WARNING: failed to rewrite %s", filename, exc_info=ex
            )

            _load_module(original_source_code, module, filename)

            return

        if _CONTRAST_OPERATOR_NAME not in module.__dict__:
            try:
                populate_operator_module(module.__dict__)
                PropagationRewriter().visit(tree)
                ast.fix_missing_locations(tree)
            except Exception as ex:
                rewriter_module.logger.debug(
                    "WARNING: failed to rewrite %s", filename, exc_info=ex
                )
        else:
            rewriter_module.logger.debug(
                "WARNING: module %s appears to have been already rewritten; will not rewrite again",
                filename,
            )

        rewriter_module.registry.add(self.name)

        _load_module(tree, module, filename)


class PropagationRewriter(ast.NodeTransformer):
    def _copy_with_context(self, node, context):
        node = copy.copy(node)
        node.ctx = context
        return node

    def _make_attr(self, op):
        return ast.Attribute(
            value=ast.Name(id=_CONTRAST_OPERATOR_NAME, ctx=ast.Load()),
            attr=op.__name__,
            ctx=ast.Load(),
        )

    def visit_BinOp(self, binop: ast.BinOp):
        """
        If we see an "Add" or a "Mod" binary operation, replace it with a call to our custom add/modulo
        function, which includes all necessary instrumentation.
        """
        binop.left = self.visit(binop.left)
        binop.right = self.visit(binop.right)

        if isinstance(binop.op, ast.Mod):
            binop_replacement = ast.Call(
                func=self._make_attr(operator.mod),
                args=[binop.left, binop.right],
                keywords=[],
            )

            ast.copy_location(binop_replacement, binop)
            return binop_replacement

        if not isinstance(binop.op, ast.Add):
            return binop

        binop_replacement = ast.Call(
            func=self._make_attr(operator.add),
            args=[binop.left, binop.right],
            keywords=[],
        )
        ast.copy_location(binop_replacement, binop)
        return binop_replacement

    def visit_AugAssign(self, node: ast.AugAssign):
        """
        If we see an "Append", `+=` operation, rewrite it as a `+`.
        """
        node.value = self.visit(node.value)

        if not isinstance(node.op, ast.Add):
            return node

        target = left = None
        if isinstance(node.target, ast.Name):
            name = ast.Name(id=node.target.id)
            target = self._copy_with_context(name, ast.Store())
            left = self._copy_with_context(name, ast.Load())
        else:
            target = node.target
            left = self._copy_with_context(target, ast.Load())

        call_contrast_append_node = ast.Assign(
            targets=[target],
            value=ast.Call(
                func=self._make_attr(operator.iadd),
                args=[self.visit(left), node.value],
                keywords=[],
            ),
        )

        ast.copy_location(call_contrast_append_node, node)
        # Recurse here in order to properly rewrite the `+` operation
        return call_contrast_append_node

    def visit_JoinedStr(self, node: ast.JoinedStr):
        return ast.Call(
            func=ast.Attribute(value=ast.Constant(""), attr="join", ctx=ast.Load()),
            args=[ast.List(elts=node.values, ctx=ast.Load())],
            keywords=[],
        )


def _non_contrast_module_filter(module_item) -> bool:
    return not _is_contrast_module_name(
        getattr(module_item[1], "__package__", "") or ""
    )


def _log_imported_modules() -> None:
    module_map = {
        importlib.machinery.BuiltinImporter: "builtin",
        importlib.machinery.FrozenImporter: "frozen",
    }

    all_modules = list(filter(_non_contrast_module_filter, sys.modules.items()))

    rewriter_module.logger.debug(
        "the following %d modules are already imported", len(all_modules)
    )
    for name, module in sorted(all_modules):
        module_type = module_map.get(getattr(module, "__loader__", None), "source")
        rewriter_module.logger.debug("%-20s type=%s", name, module_type)


def _find_pytest_rewriter_index() -> int:
    """
    Find the index of the pytest assertion rewriter

    When we run with Pytest, we want to insert our rewriter *after* the assertion rewriter
    """
    from _pytest.assertion.rewrite import AssertionRewritingHook

    for i, finder in enumerate(sys.meta_path):
        if isinstance(finder, AssertionRewritingHook):
            return i

    # Caller will increment with +1, so just return -1
    return -1


def _hook_assertion_rewrites(rewrite_module):
    from contrast_vendor.wrapt import function_wrapper

    # This hook enables us to apply our rewriter before assertion rewrites are applied
    def rewrite_asserts(wrapped, _, args, kwargs):
        mod = args[0]
        PropagationRewriter().visit(mod)
        ast.fix_missing_locations(mod)
        wrapped(*args, **kwargs)

    # This hook ensures that we add our contrast-specfic functions to the rewritten module
    def exec_module(wrapped, _, args, kwargs):
        module = args[0]
        populate_operator_module(module.__dict__)
        wrapped(*args, **kwargs)

    rewrite_module.rewrite_asserts = function_wrapper(rewrite_asserts)(
        rewrite_module.rewrite_asserts
    )
    rewrite_module.AssertionRewritingHook.exec_module = function_wrapper(exec_module)(
        rewrite_module.AssertionRewritingHook.exec_module
    )


def register_assertion_rewrite_hooks():
    """
    Register hooks for pytest's assertion rewriter

    This is only to be used for internal testing purposes. It enables our
    rewrites to be compatible with pytest's assertion rewrites.
    """
    from contrast_vendor.wrapt import register_post_import_hook

    register_post_import_hook(_hook_assertion_rewrites, "_pytest.assertion.rewrite")


def register(override_config=False, with_pytest=False):
    """
    Register our rewriter with the import system. After this call, any newly imported
    modules (from source code) will use our custom rewriter.

    Note that because this function is defined in the same module that defines our add
    replacement function, we never have to worry about rewriting the addition in the
    replacement function itself. If that were to occur, we would get an infinite
    recursion.

    Rewriter should only run in >=py3.10 and only in environments in which our default
    patching mechanism does not work.

    :param override_config: Force the rewriter to be registered regardless of configuration (for testing purposes)
    :param with_pytest: Indicates whether rewriter is being used in a pytest context (for internal use)
    """
    if not (override_config or os.environ.get(ENABLE_REWRITER) or rewrite_for_pytest()):
        rewriter_module.logger.debug("Rewriter not enabled, exiting")
        return

    if is_rewriter_enabled():
        rewriter_module.logger.debug("Rewriter already enabled, not applying again")
        return

    _log_imported_modules()

    # When we're running our own tests with pytest, we want our rewriter to be
    # inserted *after* pytest's assertion rewriting hook. This means that
    # pytest gets to rewrite assertions for any test modules, and we get to
    # rewrite any other non-test modules that are loaded (since the pytest
    # rewriting hook will defer to the next loader in those cases). We also
    # hook pytest's assertion rewriter so that we can apply our own rewriter to
    # test modules too.
    insert_idx = _find_pytest_rewriter_index() + 1 if with_pytest else 0

    sys.meta_path.insert(insert_idx, ContrastMetaPathFinder())

    rewriter_module.logger.debug("enabled AST rewriter")

    rewriter_module.enabled = True


def deregister():
    """
    Remove our rewriter from the import system. Modules that were loaded by our rewriter
    will remain rewritten.

    Return True if we find and deregister our machinery, False otherwise.
    """
    for i, finder in enumerate(sys.meta_path.copy()):
        if isinstance(finder, ContrastMetaPathFinder):
            sys.meta_path.pop(i)
            rewriter_module.enabled = False
            return True
    return False


def process_rewriter_logs(real_logger):
    if not isinstance(rewriter_module.logger, DeferredLogger):
        real_logger.debug("WARNING: cannot process deferred rewriter logs")
        return

    for level, message, args, kwargs in rewriter_module.logger.messages:
        getattr(real_logger, level)(message, *args, **kwargs)

    rewriter_module.logger.messages.clear()


def set_rewriter_logger(logger):
    rewriter_module.logger = logger


def is_rewriter_enabled() -> bool:
    return rewriter_module.enabled


def rewrite_for_pytest() -> bool:
    return REWRITE_FOR_PYTEST in os.environ


def module_was_rewritten(name: str) -> bool:
    return name in rewriter_module.registry
