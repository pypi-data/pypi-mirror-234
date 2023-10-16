from distutils.core import setup
from Cython.Build import cythonize

extensions = cythonize(
    "src/tabatu/core/tabatu_cpp.pyx",
    language_level="3",
    include_path=["src/tabatu/core"],
)

setup(
    ext_modules=extensions,
)
