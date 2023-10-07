from setuptools import setup, find_packages

setup(
    name="exception-handling-decorator",
    version="0.1.4",
    author="Zoran Jankovic",
    author_email="bpzoran@yahoo.com",
    url="https://github.com/bpzoran/exception-handling-decorator",
    packages=find_packages(),
    long_description=open("README.md").read(),
    # Specify the content type explicitly
    long_description_content_type="text/markdown",
    description="ExceptionHandler: Python library to decorate\
        exception handling.",
)
