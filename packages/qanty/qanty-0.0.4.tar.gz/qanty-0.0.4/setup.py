from setuptools import setup, find_packages

__version__ = "0.0.4"

setup(
    name='qanty',
    version=__version__,
    description="Qanty API Client",
    long_description=open("README.md").read().strip(),
    long_description_content_type="text/markdown",
    license='MIT',
    author="Juan F. Duque",
    author_email='jfelipe@grupodyd.com',
    packages=find_packages(exclude=["tests", "tests.*"]),
    include_package_data=True,
    url='https://www.qanty.com',
    project_urls={
        "Source": "https://github.com/grupodyd/python-qanty",
        "Tracker": "https://github.com/grupodyd/python-qanty/issues",
    },
    keywords='qanty',
    python_requires=">=3.8.0",
    install_requires=[
          "requests >= 2.0.0",
      ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Software Development :: Libraries :: Python Modules",
      ],
)
