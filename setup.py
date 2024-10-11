import os

from setuptools import setup, find_packages

def readme() -> str:
    """Utility function to read the README.md.

    This function is used to fetch the content of the `README.md` file, 
    which is typically used as the `long_description` in the `setup()` function.
    This helps to maintain a top-level README file for documentation and ensures 
    that the package description on distribution platforms (e.g., PyPI) is in sync 
    with the project's primary documentation.

    Args:
        nothing

    Returns:
        String of readed README.md file.
    """
    return open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

setup(
    name='mlops-student-performance',
    version='0.1.0',
    author='aalva',
    author_email='alexis.alvajn@gmail.com',
    description='MLOps project',
    python_requires='>=3',
    license='MIT',
    url='',
    packages=find_packages(),
    long_description=readme(),
)