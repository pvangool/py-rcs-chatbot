import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rcs_chatbot",
    version="0.0.3",
    author="Paul van Gool",
    author_email="pvangool@gmail.com",
    description="Python SDK for RCS MaaP chatbot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pvangool/py-rcs-chatbot",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
