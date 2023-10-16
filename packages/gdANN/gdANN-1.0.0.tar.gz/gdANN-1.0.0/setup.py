import setuptools

setuptools.setup(
    name="gdANN",
    version="1.0.0",
    author="Gordon_Shi",
    author_email="gordon2028261@concordiashanghai.org",
    description="contains artificial intelligence modules, activation functions and other useful stuff",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
# python setup.py sdist, twine upload dist/*, Gordon_Shi, chihin20100119
