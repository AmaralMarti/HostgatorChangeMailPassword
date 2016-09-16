#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import cgi

def get_domains():
    etc_path = os.path.expanduser('~/etc/')
    os.chdir(etc_path)

    domains = []

    for dir in os.listdir(etc_path):
    	if os.path.isdir(dir):
        	domains.append(dir)

    return domains


if __name__ == "__main__":
    print "Content-Type: text/html\n\n"

    domains = get_domains()

    for domain in domains:
        print domain
