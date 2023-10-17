import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name                = 'f_yolov8',
    version             = '0.0.7',
    author              = 'jskim1102',
    author_email        = 'deepi.contact.us@gmail.com',
    long_description=long_description,
    packages=setuptools.find_packages(),
    python_requires     = '>=3.8',
)