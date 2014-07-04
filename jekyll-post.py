#!/usr/bin/python

"""
This Software is derived from Josh Branchaud's work (https://github.com/jbranchaud/mybin).
Hereby is the copy of the license.

---------------------------------------------------------------------------------
Copyright (c) 2014 Josh Branchaud

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
---------------------------------------------------------------------------------

jekyll-post.py - this is a simple script that will create and initialize a new
Jekyll post file in markdown format (.md). The yaml options listed below will be 
part of the initialization.

jekyll-post [-c] [-D directory] [-d date] [-n name] [title]

title   the title of the post wrapped in quotes, e.g. "post title here"
-D      the directory (relative or absolute) that the file should be written to.
-d      the default date is today's date or this option can be used to specify
        a date. The date must be specified in the format YYYY-MM-DD.
-n      the name for the post file instead of using the automatically generated one.
-c      this optional flag to enable comments.

File output "YYYY-MM-DD-some-post-title.md":
---
layout: post
title: [title]
feature_image: '[path>]'
disqus_comments: true/false
---
"""

import argparse, datetime, os.path, sys

DEFAULT_EXT = 'md'

def main():
    # parse the arguments
    parser = argparse.ArgumentParser(description='Create a new Jekyll post.')
    parser.add_argument('title',
                        help='the title of the post wrapped in quotes.')

    parser.add_argument('-D', '--Dir',
                        help='specify the directory (relative or absolute) where the file should be written to.')

    parser.add_argument('-d', '--date',
                        help='specify the post date in the format YYYY-MM-DD, otherwise today is the default date.')

    parser.add_argument('-n', '--name',
                        help='specify the name of the post file instead of the automatically generated one. It is a best practice for the words to be separated by hyphens. Also note that the given name will be prepended with the date so as to conform to Jekyll naming requirements.')

    parser.add_argument('-c', '--comment', action='store_true',
                        help='specify if comments should be set to true. False by default.')

    args = parser.parse_args()

    title = retrieve_dash_title(args.title, args.name)
    if not title:
        print '[Error] No title could be created.'
        print 'Jekyll post NOT created.'
        sys.exit(1)

    post_title = args.title
    date = retrieve_date(args.date)

    #filename = '%s-%s.%s', date, title, DEFAULT_EXT
    filename = date + '-' + title + '.' + DEFAULT_EXT

    # if Dir is specified, append to front of filename
    if args.Dir:
        filename = args.Dir + '/' + filename

    # check if the desired file already exists
    if os.path.exists(filename):
        # file already exists, abort the program
        print '[Error] ' + filename + ' already exists.'
        print 'Jekyll post NOT created.'
        sys.exit(1)

    # try writing yaml to the post file
    try:
        f = open(filename, 'w')

        # write yaml to file
        try:
            f.write('---\n')
            f.write('layout: post\n')
            f.write('title: ' + post_title + '\n')
            f.write('published: false\n')
            f.write('#feature_image: \'\'\n')

            comment = 'false'
            if args.comment: 
                comment = 'true'
            f.write('disqus_comments: '+ comment +'\n')

            f.write('---\n\n\n')
        finally:
            f.close()
    except IOError:
        print '[Error] Issue writing to Jekyll post file.'

    # print confirmation statement
    print '[Success] New Jekyll post "' + title + '" has been created -- ' + filename



# ARGUMENT HELPER FUNCTIONS
###############################

def retrieve_dash_title(title_arg, name_arg):
    # exchange spaces for dashes
    dash_title = ''
    if name_arg:
        dash_title = name_arg.replace(' ','-')
    elif title_arg:
        dash_title = title_arg.replace(' ','-')
    else:
        return None

    # clean up any special characters from the dash-title
    title = ''
    for char in dash_title:
        if char.isalnum() or char == '-':
            title += char

    return title

def retrieve_date(date_arg):
    date = None
    if date_arg:
        date = date_arg
    else:
        # use today's date
        today = datetime.datetime.now()
        year = str(today.year)
        month = str(today.month)
        if len(month) == 1:
            month = '0' + month
        #month = today.month > 9 ? str(today.month) : '0' + str(today.month)
        day = str(today.day)
        if len(day) == 1:
            day = '0' + day
        #day = today.day > 9 ? str(today.day) : '0' + str(today.day)
        date = "-".join([year,month,day])
    return date


if __name__ == '__main__':
    main()