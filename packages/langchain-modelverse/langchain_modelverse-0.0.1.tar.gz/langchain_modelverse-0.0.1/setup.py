from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'LangChain Custom LLM for ModelVerse'
LONG_DESCRIPTION = 'LangChain Custom LLM for ModelVerse'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="langchain_modelverse",
    version=VERSION,
    author="John Doe",
    author_email="johndoe@johndoe.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["langchain", "requests"],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'

    keywords=['python'],
    classifiers=[]
)