from exercise import Exercise
from exercise_database import ExerciseDatabase
from types import SimpleNamespace
import json

class ExerciseDatabaseDecoder:

    """
     ExerciseDatabaseDecoder - Decodes input json ExerciseDatabase file and creates a ExerciseDatabase class
    """

    def __init__(self):
        pass

    def __decode_exercise_database(self, exercise_database_filename):
        exercise_database_object = ExerciseDatabase()

        with open(exercise_database_filename) as f:
            exercise_database_json = json.load(f)
            exercises = exercise_database_json["exercises"]
            for exercise in exercises:
                exercise_object = Exercise()
                print(str(exercise))
                exercise_object.name = exercise['name']
                exercise_object.description = exercise['description']
                exercise_object.id = exercise['id']
                if 'alternatesidesbetweensets' in exercise:
                    exercise_object.alternatesidesbetweensets = exercise['alternatesidesbetweensets']
                if 'musclegroups' in exercise:
                    exercise_object.musclegroups = exercise['musclegroups']
                if 'muscles' in exercise:
                    exercise_object.muscles = exercise['muscles']

                exercise_database_object.exercises.append(exercise_object)

        return exercise_database_object

    def decode_exercise_database(self, exercise_database_filename):
        return self.__decode_exercise_database(exercise_database_filename)
