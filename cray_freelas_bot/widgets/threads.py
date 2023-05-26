import json
from datetime import datetime
from pathlib import Path
from time import sleep

import pandas as pd
from PySide6 import QtCore

from cray_freelas_bot.common.project import (
    create_browser_from_module,
    get_greeting_according_time,
    to_excel,
)
from cray_freelas_bot.domain.browser import IBrowser


class BrowserThread(QtCore.QThread):
    def run(self) -> None:
        browsers = self.create_browsers()
        while True:
            bots = json.load(open('.secrets.json'))['bots']
            for browser, bot in zip(browsers, bots):
                report_path = Path(bot['report_folder']) / 'result.xlsx'
                urls = pd.read_excel(report_path)['URL']
                projects_urls = browser.get_projects_urls(bot['category'])
                for project_url in projects_urls:
                    if project_url not in urls:
                        project = browser.get_project(project_url)
                        greeting = get_greeting_according_time(
                            datetime.now().time()
                        )
                        text = (
                            f'{greeting} {{b}}{project.client_name}{{/b}}, '
                            f'tudo bem?\n\n Ao ler sobre o seu projeto '
                            f'{{b}}"{project.name}"{{/b}}, percebi que ele '
                            'está alinhado com a minha expertise em '
                            f'{project.category}, gostaria de saber qual o '
                            'seu prazo ideal para a conclusão do projeto e se '
                            'você possui algum detalhe em específico que '
                            'considera fundamental?\n\n'
                            f'ass: {{b}}{browser.get_account_name()}{{/b}}'
                        )
                        message = browser.send_message(text, project_url)
                        to_excel([message], report_path)
            sleep(60)

    def create_browsers(self) -> list[IBrowser]:
        result = []
        bots = json.load(open('.secrets.json'))['bots']
        for bot in bots:
            browser = create_browser_from_module(
                bot['website'],
                user_data_dir=bot['user_data_dir'],
                visible=True,
            )
            result.append(browser)
        return result
