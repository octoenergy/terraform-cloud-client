import setuptools

with open("README.md", "r") as f:
    long_description = f.read()


setuptools.setup(
    name="terraform-enterprise-client",
    version="0.0.1",
    author="Octopus Energy",
    author_email="talent@octopus.energy",
    description="A client for HashiCorp Terraform Enterprise",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/octoenergy/terraform-enterprise-client",
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    entry_points={"console_scripts": ["tfe = tfe.__main__:main"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
