import argparse
import os
from wap_generator.announcer.announcer_decoder import AnnouncerDecoder
from wap_generator.workout.dynamic_workout_decoder import DynamicWorkoutDecoder
from wap_generator.configuration.configuration_decoder import ConfigurationDecoder
from wap_generator.playlist.playlist_decoder import PlaylistDecoder
from wap_generator.playlist.playlist import Playlist
from wap_generator.exercise.exercise_database_decoder import ExerciseDatabaseDecoder
from pydub.playback import play
import ffmpeg

import shutil

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("exercise_database",       help="Provide an exercise database ")
    parser.add_argument("-c", "--configuration",   help="Provide an optional configuration json file")
    parser.add_argument("-a", "--announcer",       help="Provide an optional announcer configuration json file")
    args = parser.parse_args()

    print("Launching WAP Generator with arguments: " + str(args))
    
    configuration_decoder = ConfigurationDecoder()
    configuration = configuration_decoder.decode_configuration(args.configuration)

    announcer_decoder = AnnouncerDecoder()
    announcer = announcer_decoder.decode_configuration(args.configuration)

    exercise_database_decoder = ExerciseDatabaseDecoder()
    exercise_database = exercise_database_decoder.decode_exercise_database(args.exercise_database, configuration)

    exercise_duration_clip = announcer.create_delay_with_countdown(30)
    cooldown_statement_clip = announcer.create_voice_clip(f"Set Cooldown for 10 seconds.")
    cooldown_duration_clip = announcer.create_delay_with_countdown(10)

    for exercise in exercise_database.exercises:
        clips = []
        clips.append(announcer.create_voice_clip(f"Next exercise will be {exercise.name}"))
        clips.append(announcer.create_voice_clip(exercise.description))
        for i in range(2):
            set_i = i+1
            clips.append(announcer.create_voice_clip(f"Set {str(set_i)} of 2. Ready Go!"))
            clips.append(exercise_duration_clip)
            clips.append(cooldown_statement_clip)
            clips.append(cooldown_duration_clip)

        total_clip = None
        for clip in clips:
            if total_clip is None:
                total_clip = clip
            else:
                total_clip += clip

        # play(total_clip)
        for group in exercise.musclegroups:
            dir_name = os.path.join("result", group, exercise.name)
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
            file_name = os.path.join(dir_name, f"{exercise.name}.mp3")
            print(file_name)
            total_clip.export(file_name, format="mp3")
            sm_name = os.path.join(dir_name, f"{exercise.name}.sm")
            shutil.copyfile("template.sm", sm_name)

            with open(sm_name, 'r') as file:
                filedata = file.read()

            duration = str(int(total_clip.duration_seconds))
            
            filedata = filedata.replace('$exercise_name', exercise.name)
            filedata = filedata.replace('$exercise_group', group)
            filedata = filedata.replace('$exercise_mp3', f"{exercise.name}.mp3")
            filedata = filedata.replace('$exercise_length_seconds', duration)

            # Write the file out again
            with open(sm_name, 'w') as file:
                file.write(filedata)


if __name__ == '__main__':
    main()
