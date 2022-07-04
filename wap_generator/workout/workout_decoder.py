from wap_generator.exercise.exercise import Exercise
from workout import Workout
from wap_generator.announcer.announcer import Announcer
from types import SimpleNamespace
import json
import random


class WorkoutDecoder:

    """
     WorkoutDecoder - Decodes input json workout file and creates a Workout class
    """

    def __init__(self):
        self.announcer_wrapper = Announcer()

    def __process_workout(self, exercise_database, configuration):
        pass

    def __decode_workout(self, workout_filename, exercise_database, configuration):
        self.announcer_wrapper.configure(configuration)

        with open(workout_filename) as f:
            x = json.load(f, object_hook=lambda d: SimpleNamespace(**d))

        workout = Workout(x)
        workout.name = workout.decoded_object.name
        if hasattr('workout.decoded_object', 'startDelay'):
            workout.start_delay = workout.decoded_object.startDelay
        else:
            workout.start_delay = configuration.decoded_object.WorkoutStartDelayMinutesDefault
        if hasattr('workout.decoded_object', 'finishDelay'):
            workout.finish_delay = workout.decoded_object.finishDelay
        else:
            workout.finish_delay = configuration.decoded_object.WorkoutFinishDelayMinutesDefault
        if hasattr('workout.decoded_object', 'durationMinutes'):
            workout.total_duration = workout.decoded_object.durationMinutes
        else:
            workout.total_duration = configuration.decoded_object.WorkoutDurationMinutesDefault

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
            logging.debug(exercise_json)
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
