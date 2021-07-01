"""A video playlist class."""


import json
from src import video


class Playlist:
    """A class used to represent a Playlist."""
    video_playlist = '{"playlist":[]}'

    def get_playlist(self, name):
        try: 
            for i in range(len(self.video_playlist["playlist"])):
                if self.video_playlist["playlist"][i]["name"].casefold() == name.casefold():
                    return self.video_playlist["playlist"][i]
            return None
        except:
            return None

    def get_playlist_index(self, name):
        try: 
            for i in range(len(self.video_playlist["playlist"])):
                if self.video_playlist["playlist"][i]["name"].casefold() == name.casefold():
                    return i
            return None
        except:
            return None

    def get_all_playlist(self):
        return self.video_playlist["playlist"]

    def add_new_playlist(self, playlistName):
        jsonFormat = {"name": playlistName, "video": []}
        self.video_playlist["playlist"].append(jsonFormat)
        return self.video_playlist["playlist"][len(self.video_playlist["playlist"])-1]

    def isPlaylistExist(self, name):
        if len(self.video_playlist["playlist"]) != 0:
            for i in range(len(self.video_playlist["playlist"])):
                if self.video_playlist["playlist"][i]["name"].casefold() == name.casefold():
                    return True
            return False
        else: return False

    def addVideo(self, playlistName, video_object):
        try:
            result_object = self.get_playlist(playlistName)
            result_index = self.get_playlist_index(playlistName)
            if result_object != None and result_index != None:
                result_object["video"].append(video_object)
                self.video_playlist["playlist"][result_index] = result_object
                return result_object
            else: return "error"
        except:
            return "error"

    def isVideoInPlaylist(self, playlistName, video_object):
        try:
            playlist_object = self.get_playlist(playlistName)
            for i in range(len(playlist_object["video"])):
                if playlist_object["video"][i].title == video_object.title:
                    return True
            return False

        except:
            return "error"


    def updatePlaylist(self, playlistObject):
        index = self.get_playlist_index(playlistObject["name"])
        self.video_playlist["playlist"][index] = playlistObject
        return self.video_playlist["playlist"]