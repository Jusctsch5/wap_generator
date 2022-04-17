from regimen import Regimen
from regimen import Day
from types import SimpleNamespace
import json
from wap_generator.workout.dynamic_workout_decoder import DynamicWorkoutDecoder


class RegimenDecoder:

    """
     RegimenDecoder - Decodes input json Regimen file and creates a Regimen class
    """

    def __init__(self):
        pass

    def __decode_regimen(self, regimen_filename, exercise_database, configuration):
        with open(regimen_filename) as f:
            x = json.load(f, object_hook=lambda d: SimpleNamespace(**d))

        regimen_namespace = x

        regimen = Regimen(x)
        dynamicWorkoutDecoder = DynamicWorkoutDecoder()
        print(regimen_namespace)
        index = 0
        for day_namespace in regimen_namespace.days:
            index = index + 1
            day = Day()
            day.name = "{} {}".format(index, day_namespace.name)
            print("Creating workouts for day: {}".format(day.name))
            for workout_namespace in day_namespace.workouts:
                workout_namespace.name = "{} {}".format(
                    day_namespace.name, workout_namespace.name)
                workout = dynamicWorkoutDecoder.decode_workout_json(
                    workout_namespace, exercise_database, configuration)
                day.workouts.append(workout)
            regimen.days.append(day)

        return regimen

    def decode_regimen(self, regimen_filename, exercise_database, configuration):
        return self.__decode_regimen(regimen_filename, exercise_database, configuration)
