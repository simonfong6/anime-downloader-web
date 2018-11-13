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


@app.route('/')
def index():
    return redirect(url_for(
            'get_static_files',
            file_type=app.config['html'],
            file_name='index.html'))

@app.route('/download', methods=['GET', 'POST'])
def download():
    anime = NineAnime(
            'https://www1.9anime.to/watch/your-name-dub.l4yz/n2qm6m',
            quality='720p')
    print(anime.title)

    for ep in anime:
        print(ep.ep_no) # int: Episode number of the episode
        print(ep.pretty_title)  # str: title in the format <animename>-<ep_no>
        print(ep.quality)
        print(ep.stream_url)  # stream url for the epiosde.
        print(ep.title)  # title from site. Most probably giberrish

    ep = anime[0]
    print(dir(ep))
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
