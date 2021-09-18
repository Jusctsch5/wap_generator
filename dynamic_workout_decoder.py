from exercise import Exercise
from workout import Workout
from announcer_wrapper import AnnouncerWrapper
from types import SimpleNamespace
import json
from pydub import AudioSegment
import random

class DynamicWorkoutDecoder:

    """
     DynamicWorkoutDecoder - Decodes input json workout file and creates a Workout class
    """

    def __init__(self):
        self.announcer_wrapper = AnnouncerWrapper()

    def __decode_workout(self, workout_filename, exercise_database, configuration):
        self.announcer_wrapper.configure(configuration)

        with open(workout_filename) as f:
            x = json.load(f, object_hook=lambda d: SimpleNamespace(**d))

        workout = Workout(x)

        """
        Examples of Schema:

        "dynamicworkout":
        {
            "name": "Dynamic Arms Workout",
            "musclegroups": ["arms"],
            "workoutduration": 20
        }

        musclegroups defines what muscles to work. a muscle not included in one of these groups will NOT be chosen.
        Multiple groups can be chosen to work on. Muscle groups are defined in the provided exercise database.
        Workout duration is defined in minutes
        """
        
        exercises = exercise_database.get_exercises_from_muscle_groups(workout.decoded_object.musclegroups)
        random.shuffle(exercises)
        total_duration = 0
        max_duration = workout.decoded_object.durationMinutes * 60
        done = False
        while(1):
            for i in range(0, len(exercises)):
                exercise = exercises[i]
                total_duration += exercise.total_duration
                print("Adding exercise: {} to workout. TotalDuration:{}/{}".format(exercise.name, total_duration, max_duration))
                workout.exercises.append(exercise)
                if total_duration >= max_duration:
                    done = True
                    break
            if done == True: break

        workout.transform_exercises_to_clip(configuration, self.announcer_wrapper)
        return workout

    def decode_workout(self, workout_filename, exercise_database, configuration):
        return self.__decode_workout(workout_filename, exercise_database, configuration)
