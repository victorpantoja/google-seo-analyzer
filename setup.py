# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from seo_analyzer import __version__ as Version

setup(
    name=u'google-seo-analyzer',
    version=Version,
    description=u"This simple script parses Google Web Master Tools report and analyzes results.",
    long_description=u'''
    When you are worried about your site SEO, you probably make many things to correct problems such as creating
    redirects, correcting broken URLs etc. But, it can take a long time to Google come back and see that you've
    done a good job.
    
    Fortunately, you yourself can mark desired URLs as corrected. But, if you have a large number of indexed URLs
    and make lots of simultaneous changes, it can be hard to keep track of those URLs.

    google-seo-analyzer helps you by crawling all problematic URLs and generating a report about which statuses
    have been changed and by ordering URLs in such a way you can easily identify error patterns.
    
    Usage: python crw.py path/to/file/ [debug|info|warning|error|critical]
    ''',
    keywords='gogole seo analyzer crawler report',
    author=u'Victor Pantoja',
    author_email='victor.pantoja@gmail.com',
    url='https://github.com/victorpantoja/google-seo-analyzer',
    license='MIT',
    classifiers=['Development Status :: 4 - Beta',
                 'Intended Audience :: Developers',
                 'Programming Language :: Python'],
    packages=find_packages(),
    package_dir={"seo_analyzer": "seo_analyzer"},
    include_package_data=True,
    scripts=['seo_analyzer/seo_analyzer.py'],

    install_requires=[
        "requests==1.2.3"
    ]
)
