google-seo-analyzer
===================

This simple script parses Google Web Master Tools report and analyzes results.

When you are worried about your site SEO, you probably make many things to correct problems such as creating
redirects, correcting broken URLs etc. But, it can take a long time to Google come back and see that you've
done a good job.

Fortunately, you yourself can mark desired URLs as corrected. But, if you have a large number of indexed URLs
and make lots of simultaneous changes, it can be hard to keep track of those URLs.

google-seo-analyzer helps you by crawling all problematic URLs and generating a report about which statuses
have been changed and by ordering URLs in such a way you can easily identify error patterns.

Usage: seo_analyzer.py path/to/file/ [debug|info|warning|error|critical]
