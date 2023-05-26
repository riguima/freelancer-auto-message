import json
from pathlib import Path
from time import sleep

import pandas as pd
from PySide6 import QtCore, QtWidgets

from cray_freelas_bot.common.project import to_excel
from cray_freelas_bot.exceptions.project import ProjectError


class BrowserThread(QtCore.QThread):
    def __init__(self, widget: QtWidgets.QWidget) -> None:
        super().__init__()
        self.widget = widget

    def run(self) -> None:
        while True:
            bots = json.load(open('.secrets.json'))['bots']
            for browser, bot in zip(self.widget.browsers, bots):
                report_path = Path(bot['report_folder']) / 'result.xlsx'
                urls = pd.read_excel(report_path)['URL']
                projects_urls = [
                    p.url for p in browser.get_projects(bot['category'])
                ]
                for project_url in projects_urls:
                    if project_url not in urls:
                        try:
                            message = browser.send_message(project_url)
                        except ProjectError:
                            continue
                        to_excel([message], report_path)
            sleep(60)
