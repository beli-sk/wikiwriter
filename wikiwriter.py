#!/usr/bin/env python
#
# WikiWriter - Store page on compliant wiki using XML-RPC API
# Copyright (C) 2016 Michal Belica <devel@beli.sk>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import print_function

import os
import sys
import argparse
from datetime import datetime

from dokuwiki import DokuWiki, DokuWikiError


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--login')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-p', '--password', help='Provide password as argument')
    group.add_argument('-P', '--pass-fd', dest='passfd', type=int, help='File descriptor number to read password from')
    parser.add_argument('-f', '--file', help='File path to read content from (default: stdin)')
    parser.add_argument('-m', '--message', help='Description of the update')
    parser.add_argument('url', help='Wiki URL')
    parser.add_argument('page', help='Page ID')
    args = parser.parse_args()
    
    if args.passfd is not None:
        with os.fdopen(args.passfd) as f:
            password = f.read().strip()
    elif args.password:
        password = args.password
    else:
        password = None

    if args.file:
        with open(args.file, 'r') as f:
            content = f.read()
    else:
        content = sys.stdin.read()
        
    options = []
    if args.login and password:
        options.append(args.login)
        options.append(password)

    wiki = DokuWiki(args.url, *options)

    options = {}
    if args.message:
        options['message'] = args.message

    if not wiki.pages.set(args.page, content, **options):
        return 1
    else:
        return 0

if __name__ == '__main__':
    sys.exit(main())
