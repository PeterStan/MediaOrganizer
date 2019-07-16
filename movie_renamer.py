import os
import re
import shutil

from difflib import get_close_matches
from imdb import IMDb

#finds movie title using imdb 
def find_movie(search_title):
	ia = IMDb()
	titles = []
	movies = ia.search_movie(search_title)

	for movie in movies:
		titles = titles + [movie['long imdb title']]

	return get_close_matches(search_title,titles,n=1)[0]

#generates a coorectly formated name based on the given filename
def getNewName(filename):					
	print("current file: " + filename)

	title_regex = "([a-zA-Z. ']+?)( ?_?\W\d{4}\W?.*)"
	year_regex = "19\d{2}|20\d{2}";
	title_match = re.search(title_regex,filename)
	year_match = re.search(year_regex,filename)
	

	if(year_match):
		year = '(' + year_match.group(0) + ')'
	else:
		year = "";
	
	if(title_match):
		title = title_match.group(1).replace('.',' ')
	else:
		title = filename;

	return (title + " " + year)

#records all listed titles into the index file
def record_titles(index_file, titles):
	f = open(index_file, "w")
	for title in titles:
		f.write(title + '\n')
	else:
		f.close()

	return

#removes empty directories from the current directory, recursively
def remove_empty(currentDirectory):

	print("cleaning: " + currentDirectory)
	
	for file in os.listdir(currentDirectory):
		if(os.path.isdir(file) and not os.listdir(file)):
			print(file + " - empty dir")
			os.rmdir(file)
		elif(os.path.isdir(file) and (len(os.listdir(file)) == 1) and (os.listdir(file)[0] == "Thumbs.db")):
			print(file + " - almost empty dir")
			os.remove(os.path.join(currentDirectory,file,"Thumbs.db"))
			os.rmdir(file)
		elif(os.path.isdir(file)):
			remove_empty(file)
		else:
			print("\t" + file)

	print("done cleaning: " + currentDirectory)

	return

def rename_movies(lib_dir,currentDirectory):
	print("\norganizing: " + currentDirectory)

	baseDirectory = os.path.basename(currentDirectory)
	titles = [];

	movie_regex = ".*\.(mp4|avi|mov|mkv|srt|txt)$";
	correct_regex = "^([ a-zA-Z']+\(\d{4}\))[.](mp4|avi|mov|mkv|txt|srt)$";	
	
	for file in os.listdir(currentDirectory):

		movie_match = re.match(movie_regex,file)
		if(movie_match):
			if(re.match(correct_regex,file) and baseDirectory == re.match(correct_regex,file).group(1)):
				print("correct title: " + file)
				if(not baseDirectory in titles): titles = titles + [baseDirectory]
			else:
				extension = movie_match.group(1)

				new_filename = getNewName(file)
				print("old name: " + os.path.join(currentDirectory,file))
				print("new name: " + os.path.join(lib_dir,new_filename, (new_filename + "." + extension)))
				confirm = input("Is this title correct?")
				if(confirm == 'y'):
					if(not os.path.isdir(os.path.join(lib_dir,new_filename))):
						os.mkdir(os.path.join(lib_dir,new_filename))
					os.rename(os.path.join(currentDirectory,file),os.path.join(lib_dir,new_filename, (new_filename + "." + extension)))
					if(not new_filename in titles): titles = titles + [new_filename]
				else:
					new_filename = find_movie(file)
					print("old name: " + os.path.join(currentDirectory,file))
					print("new name: " + os.path.join(lib_dir,new_filename, (new_filename + "." + extension)))
					confirm = input("Is this title correct?")
					if(confirm == 'y'):
						if(not os.path.isdir(os.path.join(lib_dir,new_filename))):
							os.mkdir(os.path.join(lib_dir,new_filename))
						os.rename(os.path.join(currentDirectory,file),os.path.join(lib_dir,new_filename, (new_filename + "." + extension)))
						if(not new_filename in titles): titles = titles + [new_filename]
					
				print('\n')
		elif(os.path.isdir(file)):
			titles = titles + rename_movies(lib_dir, file)
		else:
			print("not a movie: " + file);

	else:
		print("done organizing: " + currentDirectory + "\n");
	return titles;

def parse_library(lib_dir):
	titles = rename_movies(lib_dir,lib_dir)
	record_titles("library_index.log", titles)
	remove_empty(lib_dir)
	return


parse_library(os.getcwd())

#TODO better regular expressions for movies
#https://support.plex.tv/articles/naming-and-organizing-your-movie-media-files/