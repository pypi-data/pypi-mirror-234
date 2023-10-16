#https://towardsdatascience.com/how-to-package-your-python-code-df5a7739ab2e
#https://packaging.python.org/tutorials/packaging-projects/

# Use the following commands to build
# python setup.py bdist_conda
# conda install --use-local resaid

# For pip
# pip install -e .

import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="resaid",
    version="0.1.2",
    author="Greg Easley",
    author_email="greg@easley.dev",
    description="Reservoir engineering tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/geasley-rsc/resaid",
    project_urls={
        "Bug Tracker": "https://github.com/geasley-rsc/resaid/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'numpy>=1.22',
        'pandas>=1.5.3',
        'scipy>=1.0.0',
        'statsmodels>=0.13.5',
        'tqdm>=4.65.0',
    ],
    packages=setuptools.find_packages(),
    #python_requires=">=3.6",
)