import os
from announcer_wrapper import AnnouncerWrapper

class Workout:

    """
     Workout - Decodes input json workout file and creates a Workout class
    """

    def __init__(self, i_decoded_object):
        self.decoded_object = i_decoded_object

        # Fields from the decoded object
        self.name = ""
        self.exercises = []
        self.start_delay = 0
        self.finish_delay = 0
        self.total_duration = 0

        # Resulting fields
        self.clips = []
        self.total_clip = None
        self.mp3_filename = ""

    def generate_json():
        pass

    def transform_exercises_to_clip(self, configuration, announcer_wrapper):

        first = True
        for exercise_i in range(0, len(self.exercises)):
            exercise  = self.exercises[exercise_i]
            if first is True:
                # Create announcement of workout
                print("Creating clip for workout: " + self.name)
                total_clip = announcer_wrapper.create_voice_clip("Starting workout:" + self.name + 
                                                                 " in " + str(self.start_delay) + " seconds." +
                                                                 " first exercise will be: " + exercise.name)

                # Create starting delay
                if configuration.decoded_object.ReadDescription == True:
                    total_clip += announcer_wrapper.create_voice_clip_wih_delay_and_countdown(exercise.description, self.start_delay)
                else:   
                    total_clip += announcer_wrapper.create_delay_with_countdown(self.start_delay)
                first = False

            print("Creating clip for exercise: " + exercise.name)

            total_clip += announcer_wrapper.create_voice_clip("Starting exercise:" + exercise.name)

            # Cache these clips over each set, to reduce calls to the wrapper.
            exercise_duration_clip = announcer_wrapper.create_delay_with_countdown(exercise.duration)            
            cooldown_statement_clip = announcer_wrapper.create_voice_clip("Set Cooldown for " + str(exercise.setCooldown) + " seconds.")
            cooldown_duration_clip = announcer_wrapper.create_delay_with_countdown(exercise.setCooldown)

            # Perform an exercise
            for i in range(1, exercise.sets+1):
                
                # Add Exercise
                total_clip += announcer_wrapper.create_voice_clip("Set " + str(i) + ". Ready Go!")                
                total_clip += exercise_duration_clip

                # Transition to the next set of the exercise, if it's not the last set.
                if i != exercise.sets:
                    total_clip = total_clip + cooldown_statement_clip
                    if exercise.alternatesidesbetweensets:
                        total_clip += announcer_wrapper.change_sides
                    total_clip += cooldown_duration_clip

            # If it's not the last exercise in the workout, announce the next one and give an exercise delay
            if exercise_i != len(self.exercises)-1:
                clip = announcer_wrapper.create_voice_clip("Exercise Cooldown for " + str(exercise.exerciseCooldown) + 
                                                                " seconds. Next Exercise will be " + 
                                                                self.exercises[exercise_i+1].name)
                total_clip = total_clip + clip

                # After all sets in the exercise, give a finishing exercise cooldown.
                if configuration.decoded_object.ReadDescription == True:
                    total_clip += announcer_wrapper.create_voice_clip_wih_delay_and_countdown(self.exercises[exercise_i+1].description, exercise.exerciseCooldown)
                else:   
                    total_clip += announcer_wrapper.create_delay_with_countdown(exercise.exerciseCooldown)

        # After all exercises in the workout, give a finishing workout cooldown.
        total_clip += announcer_wrapper.create_voice_clip("Exercises for workout:" + self.name + " Finished. Work it off for " + str(self.finish_delay) + " seconds")
        total_clip += announcer_wrapper.create_delay_with_countdown(self.finish_delay)
        total_clip += announcer_wrapper.create_voice_clip("Your Workout:" + self.name + " Finished. Great job.")

        self.total_clip = total_clip
        return self.total_clip

    def generate_total_clip(self, output_dir):

        resulting_name = self.decoded_object.name + ".mp3"
        if output_dir == "":
            resulting_name = os.path.join("result", resulting_name)
        else:
            resulting_name = os.path.join(output_dir, resulting_name)

        if (os.path.exists(os.path.dirname(resulting_name)) is False):
            os.makedirs(os.path.dirname(resulting_name))
        print("Creating new total workout clip with name: " + resulting_name)
        file_handle = self.total_clip.export(resulting_name, format="mp3")
        self.mp3_filename = resulting_name
