from setuptools import setup, find_packages

setup(
    name='SimplyTensors',
    version='0.4.0',
    packages=find_packages(),
    install_requires=[
        "numpy"
    ],
    description='A lightweight alternative to Tensorflow',
    long_description='What am i even meant to write here? Its kinda obvious what this is',
    long_description_content_type='text/markdown',
    license='MIT',  # Adjust as necessary
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)

