from setuptools import setup, find_packages

setup(
    name='pipproject1',
    version='0.1.0',
    author='Mustufa',
    author_email='mustafasabuwala24@gmail.com',
    description='A simple greeting package',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)