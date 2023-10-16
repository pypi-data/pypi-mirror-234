#include <Python.h>

static PyObject *StringTooShortError = NULL;

static PyObject *method_fprintf(PyObject *self, PyObject *args) {
    char *str, *filename = NULL;
    int bytes_copied = -1;

    /* Parse arguments */
    if(!PyArg_ParseTuple(args, "ss", &str, &filename)) {
        return NULL;
    }

    /* Get length of input string */
    Py_ssize_t str_len = PyUnicode_GET_LENGTH((PyObject*)str);

    if (str_len < 0) {
        /* Passing custom exception */
        PyErr_SetString(StringTooShortError, "String param must be exists");
        return NULL;
    }

    FILE *fp = fopen(filename, "w");
    if (fp == NULL) {
        /* Handle file opening error */
        PyErr_SetString(PyExc_IOError, "Unable to open file");
        return NULL;
    }

    bytes_copied = fprintf(fp, "%s", str);
    fclose(fp);

    if (bytes_copied < 0) {
        /* Handle fprintf error */
        PyErr_SetString(PyExc_IOError, "Unable to write to file");
        return NULL;
    }

    return PyLong_FromLong(bytes_copied);
}

static PyMethodDef FprintfMethods[] = {
    {"fprintf", method_fprintf, METH_VARARGS, "Python interface for fprintf C library function"},
    {NULL, NULL, 0, NULL}
};


static struct PyModuleDef fprintf_module = {
    PyModuleDef_HEAD_INIT,
    "fprintf",
    "Python interface for the fprintf C library function",
    -1,
    FprintfMethods
};

PyMODINIT_FUNC PyInit_fprintf(void) {

    /* Assign module value */
    PyObject *module = PyModule_Create(&fprintf_module);

    /* Initialize new exception object */
    StringTooShortError = PyErr_NewException("fprintf.StringTooShortError", NULL, NULL);

    /* Add exception object to your module */
    PyModule_AddObject(module, "StringTooShortError", StringTooShortError);

    return module;
}

