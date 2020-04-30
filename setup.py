import setuptools

setuptools.setup(
    name="lof",
    version="0.0.0",
    author="refraction-ray",
    author_email="refraction-ray@protonmail.com",
    description="lof-bot",
    url="https://github.com/refraction-ray/lof-bot",
    # packages=setuptools.find_packages(),
    # include_package_data=True,
    install_requires=[
        "lxml",
        "pandas",
        "jinja2",
        "numpy",
        "requests",
        "xalpha==0.5.0",
        "pushbullet.py==0.11.0",
        "beautifulsoup4",
        "sqlalchemy",
    ],
    tests_require=["pytest"],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
