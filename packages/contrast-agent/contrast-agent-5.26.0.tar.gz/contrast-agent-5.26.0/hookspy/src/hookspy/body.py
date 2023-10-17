from .signatures import (
    fastcall_name,
    fastcall_kwargs_name,
    calls_by_name,
    propagate_args_by_name,
    signatures_by_name,
)


hook_template = """{} {{{}
}}
"""


replace_hook_body_fastcall = """
    /* In Py37 the replace method type moved to METH_FASTARGS. This means that
     * instead of args being passed as a tuple, they are passed as a C array
     * that contains PyObjects. We need to check whether there is the number of
     * args that we expect, and whether the arg we care about is not NULL.
     * Specifically, we want args[1] since it represents the "new" string in
     * the replacement.
     */
    PyObject *hook_args = pack_args_tuple(args, nargs);
    PyObject *result = {orig_func}{call};

    if (result == NULL || nargs < 2 || args[1] == NULL)
        goto cleanup_and_exit;

    if (result == self)
        goto cleanup_and_exit;

    call_string_propagator("propagate_{hook_name}", self, result, hook_args, NULL);

cleanup_and_exit:
    Py_XDECREF(hook_args);
    return result;
"""


split_hook_body_fastcall = """
    PyObject *result = {orig_func}(self, args, nargs, kwnames);
    PyObject *args_tuple = pack_args_tuple(args, nargs);
    PyObject *kwargs = pack_kwargs_dict(args, nargs, kwnames);

    if (result == NULL || PySequence_Length(result) == 1)
        goto cleanup_and_exit;

    call_string_propagator("propagate_{hook_name}", (PyObject *)self, result, args_tuple, kwargs);

cleanup_and_exit:
    Py_XDECREF(args_tuple);
    Py_XDECREF(kwargs);
    return result;
"""


join_hook_body = """
    PyObject *list = PySequence_List(args);

    /* Converting args to a list might legitimately raise an exception in some cases.
     * We need to be sure we don't suppress that exception to maintain original app
     * behavior. We've seen this before when args is a generator.
     */
    if (list == NULL) {{
        return NULL;
    }}

    /* In Py36+ we also hook an internal function that is called by this
     * function in order to propagate fstring formatting. We still want to have
     * a separate hook for join so that the events are reported differently.
     * This means that we need to go into scope when calling the original
     * function here so that we don't propagate twice.
     */
    enter_propagation_scope();
    PyObject *result = {orig_func}((PyObject *)self, list);
    exit_propagation_scope();

    PyObject *prop_args = PyTuple_Pack(1, list);

    if (prop_args == NULL || result == NULL)
        goto cleanup_and_exit;

    call_string_propagator("propagate_{hook_name}", (PyObject *)self, result, prop_args, NULL);

cleanup_and_exit:
    Py_XDECREF(list);
    Py_XDECREF(prop_args);
    return result;
"""


formatmap_hook_body = """
    PyObject *result = {orig_func}{call};

    if (result == NULL)
        return result;

    call_string_propagator("propagate_{hook_name}", self, result, NULL, args);

    return result;
"""


new_hook_body = """
    PyObject *result = {orig_func}{call};

    if (result == NULL)
        return result;

    call_string_propagator("propagate_{hook_name}", NULL, result, args, kwds);

    return result;
"""


init_hook_body = """
    int result = {orig_func}{call};

    if (result == -1)
        return result;

    /* Here we report self_obj=None and ret=self
       to maintain the illusion of casting */
    call_string_propagator("propagate_{hook_name}", NULL, self, args, kwds);

    return result;
"""


hook_macro_by_signature = {
    "unaryfunc": "HOOK_{}UNARYFUNC",
    "binaryfunc": "HOOK_{}BINARYFUNC",
    "ternaryfunc": "HOOK_{}TERNARYFUNC",
    fastcall_name: "HOOK_{}FASTCALL",
    fastcall_kwargs_name: "HOOK_TERNARY_FASTCALL",
}


special_methods = {
    "replace": (None, replace_hook_body_fastcall),
    "split": (None, split_hook_body_fastcall),
    "rsplit": (None, split_hook_body_fastcall),
    "join": (join_hook_body,) * 2,
    "formatmap": (formatmap_hook_body,) * 2,
    "new": (new_hook_body,) * 2,
    "init": (init_hook_body,) * 2,
}


def build_str_hook_macro(hook_name, signature):
    hook_definition = hook_macro_by_signature[signature]
    hook_definition = hook_definition.format("")
    hook_definition += "({});"
    return hook_definition.format(hook_name)


def build_stream_hook_macro(name, hook_name, signature):
    hook_definition = hook_macro_by_signature[signature]
    hook_definition = hook_definition.format("STREAM_")
    hook_definition += '({}, "{}");'
    return hook_definition.format(hook_name, name)


def build_special_hook(name, hook_name, signature):
    idx = 1 if signature in [fastcall_name, fastcall_kwargs_name] else 0

    hook_body = special_methods[name][idx]
    if hook_body is None:
        return build_str_hook_macro(hook_name, signature)

    hook_body = hook_body.format(
        orig_func="{}_orig".format(hook_name),
        hook_name=hook_name,
        call=calls_by_name[signature],
    )
    hook_funcname = "{}_new".format(hook_name)
    hook_signature = signatures_by_name[signature].format(hook_funcname)
    return hook_template.format(hook_signature, hook_body)


def create_hook(strtype, name, signature, stream_type):
    hook_name = "{}_{}".format(strtype, name)
    if name in special_methods:
        hook_definition = build_special_hook(name, hook_name, signature)
    elif stream_type:
        hook_definition = build_stream_hook_macro(name, hook_name, signature)
    else:
        hook_definition = build_str_hook_macro(hook_name, signature)

    return hook_definition, hook_name
