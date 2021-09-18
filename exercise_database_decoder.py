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

    def __validate_exercise(self, exercise_database_object, exercise_object):
        # Validate all fields exist
        if exercise_object.name == "":
            raise ValueError("Exercise {} needs a name".format(exercise_object.name))        
        if exercise_object.description == "":
            raise ValueError("Exercise {} needs a description".format(exercise_object.name))                    
        if exercise_object.id == "":
            raise ValueError("Exercise {} needs an id".format(exercise_object.id))                                
        if len(exercise_object.musclegroups) == 0:
            raise ValueError("Exercise {} needs to work one or more muscle groups".format(exercise_object.name))        
        
        # For now, let's not mandate muscles. 
        #if len(exercise_object.muscles) == 0:
            #raise ValueError("Exercise {} needs to work one or more muscles".format(exercise_object.name))
        
        # Validate against the db for valid muscles and groups
        for muscle in exercise_object.muscles:
            if not muscle in exercise_database_object.muscles:
                raise ValueError("Exercise {} has an invalid muscle: {}".format(exercise_object.name, muscle))

        for musclegroup in exercise_object.musclegroups:
            if not musclegroup in exercise_database_object.musclegroups:
                raise ValueError("Exercise {} has an invalid musclegroup: {}".format(exercise_object.name, musclegroup))

        # Validate against other exercises for unique fields
        for exercise in exercise_database_object.exercises:
            if exercise_object.id == exercise.id:
                raise ValueError("Exercise {} ID already exists".format(exercise_object.name))
            if exercise_object.name == exercise.name:
                raise ValueError("Exercise {} Name already exists".format(exercise_object.name))

    def __decode_exercise_database(self, exercise_database_filename):
        exercise_database_object = ExerciseDatabase()

        with open(exercise_database_filename) as f:
            exercise_database_json = json.load(f)
            exercise_database_object.muscles = exercise_database_json["muscles"]
            exercise_database_object.musclegroups = exercise_database_json["musclegroups"]

            exercises_json = exercise_database_json["exercises"]
            for exercise_json in exercises_json:
                exercise_object = Exercise()
                print(str(exercise_json))
                exercise_object.name = exercise_json['name']
                exercise_object.description = exercise_json['description']
                exercise_object.id = exercise_json['id']
                if 'alternatesidesbetweensets' in exercise_json:
                    exercise_object.alternatesidesbetweensets = exercise_json['alternatesidesbetweensets']
                if 'musclegroups' in exercise_json:
                    exercise_object.musclegroups = exercise_json['musclegroups']
                if 'muscles' in exercise_json:
                    exercise_object.muscles = exercise_json['muscles']

                self.__validate_exercise(exercise_database_object, exercise_object)
                exercise_database_object.exercises.append(exercise_object)

        return exercise_database_object

    def decode_exercise_database(self, exercise_database_filename):
        return self.__decode_exercise_database(exercise_database_filename)
