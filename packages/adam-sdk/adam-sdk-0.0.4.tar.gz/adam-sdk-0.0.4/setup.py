from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='adam-sdk',
    version='0.0.4',
    packages=['adam_sdk', 'adam_sdk.Controllers', 'adam_sdk.Models'],
    url='https://github.com/Adam-Software/Adam-SDK',
    license='MIT',
    author='Adam Software',
    author_email='a@nesterof.com',
    description='SDK for robot Adam',
    long_description_content_type="text/markdown",
    long_description=long_description,
    install_requires=['servo-serial', 'feetech-servo-sdk', 'pymodbus'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.9'
    ]
)
