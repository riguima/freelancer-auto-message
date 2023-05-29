import re

import pytest

from cray_freelas_bot.exceptions.project import LoginError
from cray_freelas_bot.use_cases.workana import WorkanaBrowser


@pytest.fixture(scope='module')
def browser() -> WorkanaBrowser:
    return WorkanaBrowser(visible=True)


def test_is_logged_without_make_login(browser: WorkanaBrowser) -> None:
    assert not browser.is_logged()


def test_make_login_with_invalid_login(browser: WorkanaBrowser) -> None:
    with pytest.raises(
        LoginError,
        match=re.compile(r'Email ou senha inválidos'),
    ):
        browser.make_login('richard.alexsander.guima@gmail.com', 'Richard123')


def test_make_login(browser: WorkanaBrowser) -> None:
    browser.make_login('craybrasil@gmail.com', 'Projeto#1bot')
