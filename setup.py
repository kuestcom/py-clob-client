import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kuest-py-clob-client",
    version="0.34.4",
    author="Kuest Engineering",
    author_email="engineering@kuest.com",
    maintainer="Kuest Engineering",
    maintainer_email="engineering@kuest.com",
    description="Python client for the Kuest CLOB",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kuestcom/py-clob-client",
    install_requires=[
        "eth-account>=0.13.0",
        "eth-utils>=4.1.1",
        "kuest-py-eip712-structs==0.0.2",
        "kuest-py-order-utils==0.3.2",
        "python-dotenv",
        "kuest-py-builder-signing-sdk==0.0.1",
        "httpx[http2]>=0.27.0",
    ],
    project_urls={
        "Bug Tracker": "https://github.com/kuestcom/py-clob-client/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.9.10",
)
