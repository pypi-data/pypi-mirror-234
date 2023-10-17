/*
 * Copyright © 2023 Contrast Security, Inc.
 * See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
 */
#ifndef _ASSESS_PATCHES_H_
#define _ASSESS_PATCHES_H_
/* Python requires its own header to always be included first */
#define PY_SSIZE_T_CLEAN
#include <Python.h>

//#include <funchook.h>
#ifdef NO_FUNCHOOK
typedef void funchook_t;
#else
#include <funchook.h>
#endif /* NO_FUNCHOOK */

#define UNPACK_FUNCHOOK_CAPSULE                                                   \
    do {                                                                          \
        if (!PyCapsule_IsValid(arg, NULL)) {                                      \
            log_exception(PyExc_TypeError, "Expected funchook container");        \
            return NULL;                                                          \
        }                                                                         \
                                                                                  \
        if ((funchook = (funchook_t *)PyCapsule_GetPointer(arg, NULL)) == NULL) { \
            log_exception(                                                        \
                PyExc_RuntimeError, "Failed to get funchook from container");     \
            return NULL;                                                          \
        }                                                                         \
    } while (0);

PyObject *initialize(PyObject *, PyObject *);
PyObject *enable_required_hooks(PyObject *self, PyObject *arg);
PyObject *install(PyObject *self, PyObject *arg);
PyObject *has_funchook(PyObject *self, PyObject *arg);
PyObject *disable(PyObject *self, PyObject *args);
PyObject *set_attr_on_type(PyObject *self, PyObject *args);
PyObject *create_unicode_hook_module(PyObject *self, PyObject *args);
PyObject *create_bytes_hook_module(PyObject *self, PyObject *args);
PyObject *create_bytearray_hook_module(PyObject *self, PyObject *args);

int apply_cat_patch(funchook_t *funchook);
void apply_repeat_patch();
void apply_subscript_patch();
#ifdef NO_FUNCHOOK
void apply_format_patch();
void apply_cast_patches();
#else
int apply_format_patch(funchook_t *funchook);
int apply_cast_patches(funchook_t *funchook);
#endif
int apply_stream_patches();
void apply_repr_patches();
#if PY_MAJOR_VERSION < 3
int apply_exec_patches(funchook_t *funchook);
#endif
int patch_stringio_methods(PyTypeObject *StreamType);
int patch_bytesio_methods(PyTypeObject *StreamType);
int patch_iobase_methods(PyTypeObject *StreamType);

void reverse_format_patch();
void reverse_repeat_patch();
void reverse_subscript_patch();
void reverse_stream_patches();
void reverse_repr_patches();
#ifdef NO_FUNCHOOK
void reverse_cast_patches();
#endif

void reverse_stringio_methods(PyTypeObject *StreamType);
void reverse_bytesio_methods(PyTypeObject *StreamType);
void reverse_iobase_methods(PyTypeObject *StreamType);

#endif /* _ASSESS_PATCHES_H_ */
