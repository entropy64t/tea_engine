from setuptools import setup, Extension
from Cython.Build import cythonize

extensions = [
    Extension(
        "tea_engine.vector",
        ["tea_engine/cy/vector.pyx"],
    ),
]

setup(
    name="tea-engine",
    ext_modules=cythonize(
        extensions,
        compiler_directives={"language_level": "3"},
    ),
)
