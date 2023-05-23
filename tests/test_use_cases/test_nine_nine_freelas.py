import pytest
import json
from datetime import datetime
from random import randint

from cray_freelas_bot.use_cases.nine_nine_freelas import NineNineBrowser
from cray_freelas_bot.common.driver import create_driver
from cray_freelas_bot.common.project import get_greeting_according_time
from cray_freelas_bot.domain.models import Project
from cray_freelas_bot.exceptions.nine_nine_freelas import (
    UnreleasedProjectError
)


@pytest.fixture(scope='module')
def browser() -> NineNineBrowser:
    return NineNineBrowser(create_driver(visible=True))


@pytest.fixture(scope='module')
def login(browser) -> bool:
    return browser.make_login(
        'miqueiasmartinsoficial@gmail.com', 'Projeto#1bot'
    )


def test_make_login(browser: NineNineBrowser, login: bool) -> None:
    assert login


def test_get_all_categories(browser: NineNineBrowser, login: bool) -> None:
    expected = json.load(
        open('tests/test_use_cases/nine_nine_categories.json', 'r')
    )
    assert browser.get_all_categories() == expected


def test_get_account_name(browser: NineNineBrowser, login: bool) -> None:
    assert browser.get_account_name() == 'Miqueias Martin'


def test_get_project(browser: NineNineBrowser, login: bool) -> None:
    expected = Project(
        category='Engenharia & Arquitetura',
        client_name='Emerson L.',
        name='Transformar loja em casa residencial',
        url='https://www.99freelas.com.br/project/transformar-loja-em-casa-residencial-437559?fs=t',
    )
    assert browser.get_project(
        'https://www.99freelas.com.br/project/transformar-loja-em-casa-residencial-437559?fs=t'
    ) == expected


def test_get_project_with_invalid_url(browser: NineNineBrowser, login: bool) -> None:
    with pytest.raises(ValueError):
        browser.get_project(
            'https://www.99freelas.com.br/project/trdial-4459?fs=t'
        )


def test_get_project_with_unreleased_project(browser: NineNineBrowser, login: bool) -> None:
    with pytest.raises(UnreleasedProjectError):
        url = browser.get_projects('Engenharia & Arquitetura')[0].url
        browser.get_project(url)


def test_get_projects(browser: NineNineBrowser, login: bool) -> None:
    category = 'Engenharia & Arquitetura'
    projects = browser.get_projects(category, page=4)
    assert len(projects) == 10


def test_get_projects_with_invalid_category(browser: NineNineBrowser, login: bool) -> None:
    with pytest.raises(ValueError):
        browser.get_projects('Limpeza', page=1)


def test_send_message(browser: NineNineBrowser, login: bool) -> None:
    project = browser.get_projects(
        'Web, Mobile & Software', page=randint(20, 30)
    )[randint(0, 9)]
    message = (
        f'{get_greeting_according_time(datetime.now().time())} '
        f'{project.client_name}, tudo bem?\n'
        f'Ao ler sobre o seu projeto "{project.name}", percebi que ele está '
        f'alinhado com a minha expertise em {project.category}, gostaria de '
        'saber qual o seu prazo ideal para a conclusão do projeto e se você '
        'possui algum detalhe em específico que considera fundamental?\n'
        f'ass: {browser.get_account_name()}'
    )
    browser.send_message(project.url, message)
    assert browser.get_last_message() == message
