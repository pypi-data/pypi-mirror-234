#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION

#include <Python.h>
#include <math.h>

#include <stdlib.h>
#include <stdbool.h>

static PyObject* pdf(PyObject*, PyObject*);
static PyObject* cdf(PyObject*, PyObject*);
static PyObject* invcdf(PyObject*, PyObject*);

#ifndef NORMIE_PI
#    define NORMIE_PI 3.14159265358979323846
#endif


static PyObject* pdf(PyObject* self, PyObject* args)
{
    float x;

    /*  Parse single numpy array argument */
    if (!PyArg_ParseTuple(args, "f", &x)) return NULL;

    float z = exp(-x * x / 2.0) / sqrt(2 * NORMIE_PI);
    return Py_BuildValue("f", z);
}


static PyObject* cdf(PyObject* self, PyObject* args)
{
    float x;

    /*  Parse single numpy array argument */
    if (!PyArg_ParseTuple(args, "f", &x)) return NULL;

    float z = erfc(-x / sqrt(2.0)) / 2.0;
    return Py_BuildValue("f", z);
}

/*
 *  Acklam's Algorithm
 *  https://stackedboxes.org/2017/05/01/acklams-normal-quantile-function/
 */

const float a[] = {
    -3.969683028665376e+01, 
    2.209460984245205e+02,
    -2.759285104469687e+02,
    1.383577518672690e+02,
    -3.066479806614716e+01,
    2.506628277459239e+00
};

const float b[] = {
    -5.447609879822406e+01,
    1.615858368580409e+02,
    -1.556989798598866e+02,
    6.680131188771972e+01,
    -1.328068155288572e+01
};

const float c[] = {
    -7.784894002430293e-03,
    -3.223964580411365e-01,
    -2.400758277161838e+00,
    -2.549732539343734e+00,
     4.374664141464968e+00,
     2.938163982698783e+00
};

const float d[] = {
    7.784695709041462e-03,
    3.224671290700398e-01,
    2.445134137142996e+00,
    3.754408661907416e+00
};

static PyObject* invcdf(PyObject* self, PyObject* args)
{
    float x, q, r, z;
    float p_low = 0.02425;

    /*  Parse single numpy array argument */
    if (!PyArg_ParseTuple(args, "f", &x)) return NULL;

    if (x < p_low)
    {
        q = sqrt(-2*log(x));
        z = (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1);

        return Py_BuildValue("f", z);
    }
    if (x > 1.0 - p_low)
    {
        q = sqrt(-2*log(1-x));
        z = -(((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1);

        return Py_BuildValue("f", z);
    }
    
    q = (x - 0.5);
    r = q * q;
    z = (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]) * q / (((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1);

    return Py_BuildValue("f", z);
}


static PyMethodDef NormieImplMethods[] =
{
     {"pdf", pdf, METH_VARARGS, "Normal probability density function"},
     {"cdf", cdf, METH_VARARGS, "Normal cumulative distribution function"},
     {"invcdf", invcdf, METH_VARARGS, "Normal inverse cumulative distribution function"},
     {NULL, NULL, 0, NULL}
};

struct module_state {
	PyObject *error;
};

static int normie_impl_traverse(PyObject *m, visitproc visit, void *arg) {
	Py_VISIT(((struct module_state*)PyModule_GetState(m))->error);
	return 0;
}

static int normie_impl_clear(PyObject *m) {
	Py_CLEAR(((struct module_state*)PyModule_GetState(m))->error);
	return 0;
}

static struct PyModuleDef moduledef = {
	PyModuleDef_HEAD_INIT,
	"normie_impl",
	NULL,
	sizeof(struct module_state),
	NormieImplMethods,
	NULL,
	normie_impl_traverse,
	normie_impl_clear,
	NULL
};


/* module initialization */
PyMODINIT_FUNC
PyInit_normie_impl(void)
{
     PyObject *module = PyModule_Create(&moduledef);

     if (module == NULL)
	 return NULL;

     struct module_state *st = (struct module_state*)PyModule_GetState(module);
     // ??
     st->error = PyErr_NewException("exact_cover.Error", NULL, NULL);
     if (st->error == NULL) {
	     Py_DECREF(module);
	     return NULL;
     }

     return module;
}


