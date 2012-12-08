template = """

from distutils.core import setup, Extension

import sys
import pprint
pprint.pprint(sys.path)

from Cython.Distutils import build_ext

ext = Extension("%(name)s", sources = [ "%(pyx_file_base)s"], language="c++",
        include_dirs = %(include_dirs)r,
        extra_compile_args = [])

setup(cmdclass = {'build_ext' : build_ext},
      name="%(name)s",
      version="0.0.1",
      ext_modules = [ext]
     )

"""

def compile_and_import(pyx_file, name=None, *include_dirs, **kws):

    debug = kws.get("debug")
    import os.path
    import shutil
    import tempfile

    if name is None:
        name, _ = os.path.splitext(os.path.basename(pyx_file))

    tempdir = tempfile.mkdtemp()
    if debug:
        print
        print "tempdir=", tempdir
        print
    shutil.copy(pyx_file, tempdir)
    #if kws.get("copy_subdirs"):
        #shutil.copytree(kws.get("copy_subdirs")[0], tempdir)
    pyx_file_base = os.path.basename(pyx_file)
    include_dirs = [ os.path.abspath(d) for d in include_dirs]
    setup_code = template % locals()
    if debug:
        print
        print "-"*70
        print setup_code
        print "-"*70
        print

    now = os.getcwd()
    os.chdir(tempdir)
    with open("setup.py", "w") as fp:
        fp.write(setup_code)


    import sys
    sys.path.insert(0, tempdir)
    if debug:
        print
        print "-"*70
        import pprint
        pprint.pprint(sys.path)
        print "-"*70
        print

    assert os.system("python setup.py build_ext --inplace") == 0
    result = __import__(name)
    if debug:
        print "imported", result

    sys.path = sys.path[2:]
    os.chdir(now)
    return result


def find_cycle(graph_as_dict):
    """ modified version of
    http://neopythonic.blogspot.de/2009/01/detecting-cycles-in-directed-graph.html
    """

    nodes = graph_as_dict.keys()
    for n in graph_as_dict.values():
        nodes.extend(n)
    todo = list(set(nodes))
    while todo:
        node = todo.pop()
        stack = [node]
        while stack:
            top = stack[-1]
            for node in graph_as_dict.get(top, []):
                if node in stack:
                    return stack[stack.index(node):]
                if node in todo:
                    stack.append(node)
                    todo.remove(node)
                    break
            else:
                node = stack.pop()
    return None
