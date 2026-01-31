from setuptools import setup, Extension
from Cython.Build import cythonize

extensions = [
    Extension(
        "tea_engine.vector",
        ["src/tea_engine/cy/vector.pyx"],
    ),
    Extension(
        "tea_engine.spacegrid",
        ["src/tea_engine/cy/spacegrid.pyx"],
    ),
    Extension(
        "tea_engine.renderer_concat",
        ["src/tea_engine/cy/renderer_concat.pyx"],
    ),
]

setup(
    name="tea-engine",
    ext_modules=cythonize(
        extensions,
        compiler_directives={"language_level": "3"},
    ),
)
