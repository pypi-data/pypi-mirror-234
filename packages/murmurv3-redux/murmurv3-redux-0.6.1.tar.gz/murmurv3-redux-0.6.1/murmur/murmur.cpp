//-----------------------------------------------------------------------------
// Murmur Hash Library, by Bryan McLemore and Chris Heald
// Original Portions (c) 2008 Bryan McLemore and Chris Heald
// Released under The MIT License
// http://www.opensource.org/licenses/mit-license.php
//
// Portions of this code was based off of MurmurHash2, by Austin Appleby
// Info about that can be found at: http://murmurhash.googlepages.com/
// Is not quite as performant as the original since certain parts were broken
// up to make code more maintainable.
//
// WARNINGS: PLEASE NOTE!
// Including from the original code is a warning about assumptions and limits:
// 1. We can read a 4-byte value from any address without crashing
// 2. sizeof(int) == 4
// Also please note that:
// It will not produce the same results on little-endian and big-endian
//    machines.
//
// It would be fairly simple, I believe to swap out implementations based on
// the alignment and if your machine is little or big endian.  However, those
// are not in this implementation.

#define PY_SSIZE_T_CLEAN

#include <Python.h>
#include <fstream>
#include <iostream>
#include <sys/stat.h>

#if PY_MAJOR_VERSION >= 3
#define IS_PY3K
#endif

using namespace std;

const unsigned int m = 0x5bd1e995;
const int r = 24;

static unsigned int murmur_initialize(unsigned int len, unsigned int seed) {
    return seed ^ len;
}

static unsigned int murmur_loop(const unsigned char * buffer, Py_ssize_t len, unsigned int h) {

    while(len >= 4) {
		unsigned int k = *(unsigned int *)buffer;

		k *= m;
		k ^= k >> r;
		k *= m;

		h *= m;
		h ^= k;

		buffer += 4;
		len -= 4;
	}

    switch(len) {
	case 3: h ^= buffer[2] << 16;
	case 2: h ^= buffer[1] << 8;
	case 1: h ^= buffer[0];
	        h *= m;
	};

	return h;
}

static unsigned int murmur_finalize(unsigned int h) {
    h ^= h >> 13;
	h *= m;
	h ^= h >> 15;

	return h;
}

static unsigned int MurmurHash2_String( const void * key, Py_ssize_t len, unsigned int seed ) {
    unsigned int cur = murmur_initialize(len, seed);
	const unsigned char * data = (const unsigned char *)key;
    cur = murmur_loop(data, len, cur);
    return murmur_finalize(cur);
}

static unsigned int MurmurHash2_Stream(ifstream &stream, unsigned int seed) {

	stream.seekg(0, ios::end);
	unsigned int len = stream.tellg();
	stream.seekg (0, ios::beg);

	char buffer[4096];
	unsigned int cur = murmur_initialize(len, seed);

	while(!stream.eof()) {
		stream.read(buffer, 4096);
		unsigned int chunklen = stream.gcount();
		if (!chunklen) {
			break;
		}
	    cur = murmur_loop((const unsigned char *)&buffer[0], chunklen, cur);
	}

	return murmur_finalize(cur);
}

static unsigned int MurmurHash2_ResampledStream(ifstream &stream, unsigned int seed) {

	stream.seekg(0, ios::end);
	unsigned int len = stream.tellg();
	stream.seekg (0, ios::beg);

    char* buffer = new char[len];

    stream.read(buffer, len);

    int j = 0;

    for ( unsigned int x = 0; x < len; x++) {
        bool copy = true;
        switch (buffer[x]) {
            case 0x0a:
            case 0x0d:
            case 0x20:
            case 0x09:
                copy = false;
        }

        if (copy) {
            buffer[j++] = buffer[x];
        }
    }

	unsigned int cur = murmur_initialize(j, seed);
	cur = murmur_loop((const unsigned char *)&buffer[0], j, cur);

    delete[] buffer;

	return murmur_finalize(cur);
}


static PyObject * murmur_file_hash(PyObject *self, PyObject *args) {

	unsigned int seed = 0;
	const char *filename;
	ifstream in;

	if (!PyArg_ParseTuple(args, (char *)"s|I", &filename, &seed))
		return NULL;

	in.open(filename, ios::in | ios::binary);
	if (!in.good()) {
		PyErr_SetString(PyExc_RuntimeError, "Unable to open file");
		in.close();
		return NULL;
	} else {
		seed = MurmurHash2_Stream(in, seed);
	}
	in.close();
	return Py_BuildValue("I", seed);
}

static PyObject * murmur_resampled_file_hash(PyObject *self, PyObject *args) {

	unsigned int seed = 0;
	const char *filename;
	ifstream in;

	if (!PyArg_ParseTuple(args, (char *)"s|I", &filename, &seed))
		return NULL;

	in.open(filename, ios::in | ios::binary);
	if (!in.good()) {
		PyErr_SetString(PyExc_RuntimeError, "Unable to open file");
		in.close();
		return NULL;
	} else {
		seed = MurmurHash2_ResampledStream(in, seed);
	}
	in.close();
	return Py_BuildValue("I", seed);
}

static PyObject * murmur_string_hash(PyObject *self, PyObject *args) {
	const char *s;
	Py_ssize_t len;
	unsigned int seed = 0;
	if (!PyArg_ParseTuple(args, "s#|I", &s, &len, &seed))
		return NULL;
	return Py_BuildValue("I", MurmurHash2_String(s, len, seed));
}

static PyObject * murmur_stream_initialize(PyObject *self, PyObject *args) {
	unsigned int len;
	unsigned int seed = 0;
	if (!PyArg_ParseTuple(args, "II", &len, &seed))
		return NULL;
	return Py_BuildValue("I", murmur_initialize(len, seed));
}


static PyObject * murmur_stream_iterate(PyObject *self, PyObject *args) {
	const unsigned char * s;
	Py_ssize_t len;
	unsigned int seed = 0;
	if (!PyArg_ParseTuple(args, "s#|I", &s, &len, &seed))
		return NULL;
	return Py_BuildValue("I", murmur_loop(s, len, seed));
}

static PyObject * murmur_stream_finalize(PyObject *self, PyObject *args) {
	unsigned int seed = 0;
	if (!PyArg_ParseTuple(args, "I", &seed))
		return NULL;
	return Py_BuildValue("I", murmur_finalize(seed));
}

static PyMethodDef MurmurMethods[] = {
	{"file_hash", murmur_file_hash, METH_VARARGS, "Hash a file"},
	{"resampled_file_hash", murmur_resampled_file_hash, METH_VARARGS, "Resample and then hash a file"},
	{"initialize", murmur_stream_initialize, METH_VARARGS, "_"},
	{"iterate", murmur_stream_iterate, METH_VARARGS, "_"},
	{"finalize", murmur_stream_finalize, METH_VARARGS, "_"},
	{"string_hash", murmur_string_hash, METH_VARARGS, "Hash a string"},
	{NULL, NULL, 0, NULL}
};

static struct PyModuleDef murmur_module_definition = {
    PyModuleDef_HEAD_INIT,
    "murmur",
    "Python 3 port of Murmur",
    -1,
    MurmurMethods
};

PyMODINIT_FUNC PyInit_murmur(void){
    Py_Initialize();
    return PyModule_Create(&murmur_module_definition);
}

int main(int argc, char *argv[]) {}
