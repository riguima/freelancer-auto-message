import json
import re
from datetime import datetime
from random import randint

import pytest
from selenium.webdriver import Chrome

from cray_freelas_bot.common.driver import find_elements
from cray_freelas_bot.common.project import get_greeting_according_time
from cray_freelas_bot.domain.models import Project
from cray_freelas_bot.exceptions.project import (
    CategoryError,
    LoginError,
    ProjectError,
)
from cray_freelas_bot.use_cases.nine_nine_freelas import NineNineBrowser


@pytest.fixture(scope='module')
def browser() -> NineNineBrowser:
    return NineNineBrowser(user_data_dir='default_user_data', visible=True)


@pytest.fixture(scope='module')
def driver(browser: NineNineBrowser) -> Chrome:
    return browser.driver


def test_make_login_with_invalid_login() -> None:
    browser = NineNineBrowser(user_data_dir='tests_user_data', visible=True)
    with pytest.raises(
        LoginError,
        match=re.compile(r'Email ou senha inválidos'),
    ):
        browser.make_login('richard.alexsander.guima@gmail.com', 'Richard123')


def test_make_login() -> None:
    browser = NineNineBrowser(user_data_dir='tests_user_data', visible=True)
    browser.make_login('miqueiasmartinsoficial@gmail.com', 'Projeto#1bot')


def test_get_all_categories(browser: NineNineBrowser) -> None:
    expected = json.load(
        open('tests/test_utils/nine_nine_categories.json', 'r')
    )
    assert browser.get_all_categories() == expected


def test_get_account_name(browser: NineNineBrowser) -> None:
    assert browser.get_account_name() == 'Miqueias Martin'


def test_get_project(browser: NineNineBrowser) -> None:
    url = (
        'https://www.99freelas.com.br/project/'
        'transformar-loja-em-casa-residencial-437559?fs=t'
    )
    expected = Project(
        category='Engenharia & Arquitetura',
        client_name='Emerson L.',
        name='Transformar loja em casa residencial',
        url=url,
    )
    assert browser.get_project(url) == expected


def test_get_project_with_invalid_url(browser: NineNineBrowser) -> None:
    with pytest.raises(
        ProjectError,
        match=re.compile(r'O projeto não existe'),
    ):
        browser.get_project(
            'https://www.99freelas.com.br/project/trdial-4459?fs=t'
        )


def test_get_project_with_unreleased_project(browser: NineNineBrowser) -> None:
    with pytest.raises(
        ProjectError,
        re.compile(r'Projeto ainda não está disponivel para mandar mensagens'),
    ):
        url = browser.get_projects_urls('Engenharia & Arquitetura')[0].url
        browser.get_project(url)


def test_get_projects_urls(browser: NineNineBrowser) -> None:
    category = 'Engenharia & Arquitetura'
    urls = browser.get_projects_urls(category, page=4)
    assert len(urls) == 10


def test_get_projects_urls_with_invalid_category(
    browser: NineNineBrowser,
) -> None:
    category = 'Limpeza'
    with pytest.raises(
        CategoryError,
        re.compile(
            (
                r'Categoria inválida, utilize uma das seguintes: '
                f'{browser.get_all_categories()}'
            )
        ),
    ):
        browser.get_projects_urls(category, page=1)


def test_send_message(driver: Chrome, browser: NineNineBrowser) -> None:
    project = browser.get_projects_urls(
        'Web, Mobile & Software', page=randint(20, 30)
    )[randint(0, 9)]
    text = (
        f'{get_greeting_according_time(datetime.now().time())} '
        f'{project.client_name}, tudo bem?\n'
        f'Ao ler sobre o seu projeto "{project.name}", percebi que ele está '
        f'alinhado com a minha expertise em {project.category}, gostaria de '
        'saber qual o seu prazo ideal para a conclusão do projeto e se você '
        'possui algum detalhe em específico que considera fundamental?\n'
        f'ass: {browser.get_account_name()}'
    )
    message = browser.send_message(project.url, text)
    driver.get('https://www.99freelas.com.br/messages/inbox')
    assert (
        find_elements(driver, '.message-text:not(.empty)')[-1].text
        == message.text
    )
