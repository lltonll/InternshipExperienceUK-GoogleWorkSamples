"""A video player class."""

from os import error
from src import video, video_playlist
from .video_library import VideoLibrary
from .video_playlist import Playlist
import random
import json


class VideoPlayer:
    """A class used to represent a Video Player."""
    Playing = False
    Playing_Title = None
    Pause = False
    Playing_object = None
    video_playlist = '{"playlist":[]}'
    flag = '{"flag": []}'


    def __init__(self):
        self._video_library = VideoLibrary()
        self._video_playlist = Playlist()
        

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        all_vidios = self._video_library.get_all_videos()
        flag_obj = json.loads(self.flag)
        flag = True
        print("Here's a list of all available videos:")
        printing_array = []
        for i in range(len(all_vidios)):
            tags = all_vidios[i].tags
            if len(flag_obj["flag"]) != 0:
                for index, value in enumerate(flag_obj["flag"]):
                    for index2, value2 in enumerate(all_vidios):
                        if value2._video_id == value["video_id"]: 
                            printing_array.append(f"{all_vidios[i].title} ({all_vidios[i].video_id}) [{' '.join(tags)}] - FLAGGED (reason: {value['reason']})")
                            flag = False
            if flag == True:
                printing_array.append(f"{all_vidios[i].title} ({all_vidios[i].video_id}) [{' '.join(tags)}]")
                printing_array = sorted(printing_array)
            else: flag = True
        print("\n".join(printing_array))


    def play_video(self, video_id):
        """Plays the respective video.
        Args:
            video_id: The video_id to be played.
        """
        flag_obj = json.loads(self.flag)
        try:
            for index, value in enumerate(flag_obj["flag"]):
                if video_id == value["video_id"]: return print(f"Cannot play video: Video is currently flagged (reason: {value['reason']})")
            play_video = self._video_library.get_video(video_id)
            if play_video == None: 
                assert False
            # print(play_video.title)
            if self.Playing == True:
                self.stop_video()
                self.Playing = True
                self.Pause = False
                self.Playing_object = play_video
                print(f"Playing video: {play_video.title}")
            elif self.Playing == False: 
                self.Playing = True
                self.Pause = False
                self.Playing_object = play_video
                print(f"Playing video: {play_video.title}")
        except:
            print("Cannot play video: Video does not exist")

    def stop_video(self):
        """Stops the current video."""
        if self.Playing_object != None:
            self.Playing = False
            self.Pause = False
            print(f"Stopping video: {self.Playing_object.title}")
            self.Playing_object = None
        else:
            print("Cannot stop video: No video is currently playing")

    def play_random_video(self):
        """Plays a random video from the video library."""
        flag_obj = json.loads(self.flag)
        all_vidios = self._video_library.get_all_videos()
        random_number = random.randint(0, len(all_vidios)-1)
        if len(flag_obj["flag"]) == 5: return print("No videos available")
        if self.Playing == False:
            self.Playing = True
            self.Pause = False
            self.Playing_object = all_vidios[random_number]
            for index, value in enumerate(flag_obj["flag"]):
                if self.Playing_object._video_id == value["video_id"]: return print(f"Cannot play video: Video is currently flagged (reason: {value['reason']})")
            print(f"Playing video: {self.Playing_object.title}")
        else:
            self.stop_video()
            self.Playing = True
            self.Pause = False
            self.Playing_object = all_vidios[random_number]
            for index, value in enumerate(flag_obj["flag"]):
                if self.Playing_object._video_id == value["video_id"]: return print(f"Cannot play video: Video is currently flagged (reason: {value['reason']})")
            print(f"Playing video: {self.Playing_object.title}")
        # print("play_random_video needs implementation")

    def pause_video(self):
        """Pauses the current video."""
        # print(self.Playing)
        if self.Pause == False and self.Playing == True:
            self.Pause = True
            print(f"Pausing video: {self.Playing_object.title}")
        elif self.Pause == True and self.Playing == True:
            print(f"Video already paused: {self.Playing_object.title}")
        elif self.Pause == False and self.Playing == False:
            print("Cannot pause video: No video is currently playing")
        else: 
            print("Invaild") 

        # print("pause_video needs implementation")

    def continue_video(self):
        """Resumes playing the current video."""
        if self.Pause == False and self.Playing == True:
            print("Cannot continue video: Video is not paused")
        elif self.Pause == True and self.Playing == True:
            self.Pause = False
            print(f"Continuing video: {self.Playing_object.title}")
        elif self.Pause == False and self.Playing == False:
            print("Cannot continue video: No video is currently playing")
        else: 
            print("Invaild") 
        # print("continue_video needs implementation")

    def show_playing(self):
        """Displays video currently playing."""
        if self.Playing == True and self.Pause == False:
            print(f"Currently playing: {self.Playing_object.title} ({self.Playing_object.video_id}) [{' '.join(self.Playing_object.tags)}]")
        elif self.Playing == True and self.Pause == True:
            print(f"Currently playing: {self.Playing_object.title} ({self.Playing_object.video_id}) [{' '.join(self.Playing_object.tags)}] - PAUSED")
        else:
            print("No video is currently playing")
        
            

        # print("show_playing needs implementation")

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.
        Args:
            playlist_name: The playlist name.
        """
        duplication_flag = False
        playlist_obj = json.loads(self.video_playlist)
        if len(playlist_obj["playlist"]) == 0:
            playlist_obj["playlist"].append({"name": playlist_name, "video": []})
            self.video_playlist = json.dumps(playlist_obj)
            print(f"Successfully created new playlist: {playlist_name}")
            
        elif len(playlist_obj["playlist"]) > 0: 
            # Duplicate
            for i in playlist_obj["playlist"]:
                if i["name"].lower() == playlist_name.lower(): 
                    duplication_flag = True
            if duplication_flag == True: print("Cannot create playlist: A playlist with the same name already exists")
            else: 
                playlist_obj["playlist"].append({"name": playlist_name, "video": []})
                self.video_playlist = json.dumps(playlist_obj)
                print(f"Successfully created new playlist: {playlist_name}")
        # else: print("error")

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.
        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        # """

        duplication_flag = False
        video_object = self._video_library.get_video(video_id)
        playlist_data = json.loads(self.video_playlist)
        playlist_obj = None
        flag_obj = json.loads(self.flag)
        for index, value in enumerate(flag_obj["flag"]):
            if video_id == value["video_id"]: return print(f"Cannot add video to {playlist_name}: Video is currently flagged (reason: {value['reason']}))")

        if len(playlist_data["playlist"]) != 0:
            for index, element in enumerate(playlist_data["playlist"]):
                # print(index, element)
                if element["name"].upper() == playlist_name.upper():
                    playlist_obj = element
                    playlist_data["playlist"].pop(index)
                
        if video_object == None and playlist_obj == None: 
            print(f"Cannot add video to {playlist_name}: Playlist does not exist")
        elif video_object == None and playlist_obj != None: 
            print(f"Cannot add video to {playlist_obj['name']}: Video does not exist")
        elif video_object != None and playlist_obj == None:
            print(f"Cannot add video to {playlist_name}: Playlist does not exist")
        elif video_object != None and playlist_obj != None:
            if len(playlist_obj["video"]) == 0:
                playlist_obj["video"].append(video_object._video_id)
                playlist_data["playlist"].append(playlist_obj)
                self.video_playlist = json.dumps(playlist_data)
                print(f"Added video to {playlist_name}: {video_object._title}")
            #check first
            else: 
                for i in playlist_obj["video"]:
                    if i == video_id:
                        duplication_flag = True
                if duplication_flag == False:
                    playlist_obj["video"].append(video_object._video_id)
                    playlist_data["playlist"].append(playlist_obj)
                    self.video_playlist = json.dumps(playlist_data)
                    print(f"Added video to {playlist_name}: {video_object._title}")
                else:
                    print(f"Cannot add video to {playlist_obj['name']}: Video already added")
        else: print(f"Cannot add video to {playlist_name}: Playlist does not exist")

    def show_all_playlists(self):
        """Display all playlists."""
        playlists = json.loads(self.video_playlist)
        printing_array = []
        if len(playlists["playlist"]) == 0: 
            print("No playlists exist yet")
        else: 
            print("Showing all playlists:")
            for index, value in enumerate(playlists["playlist"]):
                printing_array.append(value["name"])
                printing_array = sorted(printing_array)
            print("\n".join(printing_array))

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.
        Args:
            playlist_name: The playlist name.
        """
        playlists = json.loads(self.video_playlist)
        for index, value in enumerate(playlists["playlist"]):
            if value["name"].upper() == playlist_name.upper():
                if len(value["video"]) == 0: return print(f"Showing playlist: {playlist_name} \n No videos here yet")
                else:
                    print(f"Showing playlist: {playlist_name}")
                    printing_array = []
                    for index2, value2 in enumerate(value["video"]):
                        video = self._video_library.get_video(value2)
                        tags = video._tags
                        printing_array.append(f"{video._title} ({video._video_id}) [{' '.join(tags)}]")
                    return print('\n'.join(printing_array))
                    
        else: print(f"Cannot show playlist {playlist_name}: Playlist does not exist")

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.
        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        playlists = json.loads(self.video_playlist)
        video_obj = self._video_library.get_video(video_id)
        target_playlist_obj = None
        remove_flag = False
        try:
            for index, value in enumerate(playlists["playlist"]):
                if value["name"].upper() == playlist_name.upper():
                    target_playlist_obj = [value, index]
            if target_playlist_obj == None and video_obj == None: print(f"Cannot remove video from {playlist_name}: Playlist does not exist")
            elif target_playlist_obj == None and video_obj != None: print(f"Cannot remove video from {playlist_name}: Playlist does not exist")
            elif target_playlist_obj != None and video_obj == None: print(f"Cannot remove video from {playlist_name}: Video does not exist")
            else: 
                for index, value in enumerate(target_playlist_obj[0]["video"]):
                    if value == video_id: 
                        remove_flag = True
                        print(f"Removed video from {playlist_name}: {self._video_library.get_video(value)._title}")
                        playlists["playlist"][target_playlist_obj[1]]["video"].remove(value)
                        self.video_playlist = json.dumps(playlists)
                        break
                if remove_flag == False: print(f"Cannot remove video from {playlist_name}: Video is not in playlist")    
        except: print(error)


        # playlist_object = self._video_playlist.get_playlist(playlist_name)
        # video_object = self._video_library.get_video(video_id)
        # if playlist_object == None and video_object == None: print(f"Cannot remove video from {playlist_name}: Playlist does not exist")
        # elif playlist_object != None and video_object == None: print(f"Cannot remove video from {playlist_name}: Video does not exist")
        # elif playlist_object == None and video_object != None: print(f"Cannot remove video from {playlist_name}: Playlist does not exist")
        # else: 
        #     if len(playlist_object["video"]) == 0: print(f"Cannot remove video from {playlist_object['name']}: Video is not in playlist")
        #     for i in range(len(playlist_object["video"])):
        #         if playlist_object["video"][i].video_id == video_id:
        #             playlist_object["video"].pop(i)
        #             result = self._video_playlist.updatePlaylist(playlist_object)
        #             print(f"Removed video from my_playLIST: {video_object.title}")
        #         else: print(f"Cannot remove video from {playlist_object['name']}: Video does not exist")


        # print("remove_from_playlist needs implementation")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.
        Args:
            playlist_name: The playlist name.
        """
        playlists = json.loads(self.video_playlist)
        if len(playlists["playlist"]) == 0: return print(f"Cannot clear playlist {playlist_name}: Playlist does not exist")
        for i, value in enumerate(playlists["playlist"]):
            if value["name"].upper() == playlist_name.upper():
                playlists["playlist"][i]["video"] = []
                self.video_playlist = json.dumps(playlists)
                return print(f"Successfully removed all videos from {playlist_name}")
        print(f"Cannot clear playlist {playlist_name}: Playlist does not exist")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlists = json.loads(self.video_playlist)
        if len(playlists["playlist"]) == 0: return print(f"Cannot delete playlist {playlist_name}: Playlist does not exist")
        for index, value in enumerate(playlists["playlist"]):
            if value["name"].upper() == playlist_name.upper():
                playlists["playlist"].pop(index)
                self.video_playlist = json.dumps(playlists)
                return print(f"Deleted playlist: {playlist_name}")
        return print(f"Cannot delete playlist {playlist_name}: Playlist does not exist")

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        videos = self._video_library.get_all_videos()
        keywordInput = search_term
        keywordInput = keywordInput

        search_results = []
        for index, value in enumerate(videos):
            checkingArray = None
            tags = value._tags 
            checkingArray = (f"{value._title.upper()} ({value._video_id.upper()}) [{' '.join(tags).upper()}]")
            if keywordInput.upper() in checkingArray:
                search_results.append(value)
        if len(search_results) == 0: return print(f"No search results for {keywordInput}")
        else:
            printing_format = []
            for index, value in enumerate(search_results):
                tags = value._tags 
                printing_format.append(f"{index+1}) {value._title} ({value._video_id}) [{' '.join(tags)}]")
            print(f"Here are the results for {search_term}:")
            print(" \n".join(printing_format))
            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")
            try: 
                userInput = int(input())
            
                if userInput in range(1,len(search_results)+1) and isinstance(userInput, int):
                    return print(f"Playing video: {search_results[userInput-1]._title}")
            except:
                return None

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        videos = self._video_library.get_all_videos()
        search_results = []
        for index, value in enumerate(videos):
            checkingArray = None
            tags = value._tags 
            checkingArray = (f"{value._title.upper()} ({value._video_id.upper()}) [{' '.join(tags).upper()}]")
            if video_tag.upper() in checkingArray:
                search_results.append(value)
        if len(search_results) == 0: return print(f"No search results for {video_tag}")
        else:
            printing_format = []
            for index, value in enumerate(search_results):
                tags = value._tags 
                printing_format.append(f"{index+1}) {value._title} ({value._video_id}) [{' '.join(tags)}]")
            print(f"Here are the results for {video_tag}:")
            print(" \n".join(printing_format))
            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")
            try: 
                userInput = int(input())
            
                if userInput in range(1,len(search_results)+1) and isinstance(userInput, int):
                    return print(f"Playing video: {search_results[userInput-1]._title}")
            except:
                return None

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        video_obj = self._video_library.get_video(video_id)
        flag_message = None
        flag_video_obj = json.loads(self.flag)
        if video_obj == None: return print("Cannot flag video: Video does not exist")
        if flag_reason == "": flag_message = "Not supplied"
        else: flag_message = flag_reason
        if len(flag_video_obj["flag"]) == 0:
            flag_video_obj["flag"].append({"video_id": video_id, "reason": flag_message})
            self.flag = json.dumps(flag_video_obj)
            return print(f"Successfully flagged video: {video_obj._title} (reason: {flag_message})")
        else:
            for index, value in enumerate(flag_video_obj["flag"]):
                if video_id == value["video_id"]: return print("Cannot flag video: Video is already flagged")
            flag_video_obj["flag"].append({"video_id": video_id, "reason": flag_message})
            self.flag = json.dumps(flag_video_obj)
            return print(f"Successfully flagged video: {video_obj._title} (reason: {flag_message})")

        

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        print("allow_video needs implementation")
