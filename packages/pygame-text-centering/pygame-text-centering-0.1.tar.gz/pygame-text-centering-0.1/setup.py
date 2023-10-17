from setuptools import setup, find_packages

setup(
    name='pygame-text-centering',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pygame', 'numpy', 'joblib', 'scipy', 'threadpoolctl', 'scikit-learn'
    ],
    author='Melvin Chen',
    author_email='melvinchen610@gmail.com',
    description='Fixes text-centering issues in pygame!.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/mchen610/pygame-text-centering',
)
