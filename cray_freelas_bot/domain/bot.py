from dataclasses import dataclass
from pathlib import Path

from selenium.common.exceptions import TimeoutException

from cray_freelas_bot.common.browser import create_browser_from_module
from cray_freelas_bot.common.project import to_excel
from cray_freelas_bot.domain.browser import IBrowser
from cray_freelas_bot.domain.message_sent import MessageSent
from cray_freelas_bot.repositories.message_sent import MessageSentRepository
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
    id: int = None

    def run(self) -> None:
        browser = create_browser_from_module(self.browser_module)
        if not browser.is_logged():
            browser.make_login(self.username, self.password)
        breakpoint()
        for url in self.get_valid_projects_urls(browser):
            try:
                self.send_message(browser, url)
            except TimeoutException:
                continue

    def get_valid_projects_urls(self, browser: IBrowser) -> list[str]:
        result = []
        urls = [m.url for m in MessageSentRepository().all()]
        for url in self.browser.get_projects_urls(self.category):
            if url not in urls:
                try:
                    self.browser.get_project(url)
                except ProjectError:
                    continue
                result.append(url)
        return result

    def send_message(self, browser: IBrowser, project_url: str) -> None:
        text = self.browser.format_message(
            self.message, browser.get_project(project_url)
        )
        report_path = Path(self.report_folder) / 'result.xlsx'
        message = browser.send_message(project_url, text)
        to_excel([message], report_path)
        MessageSentRepository().create(MessageSent(url=project_url))
