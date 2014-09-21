from setuptools import setup, find_packages

setup(
    name='tweetqueue',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click>=3.3',
        'tweepy>=2.3.0',
    ],
    entry_points='''
        [console_scripts]
        tweetqueue=tweetqueue.__main__:tweetqueue
    ''',
)
