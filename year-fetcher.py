import os, json, urllib.request, re

# Query related constants
base_uri = "http://www.omdbapi.com/?"
query_title = "t="

basepath = os.path.dirname(os.path.realpath(__file__))

RATING_LENGTH = 10		# Length of rating eg. [IMDb 8.2]

# Fetch movie rating from omdbapi.com. API returns JSON format.
def getMovieYear(title):
    movie_title = title.strip().replace(" ", "+")
    with urllib.request.urlopen(base_uri + query_title + movie_title) as url:
        data = json.loads(url.read().decode())    # decode to utf-8
    if 'Year' not in data:
        print ("Invalid response for " + title)
        return None
    # Make sure server response matches year format
    pattern = re.compile('\d{4}')
    if pattern.match(data['Year']) is None:
    	print ("")
        return None
    return data['Year']

def hasRating(filename):
    pattern = re.compile('\[IMDb \d\.\d\]')
    return pattern.match(filename) is not None

def getMovieTitle(filename):
	if hasRating(filename):
		filename = filename[RATING_LENGTH:].strip()
    return ''.join(os.path.splitext(filename)[0])

# Check if the filename already has year
def hasYear(filename):
	pattern = re.compile('\(\d{4}\)')
	return pattern.match(filename) is not None

def main():
	for filename in os.listdir(basepath):
		if hasYear(filename) or filename == __file__:
			continue
		movie_title = getMovieTitle(filename)
		movie_year = getMovieYear(movie_title)
		if movie_year is None:
			continue

		formatted_year = '(' + movie_year + ')'
		file_no_ext, file_ext = os.path.splitext(filename)
		new_filename = file_no_ext + ' ' + formatted_year + file_ext
		os.rename(os.path.join(filename), os.path.join(new_filename))
		addYear(filename, movie_year)

		print ("Processed \'" + movie_title + "\' -> " + movie_year)

if __name__ == '__main__':
	main()