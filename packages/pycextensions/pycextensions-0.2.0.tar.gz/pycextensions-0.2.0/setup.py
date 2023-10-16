import pathlib
import sys

import setuptools

long_description = pathlib.Path("README.md").read_text(encoding="utf-8")

with open("./src/pycextensions/__init__.py") as f:
    for line in f.readlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            version = line.split(delim)[1]
            break
    else:
        print("Can't find version! Stop Here!")
        exit(1)

# Determine which attach binary to take into package
package_data = {
    "pycextensions": [
        # 暂时不向包中添加任何文件,只是示例
        "modules/__init__.py",
    ]
}

setuptools.setup(
    name="pycextensions",
    version=version,
    author="ayuge",
    author_email="ayuge@gmail.com",
    description="a python c extension example",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shengchenyang",
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    package_data=package_data,
    ext_modules=[
        setuptools.Extension(
            "pycextensions.fprintf",
            sources=[
                "src/pycextensions/modules/fprintf.c",
            ],
            extra_compile_args={"win32": []}.get(sys.platform, ["-Werror", "-std=c99"]),
            extra_link_args={"win32": []}.get(sys.platform, ["-lpthread"]),
        )
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Education",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=["objprint>=0.1.3"],
    extras_require={"full": ["rich", "orjson"]},
)
