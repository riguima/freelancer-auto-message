import json
import os
from datetime import time
from pathlib import Path

import pandas as pd

from cray_freelas_bot.common.project import (
    create_browser_from_module,
    get_bots,
    get_greeting_according_time,
    to_excel,
)
from cray_freelas_bot.domain.models import Message, Project


def test_get_greeting_according_time() -> None:
    assert get_greeting_according_time(time(9, 30, 0)) == 'Bom dia'
    assert get_greeting_according_time(time(2, 30, 0)) == 'Bom dia'
    assert get_greeting_according_time(time(12, 0, 0)) == 'Boa tarde'
    assert get_greeting_according_time(time(19, 45, 0)) == 'Boa noite'


def test_to_excel() -> None:
    messages = [
        Message(
            Project(
                name='Projeto 1',
                client_name='Cliente 1',
                category='Web, Mobile & Software',
                url='url 1',
            ),
            text='Mensagem de exemplo 1',
        ),
        Message(
            Project(
                name='Projeto 2',
                client_name='Cliente 2',
                category='Web, Mobile & Software',
                url='url 2',
            ),
            text='Mensagem de exemplo 2',
        ),
        Message(
            Project(
                name='Projeto 3',
                client_name='Cliente 3',
                category='Web, Mobile & Software',
                url='url 3',
            ),
            text='Mensagem de exemplo 3',
        ),
    ]
    path = 'tests/test_utils/result.xlsx'
    os.remove(path)
    df = to_excel(messages, path)
    assert pd.read_excel('tests/test_utils/expected_spreadsheet.xlsx').equals(
        df,
    )


def test_to_excel_append_message() -> None:
    message = Message(
        Project(
            name='Projeto 4',
            client_name='Cliente 4',
            category='Web, Mobile & Software',
            url='url 4',
        ),
        text='Mensagem de exemplo 4',
    )
    df = to_excel([message], 'tests/test_utils/result.xlsx')
    assert len(df) == 4


def test_create_browser_from_module() -> None:
    browser_type = type(
        create_browser_from_module(
            'nine_nine_freelas',
            user_data_dir='.default_user_data',
            visible=False,
        )
    )
    assert 'NineNineBrowser' in str(browser_type)


def test_get_bots_without_bots_json() -> None:
    if Path('.bots.json').exists():
        os.remove('.bots.json')
    assert get_bots() == []


def test_get_bots() -> None:
    expected_bot = {
        'username': 'richard@gmail.com',
        'password': 'Richard123',
        'website': 'nine_nine_freelas',
        'category': 'Web, Mobile & Software',
        'report_folder': '/home/riguima/Downloads',
        'user_data_dir': '.richard_user_data',
        'message': 'Mensagem de teste',
    }
    json.dump({'bots': [expected_bot]}, open('.bots.json', 'w'))
    assert get_bots()[0] == expected_bot
