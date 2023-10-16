from setuptools import setup, find_packages

setup(
    name="UnBIAS",
    version="3",
    packages=find_packages(),
    install_requires=[
        "transformers==4.31.0",
        "bitsandbytes==0.40.2",
        "accelerate==0.21.0",
	'pandas',
        'torch',
        'peft',
        'trl',
        'fire',
        'datasets',
        'sentencepiece'
    ],

    author="Shaina Raza",
    author_email="shaina.raza@utoronto.ca",
    description="A package for detecting bias, performing named entity, and debiasing text.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/VectorInstitute/NewsMediaBias/UnBIAS",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)





