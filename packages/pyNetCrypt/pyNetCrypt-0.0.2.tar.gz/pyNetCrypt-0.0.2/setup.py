import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

docs_extras = [
    'Sphinx >= 3.0.0',  # Force RTD to use >= 3.0.0
    'docutils',
    'pylons-sphinx-themes >= 1.0.8',  # Ethical Ads
    'pylons_sphinx_latesturl',
    'repoze.sphinx.autointerface',
    'sphinx-copybutton',
    'sphinxcontrib-autoprogram',
]

setuptools.setup(
    name="pyNetCrypt",
    version="0.0.2",
    author="ALIASGAR - ALI",
    author_email="aholo2000@gmail.com",
    description="Networking Device MD5 Password Encrypt/Decrypt utility",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aliasgar1978/pyNetCrypt",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires= [],
    # extras_require={'docs': docs_extras},
)

