/*
 * Copyright © 2023 Contrast Security, Inc.
 * See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
 */
/* Python requires its own header to always be included first */
#define PY_SSIZE_T_CLEAN
#include <Python.h>

#ifndef NO_FUNCHOOK
#include <funchook.h>
#endif

#include <contrast/assess/logging.h>
#include <contrast/assess/patches.h>
#include <contrast/assess/propagate.h>

#define apply_or_fail_funchook(applyfunc, funchook)                 \
    do {                                                            \
        if ((applyfunc)((funchook)) != 0) {                         \
            /* Logging and exception is handled inside applyfunc */ \
            teardown_propagate();                                   \
            funchook_destroy((funchook));                           \
            return NULL;                                            \
        }                                                           \
    } while (0);

#define apply_or_fail(applyfunc)                                    \
    do {                                                            \
        if ((applyfunc)() != 0) {                                   \
            /* Logging and exception is handled inside applyfunc */ \
            teardown_propagate();                                   \
            return NULL;                                            \
        }                                                           \
    } while (0);

PyObject *set_attr_on_type(PyObject *self, PyObject *args) {
    PyTypeObject *type = NULL;
    PyObject *name = NULL;
    PyObject *attr = NULL;

    if (!PyArg_ParseTuple(args, "OOO", (PyObject **)&type, &name, &attr)) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to parse arguments");
        return NULL;
    }

    if (!PyType_Check(type)) {
        PyErr_SetString(PyExc_TypeError, "First argument must be a type");
        return NULL;
    }

    if (PyDict_SetItem(type->tp_dict, name, attr) != 0)
        return NULL;

    PyType_Modified(type);

    Py_RETURN_NONE;
}

PyObject *has_funchook(PyObject *self, PyObject *arg) {
#ifdef NO_FUNCHOOK
    Py_RETURN_FALSE;
#else
    Py_RETURN_TRUE;
#endif
}

PyObject *initialize(PyObject *unused, PyObject *unused2) {
    log_debug("BUILD DATETIME %s ", EXTENSION_BUILD_TIME);

    if (init_propagate() != 0) {
        /* Logging and exception occur inside init_propagate */
        return NULL;
    }

    log_debug("initialized propagation");

#ifdef NO_FUNCHOOK
    Py_RETURN_NONE;
#else
    funchook_t *funchook = NULL;

    if ((funchook = funchook_create()) == NULL) {
        log_exception(PyExc_RuntimeError, "failed to create funchook object");
        return NULL;
    }

    return PyCapsule_New((void *)funchook, NULL, NULL);
#endif
}

PyObject *enable_required_hooks(PyObject *self, PyObject *arg) {
#ifndef NO_FUNCHOOK
    funchook_t *funchook = NULL;

    UNPACK_FUNCHOOK_CAPSULE;

    apply_or_fail_funchook(apply_cat_patch, funchook);
    apply_or_fail_funchook(apply_format_patch, funchook);
    apply_or_fail_funchook(apply_cast_patches, funchook);
#else
    apply_format_patch();
    apply_cast_patches();
#endif

    apply_repeat_patch();
    apply_or_fail(apply_stream_patches);
    apply_subscript_patch();
    apply_repr_patches();

    Py_RETURN_NONE;
}

PyObject *install(PyObject *self, PyObject *arg) {
#ifndef NO_FUNCHOOK
    funchook_t *funchook = NULL;

    UNPACK_FUNCHOOK_CAPSULE;

    if (funchook_install(funchook, 0) != FUNCHOOK_ERROR_SUCCESS) {
        log_exception(
            PyExc_RuntimeError,
            "failed to install assess patches: %s",
            funchook_error_message(funchook));
        funchook_destroy(funchook);
        return NULL;
    }

    log_debug("installed assess patches");
#endif

    Py_RETURN_NONE;
}

PyObject *disable(PyObject *self, PyObject *arg) {
    reverse_repr_patches();
    reverse_subscript_patch();
    reverse_stream_patches();
    reverse_repeat_patch();
    reverse_format_patch();
#ifdef NO_FUNCHOOK
    reverse_cast_patches();
#endif

#ifndef NO_FUNCHOOK
    funchook_t *funchook = NULL;

    UNPACK_FUNCHOOK_CAPSULE;

    if (funchook_uninstall(funchook, 0) != FUNCHOOK_ERROR_SUCCESS) {
        log_exception(
            PyExc_RuntimeError,
            "Error uninstalling assess patches: %s",
            funchook_error_message(funchook));
        funchook_destroy(funchook);
        return NULL;
    }

    funchook_destroy(funchook);
#endif

    log_debug("uninstalled assess patches");

    teardown_propagate();

    log_debug("disabled propagation");

    teardown_logger();

    Py_RETURN_NONE;
}
