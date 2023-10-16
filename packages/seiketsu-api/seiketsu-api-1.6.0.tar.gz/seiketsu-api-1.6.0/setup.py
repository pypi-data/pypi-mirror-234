
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='seiketsu-api',
    long_description=long_description,
    long_description_content_type="text/markdown",
    version='1.6.0',
    description='A Python library to interact with a chat API',
    author='LoLip_p',
    author_email='mr.timon51@gmail.com',
    url='https://github.com/yourusername/my-json-package',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "api_seiketsu": ["data/*.json"],
    },
    install_requires=[
        "google-cloud-firestore>=2.11.1",
        "google-auth>=2.22.0",
        "google-auth-httplib2>=0.1.0",
    ],
)
