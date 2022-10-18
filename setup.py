from setuptools import setup,find_packages

version = '1.0.3'

with open('./README.rst',encoding='utf-8') as f:
    readme = f.read()


setup(
    name="PyiPNG",
    version=version,
    author="venjye",
    author_email="venjye@gmail.com",
    url="https://github.com/venjye/PyiPNG",
    project_urls={
        "Documentation": "https://github.com/venjye/PyiPNG",
    },
    description="Convert CgBI to PNG with Python",
    long_description=readme,
    packages=find_packages(exclude=["tests*"]),
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering :: Image Processing",
    ],
    keywords="CgBI",
)