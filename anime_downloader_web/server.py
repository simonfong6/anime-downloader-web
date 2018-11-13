#!/usr/bin/env python3
"""
server.py

Main server file to allow access to anime-downloader package.
"""
import os
import json
import logging
from flask import Flask, request, send_from_directory, redirect, url_for
from anime_downloader import get_anime_class

app = Flask(__name__)

AnimeClass = get_anime_class('9anime')

EXCLUDED_FILE_CHARS = '/\\:*?"<>| '
EXT_MP4 = '.mp4'


def initiliaze():
    """
    Ran before the server starts.
    """
    app.config['STATIC'] = 'static'
    app.config['html'] = 'html'
    app.config['css'] = 'css'
    app.config['js'] = 'js'
    app.config['video'] = 'video'


def clean_file_name(file_name):
    """
    Removes all the characters not allowed in file names from file name.
    """
    file_name_cleaned = file_name
    for c in EXCLUDED_FILE_CHARS:
        file_name_cleaned = file_name_cleaned.replace(c, '_')
    return file_name_cleaned


def create_mp4_file_name(video_title):
    """
    Creates a mp4 file name from video title.
    """
    file_name_cleaned = clean_file_name(video_title)
    file_name_mp4 = file_name_cleaned + EXT_MP4
    return file_name_mp4


def create_mp4_file_path(video_title):
    file_name_mp4 = create_mp4_file_name(video_title)
    file_path_mp4 = os.path.join(
                        app.config['STATIC'],
                        app.config['video'],
                        file_name_mp4)
    return file_path_mp4


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


@app.route('/download', methods=['POST'])
def download():
    """
    Downloads the given anime episode and redirects to the url.
    """
    form = request.form
    anime_url = form['anime_url']
    episode_num = int(form['episode_num'])
    quality = form['quality']

    message = (
        "Anime URL: {anime_url}\n"
        "Episode Number: {episode_num}\n"
        "Quality: {quality}".format(
            anime_url=anime_url,
            episode_num=episode_num,
            quality=quality)
    )
    logging.info(message)

    anime = AnimeClass(
            anime_url,
            quality=quality)

    episode_index = episode_num - 1

    # Download the specified episode.
    episode = anime[episode_index]

    episode_file_name = create_mp4_file_name(episode.pretty_title)
    episode_path = create_mp4_file_path(episode.pretty_title)

    logging.info("Downloading {} ...".format(episode_path))

    episode.download(path=episode_path) 
    return redirect(url_for(
                        'show_anime',
                        anime_title=episode_file_name))


@app.route('/anime/<anime_title>')
def show_anime(anime_title):
    return redirect(url_for(
                        'get_static_files',
                        file_type='video',
                        file_name=anime_title))


def main(args):
    initiliaze()
    logging.basicConfig(
                filename='server.log',
                level=logging.DEBUG)
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
