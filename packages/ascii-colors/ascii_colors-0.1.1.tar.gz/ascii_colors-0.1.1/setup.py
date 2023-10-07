from setuptools import setup, find_packages
# Define long description (usually from README.md)
with open('README.md', 'r') as readme_file:
    LONG_DESCRIPTION = readme_file.read()

setup(
    name='ascii_colors',
    version='0.1.1',
    description='A Python library for pretty console printing with colors and styles',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Saifeddine ALOUI (ParisNeo)',
    author_email='aloui.saifeddine@gmail.com',
    url='https://github.com/ParisNeo/console_tools',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',  # Specify Apache 2.0 license
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',  # You can add more supported Python versions
    ],
    python_requires='>=3.8',  # Specify Python version requirements
)
