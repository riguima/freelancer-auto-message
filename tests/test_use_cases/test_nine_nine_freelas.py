import pytest
import json

from cray_freelas_bot.use_cases.nine_nine_freelas import NineNineBrowser
from cray_freelas_bot.common.driver import create_driver


@pytest.fixture(scope='module')
def browser() -> NineNineBrowser:
    return NineNineBrowser(create_driver(visible=True))


def test_make_login(browser) -> None:
    assert browser.make_login(
        'miqueiasmartinsoficial@gmail.com', 'Projeto#1bot'
    )


def test_get_all_categories(browser) -> None:
    expected = json.load(
        open('tests/test_use_cases/nine_nine_categories.json', 'r')
    )
    assert browser.get_all_categories() == expected


def test_get_account_name(browser) -> None:
    assert browser.get_account_name() == 'Miqueias Martin'


def test_get_projects(browser) -> None:
    category = 'Engenharia & Arquitetura'
    projects = browser.get_projects(category, page=1)
    assert len(projects) == 10
    assert browser.driver.current_url == 'https://www.99freelas.com.br/projects?order=mais-recentes&categoria=engenharia-e-arquitetura&page=1'
    assert projects != browser.get_projects(category, page=2)


def test_get_projects_with_invalid_category(browser) -> None:
    with pytest.raises(ValueError):
        browser.get_projects('Limpeza', page=1)


def test_send_message(browser) -> None:
    project = browser.get_projects('Engenharia & Arquitetura', page=3)[5]
    message = (
        f'Bom dia {project.client_name}, tudo bem?\n'
        f'Ao ler sobre o seu projeto "{project.name}", percebi que ele está '
        f'alinhado com a minha expertise em {project.category}, gostaria de '
        'saber qual o seu prazo ideal para a conclusão do projeto e se você '
        'possui algum detalhe em específico que considera fundamental?\n'
        f'ass: {browser.get_account_name()}'
    )
    browser.send_message(project, message)
    last_message = browser.get_last_message()
    assert last_message.project == project
    assert last_message.text == message
