from setuptools import find_packages, setup

setup(
    name='torch-model-sharding',
    version='1.0.0',
    keywords=['torch ', 'model', 'sharding'],
    install_requires=[
        'click==8.1.6',
        'torch==2.0.1',
        'tqdm==4.65.0',
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'torch-model-sharding=scripts.sharding:main'
        ]
    },
)
