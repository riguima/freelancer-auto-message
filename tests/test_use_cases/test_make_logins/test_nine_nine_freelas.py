import re

import pytest

from cray_freelas_bot.exceptions.project import LoginError
from cray_freelas_bot.use_cases.nine_nine_freelas import NineNineBrowser


@pytest.fixture(scope='module')
def browser() -> NineNineBrowser:
    return NineNineBrowser(user_data_dir='.make_login_user_data', visible=True)


def test_is_logged_without_make_login(browser: NineNineBrowser) -> None:
    assert not browser.is_logged()


def test_make_login_with_invalid_login(browser: NineNineBrowser) -> None:
    with pytest.raises(
        LoginError,
        match=re.compile(r'Email ou senha inválidos'),
    ):
        browser.make_login('richard.alexsander.guima@gmail.com', 'Richard123')


def test_make_login(browser: NineNineBrowser) -> None:
    browser.make_login('miqueiasmartinsoficial@gmail.com', 'Projeto#1bot')
