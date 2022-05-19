import requests
import sys
from textwrap import dedent
from urllib.parse import urlparse
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError
# from os import system

# Toggle debug mode
isDebug = False

# Global variables
COOKIE = ''
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15'

HEADERS = {
    'User-Agent': user_agent,
}


def isValidUrl(episode_url: str) -> bool:
    if not 'https' in episode_url:
        print('Invalid url')
        return False
    if not 'showroom-live.com' in episode_url:
        print('Invalid url [not showroom-live.com]')
        return False
    if not 'episode' in episode_url:
        print('Invalid url [not showroom episode]')
        return False
    if not 'watch' in episode_url:
        print('Invalid url [not showroom episode]')
        return False
    query = urlparse(episode_url).query
    if not 'id=' in query:
        print('Invalid url [invalid query string]')
        return False
    return True


def getEpisodeTitle(episode_url: str) -> str or None:
    try:
        resp = requests.get(episode_url, headers=HEADERS)
        if resp.status_code != 200:
            raise Exception('status_code not 200')
        html = resp.text
        a = html.find('<title>')
        b = html.find('</title>')
        title = html[a+7:b].strip()
        print('title: ' + title)
        return title
    except Exception as e:
        print('Failed to get showroom episode html.')
        return None


def getEpisodeId(episode_url: str) -> str or None:
    query = urlparse(episode_url).query.strip()
    episode_id = query.split('id=')[1].split('&')[0]
    if not episode_id:
        print('Invalid url [empty episode id]')
        return None
    return episode_id


def getStreamingUrl(episode_id: str) -> str:
    streaming_url = f'https://www.showroom-live.com/api/episode/streaming_url?episode_id={episode_id}'
    print('streaming_url: ' + streaming_url)
    return streaming_url


def cookieParser(raw_cookie: str) -> str:
    output = []
    cookie_arr = raw_cookie.split('; ')
    for item in cookie_arr:
        if 'CloudFront' in item:
            output.append(item.split(', ')[1])
    cookie = '; '.join(output)
    return cookie


def getChunkList(streaming_url: str) -> str or None:
    try:
        global COOKIE
        resp = requests.get(streaming_url, headers=HEADERS)
        COOKIE = cookieParser(resp.headers['Set-Cookie'])
        chunklist_url = resp.json()['streaming_url_list']['hls_source']['hls']
        print('chunklist_url: ' + chunklist_url)
        return chunklist_url
    except Exception as e:
        print('Failed to GET chunklist_url.')
        return None


def download(chunklist_url: str, title: str):
    ''' old ver. uses bash command'''
    # command = f"yt-dlp --add-header 'Cookie: {COOKIE}' --add-header 'User-Agent: {user_agent}' {chunklist_url} -o '{title}'.mp4"
    # if isDebug:
    #     print()
    #     print(command)
    #     print()
    # system(command)

    ''' new ver. uses the yt_dlp python module'''
    ydl_opts = {
        'http_headers': {
            'Cookie': COOKIE,
            'User-Agent': user_agent,
        },
        'paths': {
            'home': 'showroom-output'
        },
        'outtmpl': title + '.%(ext)s'
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            error_code = ydl.download(chunklist_url)
            if isDebug:
                print(f'\nerror_code: {str(error_code)}\n')
            if error_code == 0:
                return True
    except DownloadError as e:
        return False

# main function


def main():
    '''
    [USAGE]
    To download an episode on https://www.showroom-live.com/episode,
    input the below commands into your Mac OS Terminal or Windows CMD.

    python3 showroom-episode.py [url]
    '''

    # Check cli arguments
    if len(sys.argv) < 2:
        return print(dedent(main.__doc__))

    arg = sys.argv[1]
    if arg == '--help' or arg == '-H':
        return print(dedent(main.__doc__))

    # Validate input url
    episode_url = str(arg)
    if not isValidUrl(episode_url):
        return print(dedent(main.__doc__))

    print('\nFetching episode info...')
    title = getEpisodeTitle(episode_url)
    if not title:
        return print(dedent(main.__doc__))

    episode_id = getEpisodeId(episode_url)
    if not episode_id:
        return print(dedent(main.__doc__))

    streaming_url = getStreamingUrl(episode_id)

    print('\nParsing m3u8 playlist data...')
    chunklist_url = getChunkList(streaming_url)
    if not chunklist_url:
        return print(dedent(main.__doc__))

    print('\nDownload begins...')
    isSuccess = download(chunklist_url=chunklist_url, title=title)
    if isSuccess:
        print('\nDownload completed.\n')
    else:
        print('\nDownload failed. Check error message.\n')


if __name__ == '__main__':
    main()
