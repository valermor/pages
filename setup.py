from itertools import imap
from setuptools import setup, find_packages
import pages


def get_requirements():
    reqs_file = "requirements.txt"
    try:
        with open(reqs_file) as reqs_file:
            reqs = filter(None, imap(lambda line: line.strip(), reqs_file))
            return reqs
    except IOError:
        pass
    return []

setup(
    name='pages',
    version=pages.__version__,
    author='valerio morsella',
    author_email='valerio.morsella@skyscanner.net',
    packages=find_packages(exclude=["test*"]),
    description="Python library for easy creation of readable and reliable page objects for UI tests.",
    long_description=open('./README.md').read(),
    install_requires=get_requirements(),
    test_suite="test"
)
