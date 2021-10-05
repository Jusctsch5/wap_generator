 #!python3
import argparse
import os
from dynamic_workout_decoder import DynamicWorkoutDecoder
from workout_decoder import WorkoutDecoder
from workout import Workout
from configuration_decoder import ConfigurationDecoder
from configuration import Configuration
from playlist_decoder import PlaylistDecoder
from playlist import Playlist
from exercise_database_decoder import ExerciseDatabaseDecoder
from exercise_database import ExerciseDatabase

def main():
    
    parser = argparse.ArgumentParser()

    parser.add_argument("workout",                 help="Provide a dynamic workout json file ")
    parser.add_argument("-c", "--configuration",   help="Provide an optional configuration json file")
    parser.add_argument("-p", "--playlist",        help="Provide an optional playlist json file")
    parser.add_argument("-e", "--exercise-database",      help="Provide an optional exercise database")
    args = parser.parse_args()
    
    print("Launching WAP Generator with arguments: " + str(args))

    configuration_decoder = ConfigurationDecoder()
    configuration = configuration_decoder.decode_configuration(args.configuration)

    if args.exercise_database:
        exercise_database_decoder = ExerciseDatabaseDecoder()
        exercise_database = exercise_database_decoder.decode_exercise_database(args.exercise_database, configuration)

    workout_decoder = DynamicWorkoutDecoder()
    workout = workout_decoder.decode_workout(args.workout, exercise_database, configuration)
    workout.generate_total_clip(configuration.decoded_object.OutputDirectory)

    if args.playlist:
        playlist_decoder = PlaylistDecoder()
        playlist = playlist_decoder.decode_playlist(args.playlist, configuration)
    elif configuration.decoded_object.CreatePlaylistFromDirectory is True:
        playlist = Playlist(None)
        playlist.create_playlist_from_directory = configuration.decoded_object.CreatePlaylistFromDirectory
    if playlist is not None:
        playlist.create_combined_clip(workout, configuration.decoded_object.OutputDirectory, configuration)

if __name__ == '__main__':
    main()