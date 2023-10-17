import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("pyoomysql/version.py") as fh:
    version_info = fh.read()
module_version = version_info.replace(" ","").replace('"',"").split("=")[1]

setuptools.setup(
    name="pyoomysql",
    version=module_version,
    author="Jesus Alejandro Sanchez Davila",
    author_email="jsanchez.consultant@gmail.com",
    description="Python Object-Orinted MySQL interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/jsanchezd/pyoomysql",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'mysql-connector-python'
    ]
)
