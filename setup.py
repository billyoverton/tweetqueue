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

    author = "Billy Overton",
    author_email = "billy@billyoverton.com",
    description = "A command line tool for time-delaying your tweets.",
    license = "MIT License",
    keywords = "Twitter",
    url = "https://github.com/billyoverton/tweetqueue",

    entry_points='''
        [console_scripts]
        tweetqueue=tweetqueue.__main__:tweetqueue
    ''',
    classifiers= [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Utilities',
        'Topic :: Communications'
    ]
)
