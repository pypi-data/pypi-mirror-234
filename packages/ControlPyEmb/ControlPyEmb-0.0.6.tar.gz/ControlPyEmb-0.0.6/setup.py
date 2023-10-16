from setuptools import setup

setup(
    name='ControlPyEmb',
    version='0.0.6',
    description='This library provides implementations for control-based graph embedding methods and benchmarks',
    author='Anwar Said',
    author_email='<anwar.said@vanderbilt.edu>',
    packages=['ControlPyEmb'],
    install_requires=[
        # List any dependencies your package requires
        'networkx',
        'sphinx_rtd_theme',
        'controlpy'
    ],
    keywords = ['python','control','graph machine learning','graph embeddings'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering',
    ],
)
