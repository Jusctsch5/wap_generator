import logging
import os
from wap_generator.announcer.announcer import Announcer
from pydub.playback import play


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
        self.muscle_groups = []

        # Resulting fields
        self.clips = []
        # self.total_clip = None
        self.mp3_filename = ""

    def generate_json():
        pass

    def transform_exercises_to_clip(self, configuration, announcer):

        self.clips.clear()
        clips = []

        # Create announcement of workout
        exercise = self.exercises[0]
        logging.info(f"Creating clip for workout:{self.name} ")
        clips.append(announcer.create_voice_clip(f"Starting workout:{self.name}" +
                                                 f" in {str(self.start_delay)} seconds." +
                                                 f" first exercise will be {exercise.name}"))

        # Create starting delay
        if configuration.decoded_object.ReadDescription == True:
            clips.append(announcer.create_voice_clip_wih_delay_and_countdown(exercise.description, self.start_delay))
        else:
            clips.append(announcer.create_delay_with_countdown(self.start_delay))

        for exercise_i in range(0, len(self.exercises)):
            exercise = self.exercises[exercise_i]

            logging.info(f"Creating clip for exercise:{exercise.name}")

            clips.append(announcer.create_voice_clip("Starting exercise:" + exercise.name))

            # Cache these clips over each set, to reduce calls to the wrapper.
            exercise_duration_clip = announcer.create_delay_with_countdown(exercise.duration)
            cooldown_statement_clip = announcer.create_voice_clip(f"Set Cooldown for {str(exercise.setCooldown)} seconds.")
            cooldown_duration_clip = announcer.create_delay_with_countdown(exercise.setCooldown)

            # Perform an exercise
            for i in range(1, exercise.sets+1):

                # Add Exercise
                clips.append(announcer.create_voice_clip(f"Set {str(i)}. Ready Go!"))
                clips.append(exercise_duration_clip)

                # Transition to the next set of the exercise, if it's not the last set.
                if i != exercise.sets:
                    clips.append(cooldown_statement_clip)
                    if exercise.alternatesidesbetweensets:
                        clips.append(announcer.change_sides)
                    clips.append(cooldown_duration_clip)

            # If it's not the last exercise in the workout, announce the next one and give an exercise delay
            if exercise_i != len(self.exercises)-1:
                clips.append(
                    announcer.create_voice_clip(f"Exercise Cooldown for {str(exercise.exerciseCooldown)} seconds." +
                                                f"The next Exercise will be {self.exercises[exercise_i+1].name}"))

                # After all sets in the exercise, give a finishing exercise cooldown.
                if configuration.decoded_object.ReadDescription == True:
                    clips.append(announcer.create_voice_clip_wih_delay_and_countdown(self.exercises[exercise_i+1].description, exercise.exerciseCooldown))
                else:
                    clips.append(announcer.create_delay_with_countdown(exercise.exerciseCooldown))

        # After all exercises in the workout, give a finishing workout cooldown.
        clips.append(announcer.create_voice_clip(f"Exercises for workout:{self.name}. Finished." +
                                                 f"Work it off for {str(self.finish_delay)} seconds"))
        clips.append(announcer.create_delay_with_countdown(self.finish_delay))
        clips.append(announcer.create_voice_clip(f"Your Workout {self.name} Finished. Great job."))

        self.clips.extend(clips)
        return self.clips

    def generate_total_clip(self, output_dir, configuration):

        total_clip = None
        for clip in self.clips:
            if total_clip is None:
                total_clip = clip
            else:
                total_clip += clip

        resulting_name = self.decoded_object.name + ".mp3"
        if output_dir == "":
            resulting_name = os.path.join("result", resulting_name)
        else:
            resulting_name = os.path.join(output_dir, resulting_name)

        if (os.path.exists(os.path.dirname(resulting_name)) is False):
            os.makedirs(os.path.dirname(resulting_name))

        logging.info("Creating new total workout clip with name: " + resulting_name)
        if configuration.decoded_object.Autoplay:
            play(total_clip)
        else:
            file_handle = total_clip.export(resulting_name, format="mp3")
