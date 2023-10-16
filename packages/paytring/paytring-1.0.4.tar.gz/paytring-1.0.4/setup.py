from setuptools import setup, find_packages

with open("Paytring/README.md", "r") as f:
    long_description = f.read()

setup(
    name="paytring",
    version="1.0.4",
    description="A SDK which helps to create, fetch or refund an order on Paytring",
    package_dir={"": "Paytring"},
    packages=find_packages(where="Paytring"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/paytring/python-sdk",
    author="Paytirng",
    author_email="developer@paytring.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    install_requires=["requests==2.31.0","urllib3==2.0.2"],
    python_requires=">=3.10",
)