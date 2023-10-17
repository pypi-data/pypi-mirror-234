from setuptools import setup

setup(
    name='jls_utils',
    version='0.1.35',
    author="Andrew Pogrebnoj",
    author_email="andrew2000203@gmail.com",
    package_dir={"jls_utils": "jls_utils"},
    install_requires=[
        'requests',
        'pydantic',
        'typing',
        'pandas',
        'deprecation',
        'aiohttp'
    ]
)
