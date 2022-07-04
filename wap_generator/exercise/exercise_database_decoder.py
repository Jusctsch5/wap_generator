from pathlib import PurePath
from wap_generator.exercise.exercise import Exercise
from wap_generator.exercise.exercise_database import ExerciseDatabase
import json


class ExerciseDatabaseDecoder:

    """
     ExerciseDatabaseDecoder - Decodes input json ExerciseDatabase file and creates a ExerciseDatabase class
    """

    common_config_location = PurePath(
        '.', 'user', 'exercises', 'exercises.json')

    def __init__(self):
        pass

    def __validate_exercise(self, exercise_database_object, exercise_object):
        # Validate all fields exist and are valid
        if exercise_object.name == "":
            raise ValueError("Exercise {} needs a name".format(exercise_object.name))
        if exercise_object.description == "":
            raise ValueError("Exercise {} needs a description".format(exercise_object.name))
        if exercise_object.id == "":
            raise ValueError("Exercise {} needs an id".format(exercise_object.id))
        if len(exercise_object.musclegroups) == 0:
            raise ValueError("Exercise {} needs to work one or more muscle groups".format(exercise_object.name))
        if exercise_object.duration == 0 or \
           exercise_object.sets == 0 or \
           exercise_object.setCooldown == 0 or \
           exercise_object.exerciseCooldown == 0 or \
           exercise_object.total_duration == 0:
            raise ValueError("Exercise {} needs non-zero duration and set information".format(exercise_object.name))

        # For now, let's not mandate muscles.
        # if len(exercise_object.muscles) == 0:
            #raise ValueError("Exercise {} needs to work one or more muscles".format(exercise_object.name))

        # Validate against the db for valid muscles and groups
        for muscle in exercise_object.muscles:
            if (not muscle in exercise_database_object.armsmuscles and
               not muscle in exercise_database_object.abdominalsmuscles and
               not muscle in exercise_database_object.legsmuscles):
                raise ValueError("Exercise {} has an invalid muscle: {}".format(exercise_object.name, muscle))

        for musclegroup in exercise_object.musclegroups:
            if not musclegroup in exercise_database_object.musclegroups:
                raise ValueError("Exercise {} has an invalid musclegroup: {}".format(exercise_object.name, musclegroup))

        # Validate against valid equipment
        for equip in exercise_object.equipment:
            if not equip in exercise_database_object.equipment:
                raise ValueError("Exercise {} has an invalid equipment: {}".format(exercise_object.name, equip))

        # Validate against other exercises for unique fields
        for exercise in exercise_database_object.exercises:
            if exercise_object.id == exercise.id:
                raise ValueError("Exercise {} ID already exists".format(exercise_object.name))
            if exercise_object.name == exercise.name:
                raise ValueError("Exercise {} Name already exists".format(exercise_object.name))

    def __decode_exercise_database(self, exercise_database_filename, configuration):
        exercise_database_object = ExerciseDatabase()

        with open(exercise_database_filename) as f:
            exercise_database_json = json.load(f)

            # Defines the "global" allowed set of values, to be used by the exercises
            exercise_database_object.equipment = exercise_database_json["equipment"]
            exercise_database_object.musclegroups = exercise_database_json["musclegroups"]
            exercise_database_object.armsmuscles = exercise_database_json["armsmuscles"]
            exercise_database_object.abdominalsmuscles = exercise_database_json["abdominalsmuscles"]
            exercise_database_object.legsmuscles = exercise_database_json["legsmuscles"]

            exercises_json = exercise_database_json["exercises"]
            for exercise_json in exercises_json:
                exercise_object = Exercise()
                exercise_object.name = exercise_json['name']
                exercise_object.description = exercise_json['description']
                exercise_object.equipment = exercise_json['equipment']
                exercise_object.id = exercise_json['id']
                if 'alternatesidesbetweensets' in exercise_json:
                    exercise_object.alternatesidesbetweensets = exercise_json['alternatesidesbetweensets']
                if 'musclegroups' in exercise_json:
                    exercise_object.musclegroups = exercise_json['musclegroups']
                if 'muscles' in exercise_json:
                    exercise_object.muscles = exercise_json['muscles']

                # If not specified (likely), grab the defaults from the configuration
                if 'duration' in exercise_json:
                    exercise_object.duration = exercise_json['duration']
                else:
                    exercise_object.duration = configuration.decoded_object.ExerciseDurationDefault
                if 'sets' in exercise_json:
                    exercise_object.sets = exercise_json['sets']
                else:
                    exercise_object.sets = configuration.decoded_object.ExerciseSetsDefault
                if 'setCooldown' in exercise_json:
                    exercise_object.setCooldown = exercise_json['setCooldown']
                else:
                    exercise_object.setCooldown = configuration.decoded_object.ExerciseSetCooldownDefault
                if 'exerciseCooldown' in exercise_json:
                    exercise_object.exerciseCooldown = exercise_json['exerciseCooldown']
                else:
                    exercise_object.exerciseCooldown = configuration.decoded_object.ExerciseCooldownDefault

                exercise_object.total_duration = \
                    ((exercise_object.duration + exercise_object.setCooldown) *
                     exercise_object.sets) + \
                    exercise_object.exerciseCooldown

                self.__validate_exercise(exercise_database_object, exercise_object)
                exercise_database_object.exercises.append(exercise_object)

        return exercise_database_object

    def decode_exercise_database(self, exercise_database_filename, configuration):
        return self.__decode_exercise_database(exercise_database_filename, configuration)

    def decode_common_exercise_database(self, configuration):
        return self.decode_exercise_database(self.common_config_location, configuration)
