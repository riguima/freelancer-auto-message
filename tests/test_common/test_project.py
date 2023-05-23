from datetime import time

from cray_freelas_bot.common.project import get_greeting_according_time


def test_get_greeting_according_time() -> None:
    assert get_greeting_according_time(time(9, 30, 0)) == 'Bom dia'
    assert get_greeting_according_time(time(2, 30, 0)) == 'Bom dia'
    assert get_greeting_according_time(time(12, 0, 0)) == 'Boa tarde'
    assert get_greeting_according_time(time(19, 45, 0)) == 'Boa noite'
