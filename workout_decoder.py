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

    def __decode_workout(self, workout_filename, configuration):
        self.announcer_wrapper.configure(configuration)

        with open(workout_filename) as f:
            x = json.load(f, object_hook=lambda d: SimpleNamespace(**d))

        workout = Workout(x)

        # If specified, shuffle the provided exercises
        if configuration.decoded_object.ShuffleExercises:
            random.shuffle(workout.decoded_object.exercises)

        # Create announcement of workout
        print("Creating workout: " + workout.decoded_object.name)
        total_clip = self.announcer_wrapper.create_voice_clip("Starting workout:" + workout.decoded_object.name + 
                                                              " in " + str(workout.decoded_object.startDelay) + " seconds." +
                                                              " first exercise will be: " + workout.decoded_object.exercises[0].name)


        # Create starting delay
        if configuration.decoded_object.ReadDescription == True:
            total_clip += self.announcer_wrapper.create_voice_clip_wih_delay_and_countdown(workout.decoded_object.exercises[0].description, workout.decoded_object.startDelay)
        else:   
            total_clip += self.announcer_wrapper.create_delay_with_countdown(workout.decoded_object.startDelay)

        # Loop over exercises and create voice clips introducing them
        for exercise_i in range(0, len(workout.decoded_object.exercises)):
            exercise = workout.decoded_object.exercises[exercise_i]
            print("Creating exercise: " + exercise.name)
            total_clip += self.announcer_wrapper.create_voice_clip("Starting exercise:" + exercise.name)

            # Cache these clips over each set, to reduce calls to the wrapper.
            exercise_duration_clip = self.announcer_wrapper.create_delay_with_countdown(exercise.duration)            
            cooldown_statement_clip = self.announcer_wrapper.create_voice_clip("Set Cooldown for " + str(exercise.setCooldown) + " seconds.")
            cooldown_duration_clip = self.announcer_wrapper.create_delay_with_countdown(exercise.setCooldown)

            for i in range(1, exercise.sets+1):
                clip = self.announcer_wrapper.create_voice_clip("Set " + str(i) + ". Ready Go!")
                total_clip = total_clip + clip
                
                # Add cooldown duration, cooldown statement, and cooldown duration clip
                total_clip = total_clip + exercise_duration_clip
                if i != exercise.sets:
                    total_clip = total_clip + cooldown_statement_clip
                    total_clip = total_clip + cooldown_duration_clip

            # If it's not the last exercise, announce the next one and give an exercise delay
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

        self.announcer_wrapper.generate_total_clip(total_clip, workout.decoded_object.name)

        return workout

    def decode_workout(self, workout_filename, configuration):
        return self.__decode_workout(workout_filename, configuration)
