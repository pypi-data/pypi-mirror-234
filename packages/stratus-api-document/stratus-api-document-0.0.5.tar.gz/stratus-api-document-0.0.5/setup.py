import setuptools
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
# with open('requirements.txt') as f:
#    requirements = f.readlines()

requirements = [
    "google-api-python-client>=1.7.11",
    "google-cloud-firestore>=1.6.2",
    "stratus-api-core>=0.0.29",
    "sphinx>=3.0.4",
    "sphinxcontrib-napoleon>=0.7"
]

setuptools.setup(
    name="stratus-api-document",  # Replace with your own username
    version="0.0.5",
    author="DOT",
    author_email="dot@adara.com",
    description="An API stratus_api for simplified development",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    url="https://bitbucket.org/adarainc/stratus-api-firestore",
    setup_requires=['pytest-runner'],
    test_requires=requirements,
    packages=setuptools.find_namespace_packages(include=['stratus_api.*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
    install_requires=requirements
)
