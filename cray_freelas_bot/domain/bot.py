from dataclasses import dataclass
from pathlib import Path

import pandas as pd

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
    browser_module: str

    def run(self) -> None:
        browser = create_browser_from_module(self.browser_module)
        if not browser.is_logged():
            browser.make_login(self.username, self.password)
        for url in self.get_valid_projects_urls(browser):
            self.send_message(url)

    def get_valid_projects_urls(self, browser: IBrowser):
        report_path = self.report_folder / 'result.xlsx'
        urls = pd.read_excel(report_path)['URL']
        result = []
        for url in browser.get_projects_urls(self.category):
            if url not in urls:
                try:
                    browser.get_project(url)
                except ProjectError:
                    continue
                result.append(url)
        return result

    def send_message(self, browser: IBrowser, project_url: str) -> None:
        text = browser.format_message(
            self.message, browser.get_project(project_url)
        )
        message = browser.send_message(text, project_url)
        to_excel([message], self.report_path)
