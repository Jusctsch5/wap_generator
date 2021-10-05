import os
from pydub import AudioSegment
import random
from pathlib import Path
import datetime

class Playlist:

    """
     Playlist - Decodes input json workout file and creates a Playlist class
    """

    def __init__(self, i_decoded_object):
        self.decoded_object = i_decoded_object
        self.create_playlist_from_directory = False
        self.list_of_songs = []

    def __find_song_name(self, playlist_directory, name):
        print("looking for song {} in playlist directory {}".format(name, playlist_directory))
        for path in Path(playlist_directory).rglob(name):
            print("Found path:" +str(path))
            return path

    def __get_list_of_songs_from_directory(self, directory):
        list_of_songs = []
        for path in Path(directory).rglob("*mp3"):
            list_of_songs.append(path)

        return list_of_songs

    def create_combined_clip(self, workout, configuration):
        
        workout_duration = workout.total_clip.duration_seconds
        resulting_clip = workout.total_clip

        playlist_directory = configuration.decoded_object.AdditionalSongDirectory
        shuffle = configuration.decoded_object.ShufflePlaylist
        output_dir = configuration.decoded_object.OutputDirectory

        list_of_songs = []
        if self.create_playlist_from_directory is True:
            list_of_songs = self.__get_list_of_songs_from_directory(playlist_directory)
        else:
            for song in self.decoded_object.playlist:
                resulting_name = self.__find_song_name(playlist_directory, song.name)
                if resulting_name == "":
                    print("Unable to find Song: {} from directory: {}".format(song, playlist_directory))
                    continue                
                list_of_songs.append(resulting_name)

        # If specified, shuffle the provided playlist
        if shuffle:
            random.shuffle(list_of_songs)

        done = False
        playlist_clip = AudioSegment.empty()
        while(1):
            for i in range(0, len(list_of_songs)):
                song = list_of_songs[i]
                song_segment = AudioSegment.from_file(song)
                song_segment = song_segment.apply_gain(-12)
                if configuration.decoded_object.CrossFade == True and playlist_clip.duration_seconds != 0:
                    # print("Applying crossfade")
                    playlist_clip = playlist_clip.append(song_segment, crossfade=2500)
                else:
                    playlist_clip += song_segment
                
                print("Appending Song: {} to workout. Current Duration: {}, Workout Duration: {}"
                      .format(song, playlist_clip.duration_seconds, workout_duration))

                if playlist_clip.duration_seconds >= workout_duration:
                    done = True
                    break
            if done == True:
                break
            if shuffle:
                random.shuffle(self.decoded_object.playlist)


        print("Resulting playlist file is {} seconds".format(playlist_clip.duration_seconds))
        resulting_clip = resulting_clip.overlay(playlist_clip)
        print("Resulting workout file is {} seconds".format(resulting_clip.duration_seconds))

        resulting_name = workout.decoded_object.name + "_" + str(datetime.date.today()).replace("-", "_") + "_" + "WithPlaylist.mp3"
        resulting_name = os.path.join(output_dir, resulting_name)

        print("Creating new total workout clip and playlist with name: " + resulting_name)
        file_handle = resulting_clip.export(resulting_name, format="mp3")
            

        
