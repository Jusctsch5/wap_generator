from exercise import Exercise
from workout import Workout
from announcer_wrapper import AnnouncerWrapper
from types import SimpleNamespace
import json
from pydub import AudioSegment
import random

class WorkoutDecoder:

    """
     WorkoutDecoder - Decodes input json workout file and creates a Workout class
    """

    def __init__(self):
        self.announcer_wrapper = AnnouncerWrapper()

    def __decode_workout(self, workout_filename, exercise_database, configuration):
        self.announcer_wrapper.configure(configuration)

        with open(workout_filename) as f:
            x = json.load(f, object_hook=lambda d: SimpleNamespace(**d))

        workout = Workout(x)
        workout.start_delay = workout.decoded_object.startDelay
        workout.finish_delay = workout.decoded_object.finishDelay

        # If specified, shuffle the provided exercises
        if configuration.decoded_object.ShuffleExercises:
            random.shuffle(workout.decoded_object.exercises)


        """
        Examples of Schema:

        Schema 1:
        Exercise is defined in entirity. Exercise DB is not required. 
        "exercises": [
            {
                "name": "Hex Squats",
                "description": "Standing up straight with arms at sides. Hook bands on feet. Bend knees to chair position and back.",
                "duration": 30,
                "sets": 3,
                "setCooldown": 10,
                "exerciseCooldown": 30
            },
        ]

        Schema 2:
        Drops the information about the exercise, use ID to look up the exercise.
        Information like muscle groups, muscles, description, switch sides, are in the exercise db.
        Information pertaining to duration and sets is contained here.
        "exercises": [
            {
                "id": "3d7f94b9-344e-47b7-a2f0-770cf49e8718",
                "duration": 30,
                "sets": 2,
                "setCooldown": 10,
                "exerciseCooldown": 30
            }
        ]

        Schema 1 will likely be deprecated, however no code below will have to change.
        """
    
        # Loop over exercises and create voice clips introducing them
        for exercise_i in range(0, len(workout.decoded_object.exercises)):

            # If the ID is supplied, then fill out the rest from the database.
            exercise_json = workout.decoded_object.exercises[exercise_i]
            print(exercise_json)
            exercise = Exercise()
            exercise.id = exercise_json.id
            exercise.duration = exercise_json.duration
            exercise.sets = exercise_json.sets
            exercise.setCooldown = exercise_json.setCooldown
            exercise.exerciseCooldown = exercise_json.exerciseCooldown
            if exercise.id:
                exercise = exercise_database.create_populated_exercise_from_db(exercise)

            workout.exercises.append(exercise)

        workout.transform_exercises_to_clip(configuration, self.announcer_wrapper)
        return workout

    def decode_workout(self, workout_filename, exercise_database, configuration):
        return self.__decode_workout(workout_filename, exercise_database, configuration)
