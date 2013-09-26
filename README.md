# rhythmbox_playlist_to_m3u

## Description

This script converts playlists stored by Rhythmbox to M3U files.

It reads information from ~/.local/share/rhythmbox/playlists.xml and converts every 'static' playlist into a M3U file. If the new playlists are the same as existing M3U files, they don't replace them.

This program has been written in September 2013 and works well with Rhythmbox 2.99.1.

## Usage

```./rhythmbox_playlist_to_m3u.py [-i /path/to/playlist.xml] /path/to/output/dir
```

Rhythmbox playlist will be read from `/path/to/playlist.xml` (default `~/.local/share/rhythmbox/playlists.xml`) and saved in the `/path/to/output/dir` directory, in M3U format.
