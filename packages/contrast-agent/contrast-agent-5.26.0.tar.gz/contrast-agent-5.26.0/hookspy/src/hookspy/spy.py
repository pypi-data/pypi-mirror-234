import sys
from argparse import ArgumentParser

from . import hookspy


method_flags_map = {
    hookspy.METH_O: "METH_O",
    hookspy.METH_NOARGS: "METH_NOARGS",
    hookspy.METH_VARARGS: "METH_VARARGS",
    hookspy.METH_KEYWORDS: "METH_KEYWORDS",
    hookspy.METH_FASTCALL: "METH_FASTCALL",
    hookspy.METH_VARARGS | hookspy.METH_KEYWORDS: "METH_VARARGS|METH_KEYWORDS",
    hookspy.METH_FASTCALL | hookspy.METH_KEYWORDS: "METH_FASTCALL|METH_KEYWORDS",
    hookspy.METH_NEW: "METH_NEW",
    hookspy.METH_INIT: "METH_INIT",
}

type_spies = [
    ("unicode", "PyUnicode_Type", hookspy.find_unicode_hook),
    ("bytes", "PyBytes_Type", hookspy.find_bytes_hook),
    ("bytearray", "PyByteArray_Type", hookspy.find_bytearray_hook),
]


def main():
    p = ArgumentParser(description="find method hook locations for python string types")
    p.add_argument("method", type=str, help="Name of method")
    args = p.parse_args()

    print(sys.version)

    for name, typename, spy in type_spies:
        result = spy(args.method)
        if result is None:
            print('{} hook for "{}" not found'.format(name, args.method))
            continue

        index, flags = result
        flagname = method_flags_map.get(flags, "UNKNOWN")
        print("{:17} offset={:2}, flags={}".format(typename + ":", index, flagname))
