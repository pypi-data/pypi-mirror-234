from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="nzsp-pms-utils",
    version="2.2.0",
    author="Danone New Zealand Supply Point",
    author_email="juan.parra3@danone.com",
    url="https://github.com/danone/nzsp.plant-management-system-utils",
    description="Contains code that is share across the microservices",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware",
    ],
    python_requires=">=3.7",
    packages=find_packages(exclude=["tests"]),
    install_requires=["flask", "requests"],
)
