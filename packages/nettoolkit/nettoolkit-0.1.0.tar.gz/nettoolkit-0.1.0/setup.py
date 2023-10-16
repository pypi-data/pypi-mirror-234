import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nettoolkit",
    version="0.1.0",
    author="ALIASGAR - ALI",
    author_email="aholo2000@gmail.com",
    description="Tool Set for Networking Geeks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alias1978/nettoolkit",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=['pandas', 'openpyxl', 'PySimpleGUI', 
        'nettoolkit_common', 'nettoolkit_db', 'pyNetCrypt', 'pyJuniper',
        'facts-finder', 'capture-it', 'j2config'
    ]
)

