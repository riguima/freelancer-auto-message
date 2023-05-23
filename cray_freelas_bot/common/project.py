from datetime import time

import pandas as pd

from cray_freelas_bot.domain.models import Message


def get_greeting_according_time(greeting_time: time) -> str:
    if time(0, 0, 0) <= greeting_time <= time(11, 59, 59):
        return 'Bom dia'
    elif time(12, 0, 0) <= greeting_time <= time(18, 59, 59):
        return 'Boa tarde'
    elif time(19, 0, 0) <= greeting_time <= time(23, 59, 59):
        return 'Boa noite'


def to_excel(messages: list[Message], path: str) -> pd.DataFrame:
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
