import logging
import random
import pyttsx3
import uuid
import os.path
import glob
from pydub import AudioSegment
import os


class Announcer:

    """
     Announcer - Wrap around whatever python library used for tts and give interfaces
                        that can be used by the decoders.
    """

    def __init__(self, volume=1.0, random_voice=False, voice_name=""):
        self.engine = pyttsx3.init()
        self.session_uuid = uuid.uuid4()
        self.clip_index = 0
        self.countdown_five = None
        self.change_sides = None
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.samples_dir = os.path.join(self.path, "samples")
        self.temp_dir = os.path.join(self.path, "temp")
        self.volume = volume
        self.random_voice = random_voice
        self.voice_name = voice_name

    def __get_short_uuid_str(self):
        return str(self.session_uuid).split('-')[0]

    def configure(self):
        logging.debug(f"Configure AudioSegment with ffmpeg:{self.path}")
        AudioSegment.ffmpeg = self.path

        # Configure the text-to-speech engine
        self.engine.setProperty('volume', self.volume)
        self.engine.setProperty('rate', 145)  # default 200

        # Cache voice clips with desired announcer for better performance.
        name = os.path.join(self.samples_dir, "countdown_five.mp3")

        # Try dynamically generating countdown with reasonable tempo
        total_clip = 0
        for i in range(5, 0, -1):
            self.engine.save_to_file(str(i), name)
            self.engine.runAndWait()
            clip = AudioSegment.from_file(name)
            total_clip += clip
        self.countdown_five = total_clip

        # Generate canned phrase for changing sides.
        name = os.path.join(self.samples_dir, "change_sides.mp3")
        self.engine.save_to_file("change sides", name)
        self.engine.runAndWait()
        self.change_sides = AudioSegment.from_file(name)

        voices = self.engine.getProperty('voices')
        logging.debug("Provided voices from OS:")
        for voice in voices:
            logging.debug(voice.__dict__)

        if self.voice_name:
            found = False
            for voice in voices:
                if self.voice_name.lower() in voice.name.lower():
                    logging.debug(f"Setting voice to {voice.name}")
                    self.engine.setProperty('voice', voice.id)
                    found = True
                    break
            if found is False:
                logging.debug(f"Couldn't find desired voice{self.voice_name}. Defaulting to system default voice {voices[0].name}")
        elif self.random_voice:
            rand_voice = random.choice(voices)
            logging.debug(f"Setting voice randomly to {voice.name}")
            self.engine.setProperty('voice', rand_voice.id)
        else:
            logging.debug(f"Defaulting to system default voice {voices[0].name}")

    def create_voice_clip(self, clip):

        # Make unique filename for voice clip
        name = str(self.session_uuid).split('-')[0] + "_" + str(self.clip_index) + ".mp3"
        name = os.path.join(self.temp_dir, name)

        self.engine.save_to_file(clip, name)
        self.engine.runAndWait()

        path = os.path.dirname(os.path.abspath(__file__))
        name = os.path.join(path, name)

        # logging.debug("Creating new voiceclip with name: " + name)
        clip = AudioSegment.from_file(name)
        self.clip_index = self.clip_index + 1

        return clip

    def create_delay_with_countdown(self, duration_seconds):

        # countdown takes a little time, so let's remove some delay if the asked duration is greater.
        if duration_seconds > self.countdown_five.duration_seconds:
            duration_seconds -= self.countdown_five.duration_seconds

        clip = AudioSegment.silent(duration=duration_seconds * 1000)
        return clip + self.countdown_five

    def create_voice_clip_wih_delay_and_countdown(self, clip, duration_seconds):
        # Create a voice clip based on the input, and use that duration to subtract from the delay to add.
        clip = self.create_voice_clip(clip)

        # Again, be mindful how much text is passed in. It could be longer than the delay.
        # If so, give us a tiny delay.
        if duration_seconds > clip.duration_seconds:
            duration_seconds -= clip.duration_seconds
        else:
            duration_seconds = 1

        # Generate delay and add to voice clip
        clip += self.create_delay_with_countdown(duration_seconds)
        return clip

    def generate_total_clip(self, total_clip, name, output_dir):

        resulting_name = str(self.session_uuid).split('-')[0] + "_" + name + ".mp3"
        if output_dir == "":
            resulting_name = os.path.join("result", resulting_name)
        else:
            resulting_name = os.path.join(output_dir, resulting_name)

        logging.debug("Creating new total workout clip with name: " + resulting_name)
        file_handle = total_clip.export(resulting_name, format="mp3")
        return resulting_name
