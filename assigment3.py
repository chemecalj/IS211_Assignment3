#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""IS 211 Week 3"""

import csv
import argparse
import urllib2
import re

print ("Enter a URL that links to a CSV.")

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--url', help="Enter a URL to a valid .csv file.")
args = parser.parse_args()


def download_Data(url):
    """Opens a URL link.
    Args:
        url(str): A string for a URL.
    Returns:
        data_file(assorted): A variable linked to a datafile found in
        the URL.
    Example:
        >>> downloadData('http://s3.amazonaws.com/cuny-is211-spring2015
        /weblog.csv')
    """
    data_file = urllib2.urlopen(url)
    return data_file


def process_Data(data_file):
    """Processes a the URL of a .csv file.
    Args:
        data_file(file): A .csv file imported through a URL from a user.
    Returns:
        msg(str): A string which has the number of page hits,
        percent of image requests, browser with the highest number of hits, and
        the amount of hits that browser had.
    Example:
        >>> load = downloadData('http://s3.amazonaws.com/cuny-is211-spring2015
        /weblog.csv')
        >>> processData(load)
        There were 10000 page hits today.
        Image requests account for 78.77% of hits.
        Google Chrome has the most hits with 4042.
    """

    read_file = csv.reader(data_file)
    line_count = 0
    img_count = 0

    chrome = ['Google Chrome', 0]
    ie = ['Internet Explorer', 0]
    safari = ['Safari', 0]
    fox = ['Firefox', 0]
    for line in read_file:
        line_count += 1
        if re.search("firefox", line[2], re.I):
            fox[1] += 1
        elif re.search(r"MSIE", line[2]):
            ie[1] += 1
        elif re.search(r"Chrome", line[2]):
            chrome[1] += 1
        elif re.search(r"Safari", line[2]) and not re.search("Chrome", line[2]):
            safari[1] += 1
        if re.search(r"jpe?g|JPE?G|png|PNG|gif|GIF", line[0]):
            img_count += 1

    img_hit_pct = (float(img_count) / line_count) * 100

    browser_count = [chrome, ie, safari, fox]

    high_browser = 0
    top_brow = ' '
    for b in browser_count:
        if b[1] > high_browser:
            high_browser = b[1]
            top_brow = b[0]
        else:
            continue

    msg = ('There were {} page hits today.'
           '\nImage requests account for {}% of '
           'hits. \n{} has the most hits at {}.').format(line_count,
                                                           img_hit_pct,
                                                           top_brow,
                                                           high_browser)
    print msg


def main():
    """Combines download_Data and process_Data into one script to be run
    on the command line."""
    if not args.url:
        raise SystemExit
    try:
        data = download_Data(args.url)
    except urllib2.URLError:
        print 'Please enter a valid URL.'
        raise
    else:
        process_Data(data)

if __name__ == '__main__':
    main()
