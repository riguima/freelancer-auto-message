import inspect
import json
from datetime import time
from importlib import import_module
from pathlib import Path

import pandas as pd

from cray_freelas_bot.domain.browser import IBrowser
from cray_freelas_bot.domain.models import Message


def get_greeting_according_time(greeting_time: time) -> str:
    """
    Retorna a saudação correta de acordo com o horário passado como parâmetro
    Parameters:
        greeting_time: Horário
    Returns:
        Uma string com a saudação correta
    Examples:
        >>> from datetime import time
        >>>
        >>> get_greeting_according_time(time(12, 0, 0))
        Boa tarde
        >>> get_greeting_according_time(time(9, 45, 30))
        Bom dia
        >>> get_greeting_according_time(time(20, 30, 0))
        Boa noite
    """
    if time(0, 0, 0) <= greeting_time <= time(11, 59, 59):
        return 'Bom dia'
    elif time(12, 0, 0) <= greeting_time <= time(18, 59, 59):
        return 'Boa tarde'
    elif time(19, 0, 0) <= greeting_time <= time(23, 59, 59):
        return 'Boa noite'


def to_excel(messages: list[Message], path: str) -> pd.DataFrame:
    """
    Exporta mensagens para uma planilha em Excel, se a planilha existir, adiciona novas mensagens a planilha existente
    Parameters:
        messages: A lista de mensagens que serão adicionadas a planilha, são instâncias da classe Message
        path: Caminho para o arquivo com o resultado, tem que ser com extensão .xlsx
    Returns:
        Uma DataFrame do pandas com os dados das mensagens
    Examples:
        >>> from cray_freelas_bot.domain.models import Message, Project
        >>>
        >>> messages = [
            Message(
                project=Project(
                    name='Nome do projeto',
                    client_name='Nome do cliente',
                    category='Web, Mobile & Software',
                    url='urldeexemplo.com.br',
                ),
                text='Mensagem de exemplo',
            ),
        ]
        >>> to_excel(messages, 'result.xlsx')
    """
    if Path(path).exists():
        df = pd.read_excel(path)
    else:
        df = pd.DataFrame(
            columns=[
                'Nome do projeto',
                'Nome do cliente',
                'Mensagem',
                'Categoria',
                'URL',
            ]
        )
    for message in messages:
        df.loc[len(df)] = [
            message.project.name,
            message.project.client_name,
            message.text,
            message.project.category,
            message.project.url,
        ]
    df.to_excel(path, index=False)
    return df


def create_browser_from_module(module_name: str, *args, **kwargs) -> IBrowser:
    module = import_module(f'cray_freelas_bot.use_cases.{module_name}')
    for _, obj in inspect.getmembers(module):
        if obj in IBrowser.__subclasses__():
            return obj(*args, **kwargs)


def get_bots() -> list[dict]:
    """
    Retorna a lista dos bots criados
    Returns:
        Uma lista com os bots criados
    Examples:
        >>> from cray_freelas_bot.common.project import get_bots()
        >>>
        >>> get_bots()
        [{"username": "usuario@gmail.com", "password": "senha123", "website": "nine_nine_freelas", "category": "Web, Mobile & Software", "report_folder": "~/Downloads", "user_data_dir": ".usuario_user_data", "message": "Mensagem de exemplo"}]
    """
    if not Path('.bots.json').exists():
        json.dump({'bots': []}, open('.bots.json', 'w'))
    return json.load(open('.bots.json'))['bots']
