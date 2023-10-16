import setuptools

setuptools.setup(
    name='stratus-api-storage',
    version="0.0.6",
    author="DOT",
    author_email="dot@adara.com",
    description="An API framework for simplified development",
    long_description="Sample",
    long_description_content_type="text/markdown",
    include_package_data=True,
    url="https://github.com/dot-at-adara/storage",
    setup_requires=['pytest-runner'],
    test_requires=[
        "boto3>=1.13.10",
        "botocore>=1.16.10",
        "google-api-python-client>=1.7.11",
        "google-cloud-storage>=1.28.1",
        "paramiko>=2.7.1",
        "stratus-api-core>=0.0.29"
    ],
    packages=setuptools.find_namespace_packages(include=['stratus_api.*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
    install_requires=[
        "boto3>=1.13.10",
        "botocore>=1.16.10",
        "google-api-python-client>=1.7.11",
        "google-cloud-storage>=1.28.1",
        "paramiko>=2.7.1",
        "stratus-api-core>=0.0.29"
    ]
)
