import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()
# with open('requirements.txt') as f:
#     requirements = f.readlines()

setuptools.setup(
    name="stratus-api-events",  # Replace with your own username
    version="0.0.7",
    author="DOT",
    author_email="dot@adara.com",
    description="Streamlined Pubsub Events",
    long_description="",
    long_description_content_type="text/markdown",
    include_package_data=True,
    url="https://bitbucket.org/adarainc/stratus-api-events",
    setup_requires=['pytest-runner'],
    packages=['stratus_api.events'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
    install_requires=[
        "stratus-api-core>=0.0.29",
        "google-cloud-pubsub>=1.6.0"
    ]
)
