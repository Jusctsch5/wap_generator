from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

from wap_generator.configuration.configuration_decoder import ConfigurationDecoder
from wap_generator.exercise.exercise_database_decoder import ExerciseDatabaseDecoder
from wap_generator.workout.dynamic_workout_decoder import DynamicWorkoutDecoder


class SelectWorkoutButton(Button):

    def __init__(self, app, filename, **kwargs):
        self.app = app
        self.filename = filename
        super().__init__(**kwargs)

        self.bind(on_press=self.callback)

    def callback(self, instance):
        print('The button %s state is <%s>' % (instance, instance.state))
        self.app.generate_and_play_workout(self.filename)


class UserInterface(App):
    def __init__(self):
        configuration_decoder = ConfigurationDecoder()
        self.configuration = configuration_decoder.decode_common_configuration()
        exercise_decoder = ExerciseDatabaseDecoder()
        self.exercise_database = exercise_decoder.decode_common_exercise_database(self.configuration)
        self.workout_decoder = DynamicWorkoutDecoder()
        super().__init__()

    def build(self):

        workout_layout = BoxLayout(orientation='vertical')
        screen_title = Label(text="Workout Selector")
        workout_layout.add_widget(screen_title)

        files = self.workout_decoder.get_common_workout_files()
        for f in files:
            base_name = str(f).split("\\")[-1]
            btn = SelectWorkoutButton(self, f, text=base_name)
            workout_layout.add_widget(btn)

        return workout_layout

    def generate_and_play_workout(self, workout_file):
        workout = self.workout_decoder.decode_workout(workout_file, self.exercise_database, self.configuration)
        self.configuration.decoded_object.Autoplay = True
        workout.generate_total_clip("", self.configuration)
