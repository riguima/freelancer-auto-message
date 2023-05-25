import json
from pathlib import Path

import pandas as pd
from PySide6 import QtCore

from cray_freelas_bot.common.project import to_excel
from cray_freelas_bot.domain.browser import IBrowser


class BrowserThread(QtCore.QThread):
    def __init__(self, browsers: list[IBrowser]) -> None:
        super().__init__()
        self.browsers = browsers

    def run(self) -> None:
        while True:
            print('fskjfsl;')
            bots = json.load(open('.secrets.json'))['bots']
            for browser, bot in zip(self.browsers, bots):
                report_path = Path(bot['report_folder']) / 'result.xlsx'
                urls = pd.read_excel(report_path)['URL']
                projects_urls = [
                    p.url for p in browser.get_projects(bot['category'])
                ]
                for project_url in projects_urls:
                    if project_url not in urls:
                        message = browser.send_message(project_url)
                        to_excel([message], report_path)
