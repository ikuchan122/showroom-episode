# A. INTRODUCTION:
1. This is a python script to download showroom episodes.
2. Support: python3.8+ and pip3 
3. Dependencies: 'requests' and 'yt_dlp'
4. Extra dependency: If FFMPEG is not installed in your system, you may be prompted to do so when yt_dlp is going to be installed.

# B. INSTALLATION:
1. Python3 MUST BE pre-installed.
2. Unzip to the folder you’d like to save your downloads (e.g. the Home directory).
3. In your Terminal (Unix-like systme, such as, Mac OS and Linux) or CMD (Windows), enter the following command:

```
pip3 install requirements.txt
```


# C. USAGE:
1. Get the episode page url in correct format (e.g. https://www.showroom-live.com/episode/watch?id=14).
2. To download, enter the following command. Replace [URL] with the url above and without the squared brackets.

```
python3 showroom-episode.py [URL]
```
3. It will create a folder named 'showroom-output' (if not yet existed) in the same directory of the showroom-episode.py file. 
4. You will find the downloaded video file inside the folder. 