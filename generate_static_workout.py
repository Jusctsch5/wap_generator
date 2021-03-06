 #!python3
import argparse
from wap_generator.workout.workout_decoder import WorkoutDecoder
from wap_generator.configuration.configuration_decoder import ConfigurationDecoder
from wap_generator.playlist.playlist_decoder import PlaylistDecoder
from wap_generator.exercise.exercise_database_decoder import ExerciseDatabaseDecoder

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("workout",                 help="Provide a workout json file ")
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

    workout_decoder = WorkoutDecoder()
    workout = workout_decoder.decode_workout(args.workout, exercise_database, configuration)

    if args.playlist is None:
        workout.generate_total_clip(configuration.decoded_object.OutputDirectory, configuration)
    else:
        playlist_decoder = PlaylistDecoder()
        playlist = playlist_decoder.decode_playlist(args.playlist, configuration)
        playlist.create_combined_clip(workout, configuration.decoded_object.OutputDirectory, configuration)

if __name__ == '__main__':
    main()