import re

from re import Pattern


#: Regex object to validate if an string is an valid YouTube URL.
valid: Pattern = re.compile(r'^(?:https?://)?(?:www\.)?(?:youtube\.com/(watch\?v=|playlist\?list=)|youtu\.be/)([^&]{11})')

#: Regex object to verify if the string is a YouTube playlist URL.
playlist: Pattern = re.compile(r'^(?:https?://)?(?:www\.)?(?:youtube\.com/playlist\?list=|youtu\.be/)([^&]{11})')

#: Regex object to verify if the string has an valid video id.
playlist_id: Pattern = re.compile(r'playlist\?list=([^&]{34})')

#: Regex object to verify if the string is a YouTube video URL.
video: Pattern = re.compile(r'^(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([^&]{11})')

#: Regex object to verify if the string has an valid video id.
video_id: Pattern = re.compile(r'watch\?v=([^&]{11})')
