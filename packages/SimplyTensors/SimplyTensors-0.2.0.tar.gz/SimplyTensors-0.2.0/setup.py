from setuptools import setup, find_packages

setup(
    name='SimplyTensors',
    version='0.2.0',  # Update with your new version number
    description='Who needed Tensorflow anyway?',
    packages=find_packages(),
    install_requires=[
        "numpy"
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)

