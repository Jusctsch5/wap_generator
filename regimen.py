import os
import uuid
from dynamic_workout_decoder import DynamicWorkoutDecoder

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

    def process_regimen(self, output_directory):
        for day in self.days:
            print("Generating clip or regimen on day: {}".format(day.name))
            day_directory = os.path.join(output_directory, self.id, day.name)
            for workout in day.workouts:
                workout.generate_total_clip(day_directory)