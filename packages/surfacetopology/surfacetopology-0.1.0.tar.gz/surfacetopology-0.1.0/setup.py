from setuptools import setup, Extension
from Cython.Distutils import build_ext

NAME = "surfacetopology"
VERSION = "0.1.0"
DESCR = "Check the validity and determine the topology of a triangulated surface"
URL = "https://github.com/jacquemv/surfacetopology"
REQUIRES = ['numpy', 'cython']

AUTHOR = "Vincent Jacquemet"
EMAIL = "vincent.jacquemet@umontreal.ca"

LICENSE = "MIT"

SRC_DIR = "surfacetopology"
PACKAGES = [SRC_DIR]

ext = Extension("topology",
                sources=[SRC_DIR + "/trisurftopology.cpp", SRC_DIR + "/topology.pyx"],
                libraries=[],
                extra_compile_args=['-O3'],
                extra_link_args=[],
                language="c++",
                include_dirs=[SRC_DIR])

EXTENSIONS = [ext]

setup(install_requires=REQUIRES,
      packages=PACKAGES,
      zip_safe=False,
      name=NAME,
      version=VERSION,
      description=DESCR,
      author=AUTHOR,
      author_email=EMAIL,
      url=URL,
      license=LICENSE,
      cmdclass={"build_ext": build_ext},
      ext_modules=EXTENSIONS
)
