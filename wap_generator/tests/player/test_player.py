import pytest
from pydub import AudioSegment

from wap_generator.player.player import Player

from pathlib import PurePath

sample_path = PurePath('.', 'tests', 'player', 'sample.mp3')


def test_player():
    player = Player()
    clip = AudioSegment.from_file(sample_path)
    clips = [clip, clip]
    print("Going to play clips")
    player.play_clips(clips)
    print("Player run")
    player.abort()
    print("Aborted")
    # player.pause()
