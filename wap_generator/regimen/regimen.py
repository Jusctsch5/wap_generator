import os
import uuid
from wap_generator.workout.dynamic_workout_decoder import DynamicWorkoutDecoder
from wap_generator.playlist.playlist_decoder import PlaylistDecoder
from wap_generator.playlist.playlist import Playlist


class Day:
    def __init__(self):
        self.name = ""
        self.workouts = []


class Regimen:

    """
     Regimen - Decodes input json regimen file and creates a Regimen class
    """

    def __init__(self, i_decoded_object):
        self.decoded_object = i_decoded_object
        self.days = []
        self.id = uuid.uuid4().hex

    def process_regimen(self, output_directory, configuration, playlist):
        for day in self.days:
            print("Generating clip or regimen on day: {}".format(day.name))
            day_directory = os.path.join(output_directory, self.id, day.name)
            for workout in day.workouts:
                if playlist is None:
                    workout.generate_total_clip(day_directory, configuration)
                else:
                    playlist.create_combined_clip(
                        workout, day_directory, configuration)
