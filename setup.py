from setuptools import setup, find_packages

setup(
    name='chord_matrix',
    version='0.1.0',
    author='Habib Nasir',
    author_email='habibnasir23@gmail.com',
    description='A package to generate a matrix for chord diagrams',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Habibnasir23/chord_matrix',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
    ],
    entry_points={
        'console_scripts': [
            'chord_matrix=chord_matrix.main:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
