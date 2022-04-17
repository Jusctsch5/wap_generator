from wap_generator.exercise.exercise import Exercise
from wap_generator.exercise.exercise_database_filter import ExerciseDatabaseFilter
from .workout import Workout
from wap_generator.announcer.announcer import Announcer
from types import SimpleNamespace
import json
import random


class DynamicWorkoutDecoder:

    """
     DynamicWorkoutDecoder - Decodes input json workout file and creates a Workout class
    """

    def __init__(self):
        self.announcer_wrapper = Announcer()

    def __decode_workout(self, workout_json, exercise_database, configuration):
        self.announcer_wrapper.configure(configuration)

        workout = Workout(workout_json)
        workout.name = workout.decoded_object.name
        if hasattr('workout.decoded_object', 'equipment'):
            workout.equipment = workout.decoded_object.equipment
        else:
            workout.equipment = []
        if hasattr('workout.decoded_object', 'startDelay'):
            workout.start_delay = workout.decoded_object.startDelay
        else:
            workout.start_delay = configuration.decoded_object.WorkoutStartDelayMinutesDefault
        if hasattr('workout.decoded_object', 'finishDelay'):
            workout.finish_delay = workout.decoded_object.finishDelay
        else:
            workout.finish_delay = configuration.decoded_object.WorkoutFinishDelayMinutesDefault
        if hasattr('workout.decoded_object', 'durationMinutes'):
            workout.total_duration = workout.decoded_object.durationMinutes * 60
        else:
            workout.total_duration = configuration.decoded_object.WorkoutDurationMinutesDefault * 60
        if hasattr('workout.decoded_object', 'musclegroups'):
            workout.muscle_groups = workout.decoded_object.musclegroups
        else:
            workout.muscle_groups = ["abdominals", "arms", "legs"]

        """
        Examples of Schema:

        "dynamicworkout":
        {
            "name": "Dynamic Arms Workout",
            "equipment" ["resistanceband"],
            "musclegroups": ["arms"],
            "workoutduration": 20
        }

        equipment defines what you have available.
        musclegroups defines what muscles to work. a muscle not included in one of these groups will NOT be chosen.
        Multiple groups can be chosen to work on. Muscle groups are defined in the provided exercise database.
        Workout duration is defined in minutes
        """

        filter = ExerciseDatabaseFilter(
            None, workout.muscle_groups, workout.equipment)
        exercises = exercise_database.get_exercises_from_filter(filter)
        random.shuffle(exercises)
        total_duration = 0
        max_duration = workout.total_duration

        print("Creating workout: {} for equipment: {} muscle groups: {}.".format(workout.name,
                                                                                 workout.equipment,
                                                                                 workout.muscle_groups))

        muscles_to_work = []

        for group in workout.muscle_groups:
            muscles_to_work.extend(
                exercise_database.get_muscles_in_muscle_group(group))

        # First try and work all of the muscle groups with different exercises
        for muscle in muscles_to_work:
            filter = ExerciseDatabaseFilter(
                muscle, [], workout.equipment)

            print("Finding exercises for required muscle:{}".format(muscle))
            exercises_for_muscle = exercise_database.get_exercises_from_filter(
                filter)
            random.shuffle(exercises_for_muscle)

            # Try to find a new exercise for this muscle.
            exercise = exercise_database.get_new_exercise_helper(
                exercises_for_muscle, workout.exercises)
            if exercise is None:
                continue

            # Add it to the workout
            total_duration += exercise.total_duration
            print("Adding exercise: {} for required muscle:{} to workout:{}. TotalDuration:{}/{}".format(
                exercise.name, muscle, workout.name, total_duration, max_duration))
            workout.exercises.append(exercise)
            if total_duration >= max_duration:
                break

        # Then plug exercises until the workout is complete
        while(total_duration < max_duration):

            exercise = exercise_database.get_new_exercise_helper(
                exercises, workout.exercises)

            total_duration += exercise.total_duration
            print("Adding exercise: {} to workout:{}. TotalDuration:{}/{}".format(
                exercise.name, workout.name, total_duration, max_duration))
            workout.exercises.append(exercise)

        workout.transform_exercises_to_clip(
            configuration, self.announcer_wrapper)
        return workout

    def decode_workout(self, workout_filename, exercise_database, configuration):
        with open(workout_filename) as f:
            x = json.load(f, object_hook=lambda d: SimpleNamespace(**d))

        return self.decode_workout_json(x, exercise_database, configuration)

    def decode_workout_json(self, workout_json, exercise_database, configuration):
        return self.__decode_workout(workout_json, exercise_database, configuration)
