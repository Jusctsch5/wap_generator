import os
from pydub import AudioSegment
import random
from pathlib import Path

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
        current_duration = 0 
        resulting_clip = workout.total_clip

        playlist_directory = configuration.decoded_object.AdditionalSongDirectory
        shuffle = configuration.decoded_object.ShufflePlaylist
        output_dir = configuration.decoded_object.OutputDirectory

        # If specified, shuffle the provided playlist
        if shuffle:
            random.shuffle(self.decoded_object.playlist)

        done = False
        while(1):
            for i in range(0, len(self.decoded_object.playlist)):
                song = self.decoded_object.playlist[i]
                
                resulting_name = self.__find_song_name(playlist_directory, song.name)
                if resulting_name == "":
                    print("Unable to find Song: {} from directory: {}".format(song.name, playlist_directory))
                    continue
                
                song_segment = AudioSegment.from_file(resulting_name)
                song_segment = song_segment.apply_gain(-12)
                
                resulting_clip = resulting_clip.overlay(song_segment, 
                                                        gain_during_overlay=0,
                                                        position=1000 * current_duration)
                current_duration += song_segment.duration_seconds

                print("Appending Song: {} to workout. Current Duration: {}, Workout Duration: {}".format(song.name, current_duration, workout_duration))

                if current_duration >= workout_duration:
                    done = True
                    break
            if done == True:
                break
            if shuffle:
                random.shuffle(self.decoded_object.playlist)
    
        resulting_name = workout.decoded_object.name + "WithPlaylist.mp3"
        resulting_name = os.path.join(output_dir, resulting_name)
        print("Creating new total workout clip and playlist with name: " + resulting_name)
        file_handle = resulting_clip.export(resulting_name, format="mp3")
            

        
