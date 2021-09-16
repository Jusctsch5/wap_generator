from types import SimpleNamespace
import json

class Exercise:

    """
     Exercise - 
    """

    def __init__(self):
        self.name = ""
        self.description = ""
        self.id = ""
        self.alternatesidesbetweensets = False
        self.musclegroups = []
        self.muscles = []
        self.duration = 0
        self.sets = 0
        self.setCooldown = 0
        self.exerciseCooldown = 0
