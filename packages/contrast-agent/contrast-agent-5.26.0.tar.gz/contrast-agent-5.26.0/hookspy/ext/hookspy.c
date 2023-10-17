/*
 * Copyright © 2023 Contrast Security, Inc.
 * See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
 */
/* Python requires its own header to always be included first */
#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <string.h>

#if PY_MAJOR_VERSION < 3 || PY_MINOR_VERSION < 6
#define NO_FASTCALL
#endif

#if PY_MAJOR_VERSION < 3
#define STRING_CHECK(X) PyString_Check(X)
#define COMPARE_NAME(X, Y) strcmp(PyString_AsString(X), Y)
#else
#define STRING_CHECK(X) PyUnicode_Check(X)
#define COMPARE_NAME(X, Y) PyUnicode_CompareWithASCIIString(X, Y)
#endif

static PyObject *find_method_body(PyTypeObject *type, PyObject *args) {
    PyObject *name;
    PyMethodDef *method;

    if (!PyArg_ParseTuple(args, "O", &name))
        return NULL;

    if (!STRING_CHECK(name)) {
        PyErr_SetString(PyExc_TypeError, "string argument expected");
        return NULL;
    }

    for (int i = 0;; i++) {
        method = &(type->tp_methods[i]);
        if (method->ml_name == NULL)
            break;

        if (COMPARE_NAME(name, method->ml_name) != 0)
            continue;

        /* We found a matching name */
        return Py_BuildValue("ii", i, method->ml_flags);
    }

    Py_RETURN_NONE;
}

static PyObject *find_unicode_hook(PyObject *self, PyObject *args) {
    return find_method_body(&PyUnicode_Type, args);
}

static PyObject *find_bytes_hook(PyObject *self, PyObject *args) {
    return find_method_body(&PyBytes_Type, args);
}

static PyObject *find_bytearray_hook(PyObject *self, PyObject *args) {
    return find_method_body(&PyByteArray_Type, args);
}

static PyObject *get_type_method_body(
    const char *modulename, const char *typename, PyObject *args) {
    PyObject *module = NULL;
    PyTypeObject *type = NULL;
    PyObject *result = NULL;

    if ((module = PyImport_ImportModule(modulename)) == NULL)
        goto cleanup_and_exit;

    if ((type = (PyTypeObject *)PyObject_GetAttrString(module, typename)) == NULL)
        goto cleanup_and_exit;

    result = find_method_body(type, args);

cleanup_and_exit:
    Py_XDECREF(module);
    Py_XDECREF(type);
    return result;
}

static PyObject *find_stringio_hook(PyObject *self, PyObject *args) {
    return get_type_method_body("io", "StringIO", args);
}

static PyObject *find_bytesio_hook(PyObject *self, PyObject *args) {
    return get_type_method_body("io", "BytesIO", args);
}

static PyObject *find_iobase_hook(PyObject *self, PyObject *args) {
    return get_type_method_body("_io", "_IOBase", args);
}

static void add_int_constants(PyObject *module) {
    PyModule_AddIntConstant(module, "METH_O", METH_O);
    PyModule_AddIntConstant(module, "METH_NOARGS", METH_NOARGS);
    PyModule_AddIntConstant(module, "METH_VARARGS", METH_VARARGS);
    PyModule_AddIntConstant(module, "METH_KEYWORDS", METH_KEYWORDS);
    /* these are special cases to handle "methods" that don't belong in tp_dict,
       such as __init__ - hopefully we don't reach enough special cases to run
       out of digits */
    PyModule_AddIntConstant(module, "METH_NEW", 1 << 19);
    PyModule_AddIntConstant(module, "METH_INIT", 1 << 18);
#ifdef NO_FASTCALL
    /* Dummy value */
    PyModule_AddIntConstant(module, "METH_FASTCALL", 1 << 20);
#else
    PyModule_AddIntConstant(module, "METH_FASTCALL", METH_FASTCALL);
#endif
}

static PyMethodDef methods[] = {
    {"find_bytes_hook", find_bytes_hook, METH_VARARGS, "find bytes hook"},
    {"find_unicode_hook", find_unicode_hook, METH_VARARGS, "find unicode hook"},
    {"find_bytearray_hook", find_bytearray_hook, METH_VARARGS, "find bytearray hook"},
    {"find_stringio_hook", find_stringio_hook, METH_VARARGS, "find stringio hook"},
    {"find_bytesio_hook", find_bytesio_hook, METH_VARARGS, "find bytesio hook"},
    {"find_iobase_hook", find_iobase_hook, METH_VARARGS, "find iobase hook"},
    {NULL, NULL, 0, NULL}};

#if PY_MAJOR_VERSION < 3
PyMODINIT_FUNC inithookspy(void) {
    PyObject *module = Py_InitModule("hookspy", methods);
    add_int_constants(module);
}

#else
static struct PyModuleDef hookspy_definition = {
    PyModuleDef_HEAD_INIT,
    "hookspy",
    "find method hooks for python string objects",
    -1,
    methods,
    NULL,
    NULL,
    NULL,
    NULL};

PyMODINIT_FUNC PyInit_hookspy(void) {
    PyObject *module;

    Py_Initialize();

    module = PyModule_Create(&hookspy_definition);
    add_int_constants(module);

    return module;
}
#endif /* PY_MAJOR_VERSION < 3 */
