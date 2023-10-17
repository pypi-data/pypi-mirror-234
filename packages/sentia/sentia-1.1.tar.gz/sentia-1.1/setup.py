import setuptools

print(setuptools.find_packages())
with open("D:\\SENTIA\\readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sentia", 
    version="1.1",
    author="Locutusque",
    author_email="locutusque.airshipcraft@gmail.com",
    description="A text generation model combining multiple neural network architectures",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Locutusque/SENTIA.py",
    packages=setuptools.find_packages(),
    package_data={
    'SENTIA': ['*', '*/utils'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "torch>=2.0",
        "transformers>=3.0.0",
        "datasets>=1.7.0",
        "nltk",
        "tqdm",
        "sacrebleu",
        "rotary-embedding-torch",
        "wandb",
        "configparser",
        "psutil",
        "colorama",

    ] 
)