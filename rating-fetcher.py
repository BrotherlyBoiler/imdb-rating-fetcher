'''
    Search through a target movies directory and filter movie titles
    to search IMDb for movie ratings. After fetching, append ratings
    to corresponding movie files/folders in the directory.

    File names are in one of the following formats:
    1. P.S. I Love You (7.1).mkv
    2. P.S. I Love You (2010).mp4
    3. P.S. I Love You (2010) [1080p].avi

    Ideally, this program fetched the movie ratings and adds it to
    the end of the file name (just before the extension). The query,
    in this case, would be http://www.omdbapi.com/?t=P.S.+I+Love+You

    Ideally, the file in the directory would be renamed to one of
    the following:
    1. [IMDb 7.1] P.S. I Love You.mkv
    2. [IMDb 7.1] P.S. I Love You (2010).mp4
    3. [IMDb 7.1] P.S. I Love You (2010) [1080p].avi
'''

import os, json, urllib.request, re

# Query related constants
base_uri = "http://www.omdbapi.com/?"
query_title = "t="

basepath = os.path.dirname(os.path.realpath(__file__))

# Fetch movie rating from omdbapi.com. API return JSON format.
def getMovieRating(movie_title):
    movie_title = movie_title.strip().replace(" ", "+")
    with urllib.request.urlopen(base_uri + query_title + movie_title) as url:
        data = json.loads(url.read().decode())    # decode to utf-8
    if 'imdbRating' not in data:
        print ("Invalid response for " + movie_title)
        return None
    # Make sure server response matches intended regex
    pattern = re.compile('\d\.\d')
    if pattern.match(data['imdbRating']) is None:
        return None
    return data['imdbRating']

# Checks if parameter file name already has a rating.
# Movie ratings are in the format (\d.\d)
def hasNewRating(filename):
    pattern = re.compile('\[IMDb \d\.\d\]')
    return pattern.search(filename) is not None

def hasOldRating(filename):
    pattern = re.compile('\(\d\.\d\)')
    return pattern.search(filename) is not None

def removeOldRating(filename):
    index = filename.find('(')
    new_filename = filename.replace(filename[index-1:index+5], "")
    os.rename(os.path.join(filename), os.path.join(new_filename))
    return new_filename

# Get the movie title by stripping out excess information such as the
# year released or video definition
def getMovieTitle(filename):
    if '(' in filename:
        return filename.split('(')[0]
    elif '[' in filename:
        return filename.split('[')[0]
    return ''.join(os.path.splitext(filename)[0])

def main():
    for filename in os.listdir(basepath):
        # Ignore hidden files and this script file
        if filename[0] is '.' or filename == __file__:
            continue
        if hasNewRating(filename):
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

        print ("Processed \'" + movie_title + "\' -> " + formatted_rating[1:-2])

    print ("\nDone!")

if __name__ == '__main__':
    main()
