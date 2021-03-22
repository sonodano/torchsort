#!/usr/bin/env python3

import os
from functools import lru_cache
from subprocess import DEVNULL, call

from setuptools import setup
from torch.utils import cpp_extension


@lru_cache(None)
def cuda_toolkit_available():
    # https://github.com/idiap/fast-transformers/blob/master/setup.py
    try:
        call(["nvcc"], stdout=DEVNULL, stderr=DEVNULL)
        return True
    except FileNotFoundError:
        return False


def ext_modules():
    extensions = [
        cpp_extension.CppExtension(
            "torchsort.isotonic_cpu",
            sources=["torchsort/isotonic_cpu.cpp"],
            extra_compile_args=["-fopenmp", "-ffast-math"],
        ),
    ]
    if cuda_toolkit_available():
        extensions.append(
            cpp_extension.CUDAExtension(
                "torchsort.isotonic_cuda",
                sources=["torchsort/isotonic_cuda.cu"],
            )
        )
    return extensions


with open("README.md") as f:
    long_description = f.read()
setup(
    name="torchsort",
    version="0.0.5",
    description="Differentiable sorting and ranking in PyTorch",
    author="Teddy Koker",
    url="https://github.com/teddykoker/torchsort",
    license="Apache",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["torchsort"],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    install_requires=["torch"],
    python_requires=">=3.8",
    extras_require={
        "testing": [
            "pytest",
            "torch",
        ],
    },
    ext_modules=ext_modules(),
    cmdclass={"build_ext": cpp_extension.BuildExtension},
    include_package_data=True,
)
