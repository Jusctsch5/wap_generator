import os

class Workout:

    """
     Workout - Decodes input json workout file and creates a Workout class
    """

    def __init__(self, i_decoded_object):
        self.decoded_object = i_decoded_object
        self.exercises = []
        self.clips = []
        self.total_clip = 0
        self.mp3_filename = ""

    def generate_json():
        pass

    def generate_total_clip(self, output_dir):

        resulting_name = self.decoded_object.name + ".mp3"
        if output_dir == "":
            resulting_name = os.path.join("result", resulting_name)
        else:
            resulting_name = os.path.join(output_dir, resulting_name)

        print("Creating new total workout clip with name: " + resulting_name)
        file_handle = self.total_clip.export(resulting_name, format="mp3")
        self.mp3_filename = resulting_name
