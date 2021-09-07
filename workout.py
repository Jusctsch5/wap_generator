
class Workout:

    """
     Workout - Decodes input json workout file and creates a Workout class
    """

    def __init__(self, i_decoded_object):
        self.decoded_object = i_decoded_object

        self.clips = []
        self.mp3_filename = ""
