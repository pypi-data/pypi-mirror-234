from sys import version_info

from . import hookspy


py_version = version_info[:2]


fastcall_name = "fastcall_func"
fastcall_typedef = (
    "typedef PyObject *(*{})(PyObject *, PyObject *const *, Py_ssize_t)".format(
        fastcall_name
    )
)

fastcall_kwargs_name = "fastcall_kwargs_func"
fastcall_kwargs_typedef = "typedef PyObject *(*{})(PyObject *, PyObject *const *, Py_ssize_t, PyObject *)".format(
    fastcall_kwargs_name
)


unaryfunc_signature = "PyObject *{}(PyObject *self)"
binaryfunc_signature = "PyObject *{}(PyObject *self, PyObject *args)"
ternaryfunc_signature = "PyObject *{}(PyObject *self, PyObject *args, PyObject *kwargs)"
fastcall_signature = (
    "PyObject *{}(PyObject *self, PyObject *const *args, Py_ssize_t nargs)"
)
fastcall_kwargs_signature = "PyObject *{}(PyObject *self, PyObject *const *args, Py_ssize_t nargs, PyObject *kwnames)"

newfunc_signature = "PyObject *{}(PyTypeObject *type, PyObject *args, PyObject *kwds)"
initproc_signature = "int {}(PyObject *self, PyObject *args, PyObject *kwds)"

unaryfunc_call = "(self)"
binaryfunc_call = "(self, args)"
ternaryfunc_call = "(self, args, kwargs)"
fastcall_call = "(self, args, nargs)"
fastcall_kwargs_call = "(self, args, nargs, kwargs)"
newfunc_call = "(type, args, kwds)"
initproc_call = "(self, args, kwds)"


signatures_by_name = {
    "unaryfunc": unaryfunc_signature,
    "binaryfunc": binaryfunc_signature,
    "ternaryfunc": ternaryfunc_signature,
    fastcall_name: fastcall_signature,
    fastcall_kwargs_name: fastcall_kwargs_signature,
    "newfunc": newfunc_signature,
    "initproc": initproc_signature,
}


calls_by_name = {
    "unaryfunc": unaryfunc_call,
    "binaryfunc": binaryfunc_call,
    "ternaryfunc": ternaryfunc_call,
    fastcall_name: fastcall_call,
    fastcall_kwargs_name: fastcall_kwargs_call,
    "newfunc": newfunc_call,
    "initproc": initproc_call,
}


propagate_args_by_name = {
    "unaryfunc": "NULL, NULL",
    "binaryfunc": "args, NULL",
    "ternaryfunc": "args, kwargs",
}


method_signatures_map = {
    hookspy.METH_O: "binaryfunc",
    hookspy.METH_NOARGS: "unaryfunc",
    hookspy.METH_VARARGS: "binaryfunc",
    hookspy.METH_KEYWORDS: "ternaryfunc",
    hookspy.METH_FASTCALL: fastcall_name,
    hookspy.METH_VARARGS | hookspy.METH_KEYWORDS: "ternaryfunc",
    hookspy.METH_FASTCALL | hookspy.METH_KEYWORDS: fastcall_kwargs_name,
    # special cases:
    hookspy.METH_NEW: "newfunc",
    hookspy.METH_INIT: "initproc",
}


def is_buggy_method(strtype, name):
    if strtype not in ["bytes", "bytearray"] or py_version != (3, 6):
        return False
    return name in ["decode", "split", "rsplit", "splitlines", "translate"]


def get_method_signature(strtype, name, argtype):
    # There is a bug in 3.6 that requires this special handling logic
    if is_buggy_method(strtype, name):
        return fastcall_kwargs_name
    return method_signatures_map[argtype]
