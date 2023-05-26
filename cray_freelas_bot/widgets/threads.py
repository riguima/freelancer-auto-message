import json
from pathlib import Path
from time import sleep

import pandas as pd
from PySide6 import QtCore

from cray_freelas_bot.common.project import (
    create_browser_from_module,
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
                        message = browser.send_message(project_url)
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
