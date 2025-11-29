from setuptools import setup, Extension
from Cython.Build import cythonize
import sys
import os

# Detectar el compilador
if sys.platform == 'win32':
    # Windows con MSVC
    extra_compile_args = ['/O2', '/std:c++17']
    extra_link_args = []
else:
    # Linux/Mac con GCC/Clang
    extra_compile_args = ['-O3', '-std=c++17']
    extra_link_args = []

# Configurar la extensión
extensions = [
    Extension(
        name="grafo_wrapper",
        sources=[
            "cython/grafo_wrapper.pyx",
            "src/GrafoDisperso.cpp"
        ],
        include_dirs=["include"],
        language="c++",
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,
    )
]

setup(
    name="NeuroNet",
    version="1.0.0",
    description="Sistema híbrido C++/Python para análisis de grafos masivos",
    ext_modules=cythonize(
        extensions,
        compiler_directives={
            'language_level': "3",
            'embedsignature': True
        }
    ),
    zip_safe=False,
)
