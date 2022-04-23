from typing import Optional

PLAY = [23, 26]
PAUSE = [22]
RESUME = [25]
ZERO = [28]


class Command:
    """
    Command codes and utils.
    """

    @staticmethod
    def get_number(command_id: int) -> Optional[int]:
        """
        Gets number by command code.
        @param command_id: command id
        """
        if command_id >= ZERO:
            return command_id - ZERO

        return None

    @staticmethod
    def is_play(command_id: int) -> bool:
        return command_id in PLAY

    @staticmethod
    def is_pause(command_id: int) -> bool:
        return command_id in PAUSE

    @staticmethod
    def is_resume(command_id: int) -> bool:
        return command_id in RESUME
