import os
from time import sleep
import vlc

DB_PATH = 'DB'

class AudioPlayer:
    """
    Audio player for webm (based on VLC).
    """

    def __init__(self):
        self.media = None
        self.is_pause = False

    def play_db_path(self, db_path: str) -> None:
        """
        Plays the media file with VLC player.
        @param db_path: path for the file cache.
        """
        if os.path.exists(db_path):
            if self.media is not None:
                self.media.stop()
                self.is_pause = False

            self.media = vlc.MediaPlayer(db_path)
            self.media.play()
            sleep(0.1)

    def pause(self) -> None:
        """
        Pauses current file playback (if exists).
        """
        if self.media is not None:
            if not self.is_pause:
                self.is_pause = True
                self.media.pause()

    def resume(self) -> None:
        """
        Resumes current file playback (if exists).
        """
        if self.media is not None:
            if self.is_pause:
                self.is_pause = False
                self.media.pause()
