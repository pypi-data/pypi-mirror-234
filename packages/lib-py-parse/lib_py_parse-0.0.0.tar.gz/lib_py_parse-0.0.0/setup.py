import setuptools

long_description = ''
with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

pkg_name = 'lib_py_parse'
version = '0.0.0'

setuptools.setup(
    name=pkg_name,
    version=version,

    author='hypothesisbase',
    author_email="support@hypothesisbase.com",
    url= f'http://pypi.python.org/pypi/{pkg_name}/{version}',
    license="MIT",

    install_requires=[
        "requests",
    ],
    packages=setuptools.find_packages(),
    zip_safe=False,

    # description parameters
    long_description = long_description,
    long_description_content_type = "text/markdown",
)
