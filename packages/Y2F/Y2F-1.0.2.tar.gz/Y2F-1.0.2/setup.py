from setuptools import setup, find_packages

setup(
    name='Y2F',
    version='1.0.2',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'Y2F=Y2F_PACKAGE.main:main',
        ]
    },
    description = 'Command line utility for downloading YouTube videos in MP3 or MP4 format.',
    author_email = 'teodormihail07@gmail.com',
    url = 'https://github.com/CSharpTeoMan911/Y2F', 
    install_requires=[
        'pytube'
    ]
)
