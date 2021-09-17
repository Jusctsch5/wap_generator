
class ExerciseDatabase:

    """
     ExerciseDatabase
    """

    def __init__(self):
        self.exercises = []

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
            exercise.musclegroups = exercise_from_db.musclegroups
            exercise.muscles = exercise_from_db.muscles
        return exercise
