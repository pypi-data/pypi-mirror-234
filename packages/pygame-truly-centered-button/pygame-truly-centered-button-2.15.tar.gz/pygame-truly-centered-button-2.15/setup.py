from setuptools import setup, find_packages

setup(
    name='pygame-truly-centered-button',
    version='2.15',
    packages=find_packages(),
    install_requires=[
        'pygame', 'numpy', 'joblib', 'scipy', 'threadpoolctl', 'scikit-learn'
    ],
    author='Melvin Chen',
    author_email='melvinchen610@gmail.com',
    description='THIS LIBRARY IS DEPRECATED',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/mchen610/pygame-text-centering',
)
