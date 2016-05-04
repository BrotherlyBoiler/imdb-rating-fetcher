import os, json, urllib.request, re

# Query related constants
base_uri = "http://www.omdbapi.com/?"
query_title = "t="

basepath = os.path.dirname(os.path.realpath(__file__))

RATING_LENGTH = 10		# Length of rating eg. [IMDb 8.2]

# Fetch movie rating from omdbapi.com. API returns JSON format.
def getMovieRating(movie_title):
    movie_title = movie_title.strip().replace(" ", "+")
    with urllib.request.urlopen(base_uri + query_title + movie_title) as url:
        data = json.loads(url.read().decode())    # decode to utf-8
    if 'Year' not in data:
        print ("Invalid response for " + movie_title)
        return None
    # Make sure server response matches year format
    pattern = re.compile('\d{4}')
    if pattern.match(data['Year']) is None:
        return None
    return data['Year']

def hasRating(filename):
    pattern = re.compile('\[IMDb [0-9].[0-9]\]')
    return pattern.search(filename) is not None

def getMovieTitle(filename):
	if hasRating(filename):
		filename = filename[RATING_LENGTH:].strip()
    if '(' in filename:
        return filename.split('(')[0]
    return ''.join(os.path.splitext(filename)[0])

# Check if the filename already has year
def hasYear(filename):
	pattern = re.compile('\(\d{4}\)')
	return pattern.search(filename) is not None

def addYear(filename):


def main():


if __name__ == '__main__':
	main()