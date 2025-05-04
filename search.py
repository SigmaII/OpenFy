from youtubesearchpython import VideosSearch
import sys

class Search():

        def dataParsing(song_name):
                str(song_name)
                title = []
                link = []
                thumbnail = []
                customSearch = VideosSearch(song_name, limit = 20)
                for i in range (19):
                        try:
                                title.append((customSearch.result())["result"][i]["title"])
                                link.append((customSearch.result())["result"][i]["link"])                       # customSearch.result() is dictionary composed by n index where 
                                                                                                   #one of this represents a specific result of the search ([0] is the 
                                thumbnail.append((customSearch.result())["result"][i]["thumbnails"][1]["url"])  #first song found, [1] the second...)
                                                                                                                # each index in composed by n fileds, one of this, for example, is the 
                                                                                                                #link that represent a link of the song
                        except IOError as e:
                                print("OS error:", e)
                        except ValueError:
                                print("Could not convert data to an integer.") # if thumbnail doesn't exist the try catch function return error but not stopping the program
                        except:
                                print("Unexpected error:", sys.exc_info()[0]) 
                data = [title, link, thumbnail]
                return data
        song = "Welcome to the Jungle"
        #for i in range (10):
        #        print (dataParsing(song)[0][i])
        #        print (dataParsing(song)[1][i])
        #        print (dataParsing(song)[2][i])
#customSearch = VideosSearch("Welcome to the Jungle", limit = 12)
#print ((customSearch.result())["result"][2]["title"])