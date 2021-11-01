import random

class ExerciseDatabase:

    """
     ExerciseDatabase
    """

    def __init__(self):
        self.exercises = []
        self.musclegroups = []
        self.armsmuscles = []
        self.abdominalsmuscles = []
        self.legsmuscles = []

    def __get_exercise_from_id(self, id):
        for exercise_entry in self.exercises:
            if exercise_entry.id == id:
                return exercise_entry
        return None
    
    def create_populated_exercise_from_db(self, exercise):
        exercise_from_db = self.__get_exercise_from_id(exercise.id)
        if exercise_from_db:
            exercise.name = exercise_from_db.name
            exercise.description = exercise_from_db.description
            exercise.alternatesidesbetweensets = exercise_from_db.alternatesidesbetweensets
            exercise.equipment = exercise_from_db.equipment
            exercise.musclegroups = exercise_from_db.musclegroups
            exercise.armsmuscles = exercise_from_db.armsmuscles
            exercise.abdominalsmuscles = exercise_from_db.abdominalsmuscles
            exercise.legsmuscles = exercise_from_db.legsmuscles

        return exercise

    def get_exercises_from_filter(self, filter):
        exercises = []

        for exercise in self.exercises:

            # Make sure a muscle matches, if provided in the filter
            match = False
            if filter.muscle != None:
                if filter.muscle in exercise.muscles:
                    match = True
            else:
                match = True
            if match is False:
                print("Did not match exercise: {} based on muscle filter: {}".format(exercise.name, filter.muscle))
                continue

            # Make sure a muscle group matches, if provided in the filter
            match = False
            if len(filter.musclegroup) > 0:
                for musclegroup in filter.musclegroup:
                    if musclegroup in exercise.musclegroups:
                        match = True
                        break
            else:
                match = True
            if match is False:
                print("Did not match exercise: {} based on muscle group filter: {}".format(exercise.name, filter.musclegroup))
                continue

            # Make sure an equipment matches, if provided in the filter
            match = False
            if len(filter.equipment) > 0:
                for equipment in filter.equipment:
                    if equipment in exercise.equipment:
                        match = True
                        break
            else:
                match = True
            if match is False:
                print("Did not match exercise: {} based on equipment filter: {}".format(exercise.name, filter.equipment))
                continue

            exercises.append(exercise)

        return exercises

    def get_exercises_from_muscle_group(self, musclegroup):
        exercises = []
        for exercise in self.exercises:
            if musclegroup in exercise.musclegroups:
                exercises.append(exercise)

        return exercises

    def get_exercises_from_muscle_groups(self, musclegroups):
        exercises = []
        for musclegroup in musclegroups:
            returned_exercises = self.get_exercises_from_muscle_group(musclegroup)
            exercises.extend(x for x in returned_exercises if x not in exercises)
        return exercises

    def get_exercises_for_muscle(self, muscle):
        exercises_for_muscle = []
        for exercise in self.exercises:
            if muscle in exercise.muscles:
                exercises_for_muscle.append(exercise)

        return exercises_for_muscle            

    def get_muscles_in_muscle_group(self, musclegroup):
        if musclegroup == "arms" : return self.armsmuscles
        if musclegroup == "legs" : return self.legsmuscles
        if musclegroup == "abdominals" : return self.abdominalsmuscles
        return None      

    def get_new_exercise_helper(self, exercises, excluded_exercises):
        if len(exercises) == 0:
            print("No exercises passed in")
            return None

        random.shuffle(exercises)

        for exercise in exercises:
            foundNewOne = True
            for existing_exercise in excluded_exercises:
                if exercise.id == existing_exercise.id: 
                    foundNewOne = False
                    break
            if foundNewOne is True:
                return exercise


        print("Unable to find new exercise. Using {} instead".format(exercise.name))
        return exercise

        
