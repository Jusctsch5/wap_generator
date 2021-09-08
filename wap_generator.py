 #!python3
import argparse
import os
from workout_decoder import WorkoutDecoder
from workout import Workout
from configuration_decoder import ConfigurationDecoder
from configuration import Configuration
from playlist_decoder import PlaylistDecoder
from playlist import Playlist

def main():
    
    parser = argparse.ArgumentParser()

    parser.add_argument("workout",                 help="Provide a workout json file ")
    parser.add_argument("-c", "--configuration",   help="Provide an optional configuration json file")
    parser.add_argument("-p", "--playlist",        help="Provide an optional playlist json file")
    args = parser.parse_args()
    
    print("Launching WAP Generator with arguments: " + str(args))

    configuration_decoder = ConfigurationDecoder()
    configuration = configuration_decoder.decode_configuration(args.configuration)

    workout_decoder = WorkoutDecoder()
    workout = workout_decoder.decode_workout(args.workout, configuration)
    workout.generate_total_clip(configuration.decoded_object.OutputDirectory)

    if args.playlist:
        playlist_decoder = PlaylistDecoder()
        playlist = playlist_decoder.decode_playlist(args.playlist, configuration)
        playlist.create_combined_clip(workout, configuration)

if __name__ == '__main__':
    main()