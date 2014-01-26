#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2013 Adrien Vergé

"""This script converts playlists stored by Rhythmbox to M3U files.

It reads information from ~/.local/share/rhythmbox/playlists.xml and converts
every 'static' playlist into a M3U file. If the new playlists are the same as
existing M3U files, they don't replace them.

This program has been written in September 2013 and works well with
Rhythmbox 2.99.1.

"""

__author__ = "Adrien Vergé"
__copyright__ = "Copyright 2013, Adrien Vergé"
__license__ = "GPL"
__version__ = "1.0"

import argparse
import filecmp
import os
import shutil
import sys
import urllib.parse
import xml.etree.ElementTree

if sys.version_info < (3, 0):
	raise Exception("This script is made for Python 3.0 or higher")

def save_playlist(playlist, filename):
	f = open(filename, 'w')
	f.write('#EXTM3U\n')
	for song in playlist:
		if song.tag == 'location':
			if song.text[0:18] == 'file:///docs/music':
				songfile = '..'+song.text[18:]
				songfile = urllib.parse.unquote(songfile)
				f.write(songfile+'\n')
			else:
				print('WARNING: unexpected path')
		else:
			print('WARNING: unexpected tag')
	f.close()

def main():
	"""This is the entry point of the script."""

	def_pl = '.local/share/rhythmbox/playlists.xml'
	if 'HOME' in os.environ:
		def_pl = os.environ['HOME']+'/'+def_pl
	# Parse arguments
	parser = argparse.ArgumentParser(
		description='Converts playlists stored by Rhythmbox to M3U files.')
	parser.add_argument('o', metavar='/path/to/output/dir',
						help='output directory to save M3U playlists')
	parser.add_argument('-i', metavar='/path/to/playlist.xml',
						default=def_pl,
						help='Rhythmbox playlist file, in XML format')
	args = parser.parse_args()

	infile = args.i
	outdir = args.o # '/docs/music/__playlists'
	tmpdir = '/tmp'

	tree = xml.etree.ElementTree.parse(infile)
	root = tree.getroot()

	donesomething = False

	for child in root:
		if child.attrib['type'] == 'static':
			filename = child.attrib['name']+'.m3u'
			save_playlist(child, tmpdir+'/'+filename)
			if os.path.exists(outdir+'/'+filename) and \
			   filecmp.cmp(tmpdir+'/'+filename, outdir+'/'+filename):
				# The playlist has not changed
				os.remove(tmpdir+'/'+filename)
			else:
				# Move to overwrite previous playlist
				shutil.move(tmpdir+'/'+filename, outdir+'/'+filename)
				print('Saving new "%s"' % filename)
				donesomething = True

	if not donesomething:
		print('No modification made')

if __name__ == "__main__":
	main()

