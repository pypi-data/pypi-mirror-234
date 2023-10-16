import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()
# with open('requirements.txt') as f:
#     requirements = f.readlines()

setuptools.setup(
    name="stratus-api-sql",  # Replace with your own username
    version="0.0.4",
    author="DOT",
    author_email="dot@adara.com",
    description="Simplified SQL API",
    long_description="",
    long_description_content_type="text/markdown",
    include_package_data=True,
    url="https://bitbucket.org/adarainc/stratus-api-sql",
    setup_requires=['pytest-runner'],
    packages=['stratus_api.sql'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
    install_requires=[
        "sqlalchemy>=1.3.18",
        "stratus-api-core>=0.0.29",
        "alembic>=1.4.2"
    ]
)
