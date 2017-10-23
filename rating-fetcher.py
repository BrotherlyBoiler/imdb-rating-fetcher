'''
    Search through a target movies directory and filter movie titles
    to search IMDb for movie ratings. After fetching, append ratings
    to corresponding movie files/folders in the directory.

    File names initially could be in one of the following formats:
    1. P.S. I Love You (7.1).mkv
    2. P.S. I Love You (2010).mp4
    3. P.S. I Love You (2010) [1080p].avi

    The IMDb rating for the movie is fetched from omdbapi.com and added to
    the end of the file name (just before the extension).

    The above file would be renamed to one of the following:
    1. [IMDb 7.1] P.S. I Love You.mkv
    2. [IMDb 7.1] P.S. I Love You (2010).mp4
    3. [IMDb 7.1] P.S. I Love You (2010) [1080p].avi
'''

import os
import json
import urllib.request
import re

# Query related constants
base_uri = "http://www.omdbapi.com/?apikey=e83526a2&"
query_title = "t="

basepath = os.path.dirname(os.path.realpath(__file__))


def getMovieRating(movie_title):
    """ Fetch movie rating from omdbapi.com. API return JSON format. """
    # format movie name with spaces for query to server
    movie_title = movie_title.strip().replace(" ", "+")

    with urllib.request.urlopen(base_uri + query_title + movie_title) as url:
        data = json.loads(url.read().decode())    # decode to utf-8

    if 'imdbRating' not in data:
        print("Invalid server response for " + movie_title)
        return None

    # Make sure server response matches intended regex
    regex = re.compile('[0-9].[0-9]')
    if regex.match(data['imdbRating']) is None:
        return None

    return data['imdbRating']


def hasNewRating(filename):
    """
    Checks if parameter file name already has a rating.
    Movie ratings are in the format (\d.\d)
    """
    pattern = re.compile('\[IMDb [0-9].[0-9]\]')
    return pattern.search(filename) is not None


def hasOldRating(filename):
    pattern = re.compile('\([0-9].[0-9]\)')
    return pattern.search(filename) is not None


def removeOldRating(filename):
    index = filename.find('(')
    new_filename = filename.replace(filename[index - 1:index + 5], "")
    os.rename(os.path.join(filename), os.path.join(new_filename))
    return new_filename


def getMovieTitle(filename):
    """
    Get the movie title by stripping out excess information such as the
    year released or video definition
    """
    if '(' in filename:
        return filename.split('(')[0]
    elif '[' in filename:
        return filename.split('[')[0]

    return ''.join(os.path.splitext(filename)[0])


if __name__ == '__main__':
    renamed = 0

    print("Working...")
    # try to find rating for each title in the directory
    for filename in os.listdir(basepath):

        # ignore hidden files
        if filename[0] is '.' or filename == __file__:
            continue

        # ignore files that already have a rating
        if hasNewRating(filename):
            continue

        # ignore this python file
        if filename == __file__:
            continue

        movie_title = getMovieTitle(filename)
        movie_rating = getMovieRating(movie_title)

        # Continue if no rating is found
        if (movie_rating is None):
            continue
        if hasOldRating(filename):
            filename = removeOldRating(filename)

        formatted_rating = '[IMDb ' + movie_rating + '] '
        file_no_ext, file_ext = os.path.splitext(filename)
        new_file_name = formatted_rating + file_no_ext + file_ext

        os.rename(os.path.join(filename), os.path.join(new_file_name))

        print(filename + " -> " + new_filename)

        renamed += 1

    print("    Total: " + str(len(os.listdir('.')) - 1))
    print("  Renamed: " + str(renamed))
