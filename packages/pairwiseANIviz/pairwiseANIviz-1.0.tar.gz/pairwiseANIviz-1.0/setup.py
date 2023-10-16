from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
    name='pairwiseANIviz',
    version='1.0',
    description="Pairwise ANI (Average Nucleotide Identity) visulization tool.",
    url="https://github.com/RunJiaJi/pairwiseANIviz",
    author='Runjia Ji',
    author_email='jirunjia@gmail.com',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'pandas',
        'matplotlib',
        'seaborn',
        'scipy',
    ],
    entry_points={
        'console_scripts':[
            'pairwiseANIviz = pairwiseANIviz:main',
        ]
    },
)