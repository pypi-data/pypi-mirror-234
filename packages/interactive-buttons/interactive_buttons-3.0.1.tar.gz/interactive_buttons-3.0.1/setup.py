from setuptools import setup, find_packages

setup(
    name="interactive_buttons",
    version="3.0.1",
    author="Mathys B",
    author_email="mathys.boyer@pro.mbinc.tech",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    # url="https://lien_vers_votre_projet.com",
    packages=find_packages(),
    install_requires=[
        "keyboard",
        "pynput==1.7.6"
    ]
)
