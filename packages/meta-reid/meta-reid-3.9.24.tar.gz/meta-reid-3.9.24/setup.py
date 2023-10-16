from setuptools import setup, find_packages

requirements = [
    'opencv-python',
    'setuptools',
    'tensorrt',
    'pycuda',
    'numpy',
    'pillow',
    'tqdm',
    'faiss-gpu'
]

__version__ = 'V3.09.24'

setup(
    name='meta-reid',
    version=__version__,
    author='CachCheng',
    author_email='tkggpdc2007@163.com',
    url='https://github.com/CachCheng/cvreid',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    description='Meta Reid Toolkit',
    license='Apache-2.0',
    packages=find_packages(exclude=('docs', 'tests', 'scripts')),
    zip_safe=True,
    include_package_data=True,
    install_requires=requirements,
)
