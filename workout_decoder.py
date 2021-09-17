from exercise import Exercise
from workout import Workout
from announcer_wrapper import AnnouncerWrapper
from types import SimpleNamespace
import json
from pydub import AudioSegment
import random

class WorkoutDecoder:

    """
     WorkoutDecoder - Decodes input json workout file and creates a Workout class
    """

    def __init__(self):
        self.announcer_wrapper = AnnouncerWrapper()

    def __decode_workout(self, workout_filename, exercise_database, configuration):
        self.announcer_wrapper.configure(configuration)

        with open(workout_filename) as f:
            x = json.load(f, object_hook=lambda d: SimpleNamespace(**d))

        workout = Workout(x)

        # If specified, shuffle the provided exercises
        if configuration.decoded_object.ShuffleExercises:
            random.shuffle(workout.decoded_object.exercises)


        """
        Examples of Schema:

        Schema 1:
        Exercise is defined in entirity. Exercise DB is not required. 
        "exercises": [
            {
                "name": "Hex Squats",
                "description": "Standing up straight with arms at sides. Hook bands on feet. Bend knees to chair position and back.",
                "duration": 30,
                "sets": 3,
                "setCooldown": 10,
                "exerciseCooldown": 30
            },
        ]

        Schema 2:
        Drops the information about the exercise, use ID to look up the exercise.
        Information like muscle groups, muscles, description, switch sides, are in the exercise db.
        Information pertaining to duration and sets is contained here.
        "exercises": [
            {
                "id": "3d7f94b9-344e-47b7-a2f0-770cf49e8718",
                "duration": 30,
                "sets": 2,
                "setCooldown": 10,
                "exerciseCooldown": 30
            }
        ]

        Schema 1 will likely be deprecated, however no code below will have to change.
        """
        
        total_clip = AudioSegment.empty()

        # Loop over exercises and create voice clips introducing them
        first = True
        for exercise_i in range(0, len(workout.decoded_object.exercises)):

            # If the ID is supplied, then fill out the rest from the database.
            exercise_json = workout.decoded_object.exercises[exercise_i]
            print(exercise_json)
            exercise = Exercise()
            exercise.id = exercise_json.id
            exercise.duration = exercise_json.duration
            exercise.sets = exercise_json.sets
            exercise.setCooldown = exercise_json.setCooldown
            exercise.exerciseCooldown = exercise_json.exerciseCooldown
            if exercise.id:
                exercise = exercise_database.create_populated_exercise_from_db(exercise)

            if first is True:
                # Create announcement of workout
                print("Creating workout: " + workout.decoded_object.name)
                total_clip = self.announcer_wrapper.create_voice_clip("Starting workout:" + workout.decoded_object.name + 
                                                                    " in " + str(workout.decoded_object.startDelay) + " seconds." +
                                                                    " first exercise will be: " + exercise.name)

                # Create starting delay
                if configuration.decoded_object.ReadDescription == True:
                    total_clip += self.announcer_wrapper.create_voice_clip_wih_delay_and_countdown(exercise.description, workout.decoded_object.startDelay)
                else:   
                    total_clip += self.announcer_wrapper.create_delay_with_countdown(workout.decoded_object.startDelay)
                first = False

            print("Creating exercise: " + exercise.name)

            total_clip += self.announcer_wrapper.create_voice_clip("Starting exercise:" + exercise.name)

            # Cache these clips over each set, to reduce calls to the wrapper.
            exercise_duration_clip = self.announcer_wrapper.create_delay_with_countdown(exercise.duration)            
            cooldown_statement_clip = self.announcer_wrapper.create_voice_clip("Set Cooldown for " + str(exercise.setCooldown) + " seconds.")
            cooldown_duration_clip = self.announcer_wrapper.create_delay_with_countdown(exercise.setCooldown)

            # Perform an exercise
            for i in range(1, exercise.sets+1):
                
                # Add Exercise
                total_clip += self.announcer_wrapper.create_voice_clip("Set " + str(i) + ". Ready Go!")                
                total_clip += exercise_duration_clip

                # Transition to the next set of the exercise, if it's not the last set.
                if i != exercise.sets:
                    total_clip = total_clip + cooldown_statement_clip
                    if exercise.alternatesidesbetweensets:
                        total_clip += self.announcer_wrapper.change_sides
                    total_clip += cooldown_duration_clip

            # If it's not the last exercise in the workout, announce the next one and give an exercise delay
            if exercise_i != len(workout.decoded_object.exercises)-1:
                clip = self.announcer_wrapper.create_voice_clip("Exercise Cooldown for " + str(exercise.exerciseCooldown) + 
                                                                " seconds. Next Exercise will be " + 
                                                                workout.decoded_object.exercises[exercise_i+1].name)
                total_clip = total_clip + clip

                # After all sets in the exercise, give a finishing exercise cooldown.
                if configuration.decoded_object.ReadDescription == True:
                    total_clip += self.announcer_wrapper.create_voice_clip_wih_delay_and_countdown(workout.decoded_object.exercises[exercise_i+1].description, exercise.exerciseCooldown)
                else:   
                    total_clip += self.announcer_wrapper.create_delay_with_countdown(exercise.exerciseCooldown)

        # After all exercises in the workout, give a finishing workout cooldown.
        total_clip += self.announcer_wrapper.create_voice_clip("Exercises for workout:" + workout.decoded_object.name + " Finished. Work it off for " + str(workout.decoded_object.finishDelay) + " seconds")
        total_clip += self.announcer_wrapper.create_delay_with_countdown(workout.decoded_object.finishDelay)
        total_clip += self.announcer_wrapper.create_voice_clip("Your Workout:" + workout.decoded_object.name + " Finished. Great job.")


        workout.total_clip = total_clip
        return workout

    def decode_workout(self, workout_filename, exercise_database, configuration):
        return self.__decode_workout(workout_filename, exercise_database, configuration)
