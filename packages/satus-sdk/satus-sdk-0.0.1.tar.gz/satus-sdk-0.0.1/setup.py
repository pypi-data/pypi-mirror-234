import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="satus-sdk",
    version="0.0.1",
    author="Jonas Briguet",
    author_email="briguetjo@yahoo.de",
    description="A python wrapper for the satus.dev API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://satus.dev",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
        'requests',
        'requests-toolbelt',
        'urllib3',
    ],
    keywords='transcription, audio, video, speech, satus, api, wrapper',
    project_urls={
        'Homepage': 'https://satus.dev',
    }
)
