from fetchers.indeed import indeed
import os

if(os.path.isfile("fetchers/indeed/prefs.json")):
    indeed.IndeedFetcher().get()
else:
    print("Please, edit and copy prefs-example.json")
