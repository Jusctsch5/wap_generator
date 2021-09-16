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

    def __find_song_name(self, playlist_directory, name):
        for path in Path(playlist_directory).rglob(name):
            print("Found path:" +str(path))
            return path

    def create_combined_clip(self, workout, configuration):
        
        workout_duration = workout.total_clip.duration_seconds
        resulting_clip = workout.total_clip

        playlist_directory = configuration.decoded_object.AdditionalSongDirectory
        shuffle = configuration.decoded_object.ShufflePlaylist
        output_dir = configuration.decoded_object.OutputDirectory

        # If specified, shuffle the provided playlist
        if shuffle:
            random.shuffle(self.decoded_object.playlist)

        done = False
        playlist_clip = AudioSegment.empty()
        while(1):
            for i in range(0, len(self.decoded_object.playlist)):
                song = self.decoded_object.playlist[i]
                
                resulting_name = self.__find_song_name(playlist_directory, song.name)
                if resulting_name == "":
                    print("Unable to find Song: {} from directory: {}".format(song.name, playlist_directory))
                    continue
                
                song_segment = AudioSegment.from_file(resulting_name)
                song_segment = song_segment.apply_gain(-12)
                if configuration.decoded_object.CrossFade == True and playlist_clip.duration_seconds != 0:
                    print("Applying crossfade")
                    playlist_clip = playlist_clip.append(song_segment, crossfade=2500)
                else:
                    playlist_clip += song_segment
                
                print("Appending Song: {} to workout. Current Duration: {}, Workout Duration: {}"
                      .format(song.name, playlist_clip.duration_seconds, workout_duration))

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
            

        
