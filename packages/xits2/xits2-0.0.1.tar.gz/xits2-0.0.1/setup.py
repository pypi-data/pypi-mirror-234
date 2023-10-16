from setuptools import setup, find_packages

setup(
    name="xits2",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "stix2>=3.0.1",
    ],
    extras_require={
        "dev": [
            # List your dev dependencies here
            # For example:
            # 'pytest>=6.2.4',
        ],
    },
    python_requires=">=3.6",
    author="Tomás Lima, Adrian Dinis",
    author_email="tomas@abusetotal.com, adrian@abusetotal.com",
    description="",
    license="",
    url="http://github.com/opensticks/xits2",
)
