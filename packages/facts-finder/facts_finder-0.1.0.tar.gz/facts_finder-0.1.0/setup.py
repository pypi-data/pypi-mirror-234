import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="facts_finder",
    version="0.1.0",
    author="ALIASGAR - ALI",
    author_email="aholo2000@gmail.com",
    description="facts_finder for Networking Geeks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alias1978/facts_finder",
    # package_data={
    #     'facts_finder': [
    #         'generators/commands/*',
    #         'modifiers/cisco/commands/*',
    #         'modifiers/juniper/commands/*', 
    #         ],
    # },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=['pandas', 'numpy', 'xlrd', 'openpyxl', 'nettoolkit'],
)
