from setuptools import setup

setup(
    name='GuardPyCaptcha',
    version='0.1.0',
    packages=['GuardPyCaptcha'],
    install_requires=[
        'opencv-python',
        'keyring',
        'cryptography',
        'numpy',
    ],
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
