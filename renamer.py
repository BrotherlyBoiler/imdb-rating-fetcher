'''
    Search through a target movies directory and filter movie titles
    to search IMDb for movie ratings. After fetching, append ratings
    to corresponding movie files/folders in the directory.

    File names are in one of the following formats:
    1. P.S. I Love You.mkv
    2. P.S. I Love You (2010).mp4
    3. P.S. I Love You (2010) [1080p].avi

    Ideally, this program fetched the movie ratings and adds it to
    the end of the file name (just before the extension). The query,
    in this case, would be http://www.omdbapi.com/?t=P.S.+I+Love+You

    Ideally, the file in the directory would be renamed to one of
    the following:
    1. P.S. I Love You (7.1).mkv
    2. P.S. I Love You (2010) (7.1).mp4
    3. P.S. I Love You (2010) [1080p] (7.1).avi
'''

import os, json, urllib.request, re

# Query related constants
base_uri = "http://www.omdbapi.com/?"
query_title = "t="

basepath = "C:/Users/Vishal/Downloads/Movies/"
# basepath = "E:/Movies"

# Fetch movie rating from omdbapi.com. API return JSON format.
def getRating(movie_title):
    movie_title = movie_title.strip().replace(" ", "+")
    # Request API for JSON response
    with urllib.request.urlopen(base_uri + query_title + movie_title) as url:
        movie_data = json.loads(url.read().decode())    # decode to utf-8
    if 'imdbRating' not in movie_data:
        print ("Cannot find rating for " + movie_title)
        return None
    return movie_data['imdbRating']

# Checks if parameter file name already has a rating.
# Movie ratings are in the format (\d.\d)
def hasRating(filename):
    pattern = re.compile('\[IMDb [0-9].[0-9]\]')
    if pattern.search(filename) is not None:
        return True
    return False

def hasOldRating(filename):
    pattern = re.compile('\([0-9].[0-9]\)')
    if pattern.search(filename) is not None:
        return True
    return False

# Get the movie title by stripping out excess information such as the
# year released or video definition
def getMovieTitle(filename):
    if '(' in filename:
        return filename.split('(')[0]
    elif '[' in filename:
        return filename.split('[')[0]
    return ''.join(os.path.splitext(filename)[0])

def main():
    renamed = 0
    skipped = 0
    reformatted = 0

    print ("Running renamer...")
    for filename in os.listdir(basepath):
        if hasOldRating(filename):
            renamed += 1;

        if hasRating(filename) is True:
            skipped += 1
            continue

        movie_title = getMovieTitle(filename)
        file_ext = os.path.splitext(filename)[1]
        print (movie_title + "\n\n")
        movie_rating = getRating(movie_title)
        if (movie_rating is None):
            skipped += 1
            continue

        formatted_rating = '[IMDb ' + movie_rating + '] '
        file_no_ext = os.path.splitext(filename)[0]
        new_file_name = formatted_rating + file_no_ext + file_ext
        os.rename(os.path.join(basepath + filename), os.path.join(basepath + new_file_name))

        print ("\'" + filename + "\' -> \'" + new_file_name + "\'")
        renamed += 1

    print ("Done. ", end="")
    if (renamed is 0 and skipped is 0 and reformatted is 0): print ("No changes made.")
    if (renamed > 0): print (renamed + " renamed, ", end="")
    if (skipped > 0): print(skipped + " skipped, ", end="")
    if (reformatted > 0): print(reformatted + " reformatted.")

if __name__ == '__main__':
    main()
