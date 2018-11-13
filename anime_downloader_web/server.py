#!/usr/bin/env python3
"""
server.py

Main server file to allow access to anime-downloader package.
"""
import os
import json
from flask import Flask, request, send_from_directory, redirect, url_for
from anime_downloader import get_anime_class

app = Flask(__name__)

AnimeClass = None

EXCLUDED_FILE_CHARS = '/\\:*?"<>| '


def initiliaze():
    """
    Ran before the server starts.
    """
    AnimeClass = get_anime_class('9anime')
    app.config['STATIC'] = 'static'
    app.config['html'] = 'html'
    app.config['css'] = 'css'
    app.config['js'] = 'js'
    app.config['video'] = 'video'


def clean_file_name(file_name):
    """
    Removes all the characters not allowed in file names from file name.
    """
    file_name_cleaned = None
    for c in EXCLUDED_FILE_CHARS:
        file_name_cleaned = file_name.replace(c, '_')
    return file_name_cleaned


@app.route('/')
def index():
    """
    Serves main page.
    """
    return redirect(url_for(
            'get_static_files',
            file_type=app.config['html'],
            file_name='index.html'))


@app.route('/static/<file_type>/<file_name>')
def get_static_files(file_type, file_name):
    """
    Serves any static resources.
    """
    dir_path = os.path.join(app.config['STATIC'], app.config[file_type])
    return send_from_directory(dir_path, file_name)


@app.route('/download', methods=['GET', 'POST'])
def download():
    anime_url = 'https://www1.9anime.to/watch/code-geass-lelouch-of-the-rebellion-dub.k3w/k4nnxv'
    quality = '720p'
    anime = AnimeClass(
            anime_url,
            quality=quality)
    print(anime.title)

    for ep in anime:
        print(ep.ep_no) # int: Episode number of the episode
        print(ep.pretty_title)  # str: title in the format <animename>-<ep_no>
        print(ep.quality)
        print(ep.stream_url)  # stream url for the epiosde.
        print(ep.title)  # title from site. Most probably giberrish

    # Download the first episode.
    ep = anime[0]

    ep.download()  # downloads the episode
    return "Download"


@app.route('/anime/<anime_title>')
def show_anime():
    pass


def main(args):
    initiliaze()
    app.run(
        host='0.0.0.0',
        port=args.port,
        threaded=False,
        debug=args.debug)


if(__name__ == "__main__"):
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port',
                        help="Port that the server will listen on.",
                        type=int, default=8080)
    parser.add_argument('-d', '--debug',
                        help="Whether or not to run in debug mode.",
                        default=False, action='store_true')

    args = parser.parse_args()
    main(args)
