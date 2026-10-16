#!/bin/sh
# Download a Google Drive file (any size) into a folder.
# Usage: sh fetch_drive.sh "<drive link or file id>" <dest-dir> [name]
# Needs drive.google.com + drive.usercontent.google.com in the environment's Allowed domains.
set -e
id=$(printf '%s' "$1" | sed -E 's#.*/d/([^/?]+).*#\1#; s#.*[?&]id=([^&]+).*#\1#')
dest=${2:-$HOME/Downloads}; mkdir -p "$dest"
name=${3:-$id}
tmp="$dest/.$name.part"
curl -fsSL -o "$tmp" "https://drive.usercontent.google.com/download?id=$id&export=download&confirm=t"
ext=$(ffprobe -v error -show_entries format=format_name -of default=nw=1:nk=1 "$tmp" 2>/dev/null | cut -d, -f1)
case "$ext" in mov) ext=mp4 ;; "") echo "not a video (check sharing is 'anyone with the link')" >&2; exit 1 ;; esac
mv "$tmp" "$dest/$name.$ext"
echo "$dest/$name.$ext"
