from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import urllib.parse as up

def video_id(url):

    query = up.urlparse(url)
    if query.hostname == 'youtu.be':
        video_id = query.path[1:]
        return video_id
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = up.parse_qs(query.query)
            video_id = p['v'][0]
            return video_id
        if query.path[:7] == '/embed/':
            video_id = query.path.split('/')[2]
            return video_id
        if query.path[:3] == '/v/':
            video_id = query.path.split('/')[2]
            return video_id

    return None

def youtube_to_text(url):

    id = video_id(url)

    transcript = YouTubeTranscriptApi.get_transcript(id)

    formatter = TextFormatter()

    text_formatted = formatter.format_transcript(transcript)

    text_formatted = text_formatted.replace("\n", " ")

    return text_formatted
