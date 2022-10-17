from setuptools import setup,find_packages

version = '1.0.0'

with open('./README.md',encoding='utf-8') as f:
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
    packages=find_packages(exclude=["tests*", "pymysql.tests*"]),
    python_requires=">=3.7",
    extras_require={
        "zlib": ["cryptography"],
        "ed25519": ["PyNaCl>=1.4.0"],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Image",
    ],
    keywords="CgBI",
)