# Always prefer setuptools over distutils
from setuptools import setup


# This call to setup() does all the work
setup(
    name="edat_utils",
    version="0.6.9",
    description="Biblioteca de Apoio ao desenvolvimento no EDAT",
    long_description="# Utilitarios EDAT <br /> Classes utilitarias utilizadas pelo EDAT.",
    long_description_content_type="text/markdown",
    author="Escritório de Dados",
    author_email="dados@unicamp.br",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Operating System :: OS Independent"
    ],
    packages=["edat_utils"],
    include_package_data=True,
    install_requires=["trino", "SQLAlchemy",
                      "python-decouple", "strawberry-graphql"]
)
