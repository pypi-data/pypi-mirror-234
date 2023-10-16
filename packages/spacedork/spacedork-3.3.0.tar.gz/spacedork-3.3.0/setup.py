from setuptools import setup, find_packages
setup(
    name='spacedork',
    version="3.3.0",
    url='',
    description='',
    long_description='',
    keywords='dork search',
    author='',
    author_email='tongchengbin@outlook.com',
    maintainer='',
    platforms=['any'],
    license='',
    zip_safe=False,
    include_package_data=True,
    python_requires='>=3.6',
    packages=find_packages('.'),
    entry_points={
        "console_scripts": [
            "dork = spacedork.cli:main"
        ]
    },
    install_requires=[
        "httpx",
        "PyYAML",

    ],
)
