class ExerciseDatabaseFilter:

    """
     ExerciseDatabaseFilter - 
     Treat everything as an "And" filter for now
    """

    def __init__(self, muscle, musclegroup, equipment):
        
        self.muscle = muscle
        self.musclegroup = musclegroup
        self.equipment = equipment