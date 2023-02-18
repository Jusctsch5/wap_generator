import threading
from pydub.playback import play


def run_player(player):
    print("I'm playing here!")
    print(player)
    if not player.run:
        return

    print("I'm playing here!")
    play(player.clip)


def run_player2(player):
    print(player)
    for clip in player.clips:
        play(clip)


def abort_player(player):
    pass


class Player:

    def __init__(self):
        self.run = True
        pass

    def play(self, clip):
        self.clip = clip
        threading.Thread(target=run_player, args=(self,)).start()

    def play_clips(self, clips):
        self.clips = clips
        for clip in clips:
            self.clip = clip
            threading.Thread(target=run_player, args=(self,)).start()

    def abort(self):
        self.run = False
