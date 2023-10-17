from setuptools import setup, find_packages

setup(
    name='pygame-text-centering',
    version='0.6',
    packages=find_packages(),
    install_requires=[
        'pygame', 'numpy', 'joblib', 'scipy', 'threadpoolctl', 'scikit-learn'
    ],
    author='Melvin Chen',
    author_email='melvinchen610@gmail.com',
    description='A Pygame library to fix Pygame\'s text-centering!',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/mchen610/pygame-text-centering',
)
