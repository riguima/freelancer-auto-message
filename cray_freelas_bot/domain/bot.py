from dataclasses import dataclass
from pathlib import Path

import pandas as pd
from selenium.common.exceptions import TimeoutException

from cray_freelas_bot.common.project import (
    create_browser_from_module,
    to_excel,
)
from cray_freelas_bot.domain.browser import IBrowser
from cray_freelas_bot.exceptions.project import ProjectError


@dataclass
class Bot:
    username: str
    password: str
    report_folder: Path
    category: str
    message: str
    user_data_dir: str
    browser: IBrowser
    id: int = None

    def run(self) -> None:
        if not self.browser.is_logged():
            self.browser.make_login(self.username, self.password)
        for url in self.get_valid_projects_urls():
            try:
                self.send_message(url)
            except TimeoutException:
                continue

    def get_valid_projects_urls(self):
        report_path = Path(self.report_folder) / 'result.xlsx'
        urls = to_excel([], report_path)['URL']
        result = []
        for url in self.browser.get_projects_urls(self.category):
            if url not in urls:
                try:
                    self.browser.get_project(url)
                except ProjectError:
                    continue
                result.append(url)
        return result

    def send_message(self, project_url: str) -> None:
        text = self.browser.format_message(
            self.message, self.browser.get_project(project_url)
        )
        report_path = Path(self.report_folder) / 'result.xlsx'
        message = self.browser.send_message(project_url, text)
        to_excel([message], report_path)
