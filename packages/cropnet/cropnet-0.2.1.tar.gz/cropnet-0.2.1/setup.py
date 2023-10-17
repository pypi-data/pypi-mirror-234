from setuptools import setup
from pathlib import Path

# read the contents of the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='cropnet',
    version='0.2.1',
    description='A Python package for the CropNet dataset',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Anonymous AI4Science',
    author_email='anonymous.ai4science@gmail.com',
    license='Free for non-commercial use',
    packages=['cropnet', 'cropnet.dataset', 'cropnet.utils'],
    install_requires=[
        'torch >= 1.13.0',
        'torchvision >= 0.14.0',
        'numpy >= 1.24.4',
        'pandas >= 2.0.3',
        'h5py >= 3.9.0',
        'Pillow >= 10.0.0',
        'einops >= 0.6.1',
        'scikit-learn >= 1.3.0',
        'matplotlib >= 3.7.2',
        'oauthlib >= 3.2.2',
        'requests-oauthlib >= 1.3.1',
        'geopandas >= 0.13.2',
        'shapely >= 2.0.1',
        'tqdm >= 4.65.0',
        'herbie-data >= 2023.3.0',
    ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: Free for non-commercial use',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
