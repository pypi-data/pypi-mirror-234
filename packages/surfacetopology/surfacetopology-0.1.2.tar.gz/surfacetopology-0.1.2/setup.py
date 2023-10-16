from setuptools import setup, Extension
from Cython.Distutils import build_ext

NAME = "surfacetopology"
VERSION = "0.1.2"
DESCR = "Check the validity and determine the topology of a triangulated surface"
KEYWORDS = "triangular,mesh,surface,manifold,boundary,orientability,genus"
URL = "https://github.com/jacquemv/surfacetopology"
REQUIRES = ['numpy', 'cython']

AUTHOR = "Vincent Jacquemet"
EMAIL = "vincent.jacquemet@umontreal.ca"

LICENSE = "MIT"

SRC_DIR = "surfacetopology"
PACKAGES = [SRC_DIR]

ext = Extension(SRC_DIR + ".topology",
                sources=[SRC_DIR + "/trisurftopology.cpp", 
                         SRC_DIR + "/topology.pyx"],
                libraries=[],
                extra_compile_args=['-O3'],
                extra_link_args=[],
                language="c++",
                include_dirs=[SRC_DIR], )
ext.cython_directives = {'language_level': "3"}

EXTENSIONS = [ext]

setup(install_requires=REQUIRES,
      packages=PACKAGES,
      zip_safe=False,
      name=NAME,
      version=VERSION,
      description=DESCR,
      keywords=KEYWORDS,
      long_description=open('README.md', 'r').read(),
      long_description_content_type='text/markdown',
      author=AUTHOR,
      author_email=EMAIL,
      url=URL,
      license=LICENSE,
      cmdclass={"build_ext": build_ext},
      ext_modules=EXTENSIONS
)
