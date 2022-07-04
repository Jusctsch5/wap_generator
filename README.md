# Usage

.\workout_env\Scripts\activate

Run one of generate_dynamic_workout, generate_static_workout, or generate_regimen
## generate_dynamic_workout.py
- Consumes a file that describes the details of the dynamic workout, such as the muscle groups to work, the duration, as well as start/end delays.
- Consumes a file that describes all of the exercises to pull from
- Consumes a configuration file that describes other working parameters
- Consumes a playlist file to identify specific songs to pull from
- Generates an mp3 file of the workout or autoplays the result (depending on config option)

## generate_static_workout.py
- Consumes a file that describes each exercise to perform
- Consumes a configuration file that describes other working parameters
- Consumes a playlist file to identify specific songs to pull from
- Generates an mp3 file of the workout or autoplays the result (depending on config option)

## generate_regimen.py
- Consumes a file that describes a series of dynamic workouts for different days of the week.
- Consumes a file that describes all of the exercises to pull from
- Consumes a configuration file that describes other working parameters
- Consumes a playlist file to identify specific songs to pull from
- Generates a directory of files that includes the workouts for each day


## Examples
.\generate_dynamic_workout.py .\user\workout_dynamic\dynamic_workout.json -c .\user\configuration\configuration_jukebox.json -e .\user\exercises\exercises.json

.\generate_dynamic_workout.py .\user\workout_dynamic\dynamic_all_no_suspended_workout.json -c .\user\configuration\configuration_autoplay_no_music.json -e .\user\exercises\exercises.json

.\generate_dynamic_workout.py .\user\workout_dynamic\dynamic_arms_no_suspended_workout.json -c .\user\configuration\configuration_autoplay_no_music.json -e .\user\exercises\exercises.json
