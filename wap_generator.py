 #!python3
import argparse
import os
from workout_decoder import WorkoutDecoder
from workout import Workout
from configuration_decoder import ConfigurationDecoder
from configuration import Configuration

def main():
    
    parser = argparse.ArgumentParser()

    parser.add_argument("workout",                 help="Provide a workout json file ")
    parser.add_argument("-c", "--configuration",   help="Provide an optional configuration json file")
    parser.add_argument("-p", "--playlist",        help="Provide an optional playlist json file")
    args = parser.parse_args()
    
    print("Launching WAP Generator with arguments: " + str(args))

    configuration_decoder = ConfigurationDecoder()
    configuration = configuration_decoder.decode_configuration(args.configuration)
    print("Created Configuration: " + str(configuration))

    workout_decoder = WorkoutDecoder()
    workout = workout_decoder.decode_workout(args.workout, configuration)
    print("Created Workout: " + str(workout))

if __name__ == '__main__':
    main()