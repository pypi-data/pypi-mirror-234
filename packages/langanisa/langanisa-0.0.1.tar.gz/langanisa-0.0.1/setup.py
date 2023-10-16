from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='langanisa',
    version='0.0.1',
    author='Collin Paran',
    description='A langchain, transformers, and attention_sinks wrapper for longform response generation.',
    long_description=long_description,
    long_description_content_type="text/markdown", 
    packages=find_packages(),
    install_requires=[
        'fastapi',
        'pydantic',
        'langchain',
        'transformers',
        'torch',
        'numpy',
        'pandas',
        'xformers',
        'sentencepiece',
        'accelerate>=0.20.3',
        'bitsandbytes',
        'sentence_transformers',
        'attention_sinks',
        'uvicorn'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    license='Apache-2.0', 
    python_requires='>=3.6'
)
