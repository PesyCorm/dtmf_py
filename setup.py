from setuptools import find_packages, setup


setup(
    name="dtmf_py",
    version="1.0.0",
    description="DTMF (RFC2833) generator.",
    author="Noskov D.V.",
    author_email="pesycorm@yandex.ru",
    packages=find_packages(),
    install_requires=[
        "rtp"
    ]
)
