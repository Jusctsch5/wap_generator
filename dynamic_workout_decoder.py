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
        workout.name = workout.decoded_object.name
        workout.start_delay = workout.decoded_object.startDelay
        workout.finish_delay = workout.decoded_object.finishDelay

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

        muscles_to_work = []
        for group in workout.decoded_object.musclegroups:
            muscles_to_work.extend(exercise_database.get_muscles_in_muscle_group(group))


        # First work all of the muscle groups with different exercises
        for muscle in muscles_to_work:
            exercises_for_muscle = exercise_database.get_exercises_for_muscle(muscle)
            random.shuffle(exercises_for_muscle)

            # Try to find a new exercise
            exercise = exercise_database.get_new_exercise_helper(exercises, workout.exercises)

            total_duration += exercise.total_duration
            print("Adding exercise: {} for required muscle:{} to workout. TotalDuration:{}/{}".format(exercise.name, muscle, total_duration, max_duration))
            workout.exercises.append(exercise)
            if total_duration >= max_duration:
                break

        # Then plug exercises until the workout is complete
        while(total_duration < max_duration):

            exercise = exercise_database.get_new_exercise_helper(exercises, workout.exercises)

            total_duration += exercise.total_duration
            print("Adding exercise: {} to workout. TotalDuration:{}/{}".format(exercise.name, total_duration, max_duration))
            workout.exercises.append(exercise)

        workout.transform_exercises_to_clip(configuration, self.announcer_wrapper)
        return workout

    def decode_workout(self, workout_filename, exercise_database, configuration):
        return self.__decode_workout(workout_filename, exercise_database, configuration)
