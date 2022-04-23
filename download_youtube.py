from yt_dlp import YoutubeDL
from youtube_search import YoutubeSearch

MAX_SONG_DURATION = 900

OUTPUT_TEMPLATE = 'out.webm'

YDL_SEARCH_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}

YDL_DOWNLOAD_OPTIONS = {
    'outtmpl': 'out.webm',
    'format': 'bestaudio/best',
    # ffmpeg is required. Files could be broken on Windows.
    # 'postprocessors': [{
    #    'key': 'FFmpegExtractAudio',
    #    'preferredcodec': 'mp3',
    #    'preferredquality': '192',
    # }],
}


def search_yt(arg: str, max_duration: int = MAX_SONG_DURATION) -> any:
    """
    Search youtube for media.
    @param arg: music search string
    @param max_duration: max duration of the media
    """
    video = []
    with YoutubeDL(YDL_SEARCH_OPTIONS) as ydl:
        results = YoutubeSearch(arg, max_results=4).to_dict()
        for result in results:
            link = f"https://youtube.com{result['url_suffix']}"
            video = ydl.extract_info(link, download=False)
            if video['duration'] < max_duration:
                break
    return video


def download_yt(url: str) -> None:
    """
    Downloads media by the url and saves to OUTPUT_TEMPLATE path.
    @param url: url
    """
    with YoutubeDL(YDL_DOWNLOAD_OPTIONS) as ydl:
        ydl.download([url])
