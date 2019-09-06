import setuptools

with open("README.md", "r") as f:
    long_description = f.read()


setuptools.setup(
    name="terraform-cloud-client",
    version="0.0.2",
    author="Kraken Technologies Limited",
    author_email="talent@octopus.energy",
    description="A client for HashiCorp Terraform Cloud",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/octoenergy/terraform-cloud-client",
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    entry_points={"console_scripts": ["tfc = tfc.__main__:main"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
