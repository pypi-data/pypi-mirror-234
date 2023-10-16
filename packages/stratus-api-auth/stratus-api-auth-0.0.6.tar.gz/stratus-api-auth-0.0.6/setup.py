import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()
# with open('requirements.txt') as f:
#    requirements = f.readlines()

requirements = [
        "python-jose[cryptography]>=3.1.0",
        "stratus-api-core>=0.0.29"
    ]

setuptools.setup(
    name="stratus-api-auth",  # Replace with your own username
    version="0.0.6",
    author="DOT",
    author_email="dot@adara.com",
    description="An API framework for simplified OAuth",
    long_description="Sample",
    long_description_content_type="text/markdown",
    include_package_data=True,
    url="https://bitbucket.org/adarainc/stratus-api-auth",
    setup_requires=['pytest-runner'],
    test_requires=requirements,
    packages=['stratus_api.auth'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
    install_requires=requirements
)
