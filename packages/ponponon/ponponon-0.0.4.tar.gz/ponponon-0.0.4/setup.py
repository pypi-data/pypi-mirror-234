import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

from pon import VERSION

setuptools.setup(
    name="ponponon",
    version=VERSION,
    author="ponponon",
    author_email="1729303158@qq.com",
    maintainer='ponponon',
    maintainer_email='1729303158@qq.com',
    license='MIT License',
    platforms=["all"],
    description="An advanced message queue framework, derived from nameko",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ponponon/pon",
    packages=setuptools.find_packages(),
    install_requires=[
        "pydantic",
        "loguru",
        "pyyaml",
        "eventlet",
        "kombu",
        "werkzeug",
    ],
    extras_require={
    },
    entry_points={
        'console_scripts': [
            'pon=pon.cli.main:cli',
        ]
    },
    classifiers=[
        "Programming Language :: Python",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
    ]
)
