from datetime import time

import pandas as pd

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
    Exporta mensagens para uma planilha em Excel
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
