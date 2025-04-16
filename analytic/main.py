#!/usr/bin/env python3
#!/usr/bin/env python

import datetime
import re
import sys
import time

import __os as os
import search
import images
import videos
import page
import facebook


def run_as_type():
    _type = os.environ.get("TYPE", "crawl")
    if _type == "crawl":
        page.crawl()
    elif _type == "images":
        images.crawl()
    elif _type == "search":
        search.crawl()
    elif _type == "videos":
        videos.crawl()
    elif _type == "facebook":
        facebook.crawl()
    else:
        page.crawl()


if __name__ == "__main__":
    run_as_type()
