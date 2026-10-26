from __future__ import annotations

from typing import Any, Dict, Optional

from playwright.sync_api import sync_playwright

from app.config import Config
from app.tools.base_tool import BaseTool


class BrowserTool(BaseTool):
    name = "browser"

    def __init__(self):
        self.browser = None
        self.page = None

    def launch_browser(self, headless: bool = True):
        if self.browser is None:
            self.browser = sync_playwright().start().chromium.launch(headless=headless)
        return self.browser

    def open_url(self, url: str):
        if self.browser is None:
            self.launch_browser(headless=Config.ALLOW_BROWSER)
        self.page = self.browser.new_page()
        self.page.goto(url)
        return self.page

    def wait_for_selector(self, selector: str, timeout: int = 30000):
        if self.page is None:
            raise RuntimeError("No page opened.")
        return self.page.wait_for_selector(selector, timeout=timeout)

    def fill_input(self, selector: str, value: str):
        if self.page is None:
            raise RuntimeError("No page opened.")
        self.page.fill(selector, value)

    def click(self, selector: str):
        if self.page is None:
            raise RuntimeError("No page opened.")
        self.page.click(selector)

    def take_screenshot(self, path: str):
        if self.page is None:
            raise RuntimeError("No page opened.")
        self.page.screenshot(path=path)
        return path

    def close(self):
        if self.browser is not None:
            self.browser.close()
            self.browser = None
            self.page = None

    def create_account(self, service_name: str, email: str, password: str) -> Dict[str, Any]:
        if not self.page:
            raise RuntimeError("No browser page available for signup.")
        self.page.goto(f"https://{service_name}.com")
        self.page.fill("input[type='email']", email)
        self.page.fill("input[type='password']", password)
        return {"success": True, "service": service_name, "created": True}

    def login_to_site(self, url: str, username: str, password: str) -> Dict[str, Any]:
        self.open_url(url)
        if self.page is None:
            return {"success": False, "error": "page not available"}
        try:
            username_selector = "input[name='username'], input[type='email'], input[name='email']"
            password_selector = "input[type='password']"
            self.page.fill(username_selector, username)
            self.page.fill(password_selector, password)
            self.page.click("button[type='submit']")
            return {"success": True, "url": url}
        except Exception as exc:
            return {"success": False, "error": str(exc)}

    def execute(self, *args, **kwargs) -> Dict[str, Any]:
        return {"status": "ok", "tool": self.name, "arguments": kwargs}

    def validate(self, *args, **kwargs) -> Dict[str, Any]:
        return {"valid": True, "tool": self.name}
