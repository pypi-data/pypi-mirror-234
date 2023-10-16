import setuptools
  
with open("README.md", "r") as fh:
    description = fh.read()
  
setuptools.setup(
    name="test_package_new_test",
    version="0.0.1",
    author="GhaniyyaMedghoul",
    author_email="gmedghoul@aneo.fr",
    packages=["test_package_new_test"],
    description="A sample test package",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/ghaniyyamedghoul/test-tackage.git",
    license='MIT',
    python_requires='>=3.8',
    install_requires=[]
)
