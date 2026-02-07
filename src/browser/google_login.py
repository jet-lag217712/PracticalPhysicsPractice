from src.config import AUTH
from src.utils.exceptions import ButtonNotFound, InputNotFound
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


def click_google_login(page):
    try:
        page.locator(".Button.Button--primary").first.click(timeout=5000)
    except PlaywrightTimeoutError:
        raise ButtonNotFound("Google login button not found")


def enter_email(page, email):
    try:
        email_input = page.locator('input[type="email"]')
        email_input.wait_for(timeout=5000)
        email_input.fill(email)
    except PlaywrightTimeoutError:
        raise InputNotFound("Email input not found")


def enter_password(page, password):
    try:
        password_input = page.locator('input[name="Passwd"]')
        password_input.wait_for(state="visible", timeout=10000)
        password_input.fill(password)
    except Exception:
        raise InputNotFound("Password input not found or not interactable")

def click_next(page):
    try:
        next_btn = page.locator('button:has-text("Next")').first
        next_btn.wait_for(state="visible", timeout=5000)
        next_btn.click()
    except Exception:
        raise ButtonNotFound("Next button not found")

def google_login(page):
    email, password = AUTH
    click_google_login(page)
    # Email step
    enter_email(page, email)
    click_next(page)
    # Password step
    enter_password(page, password)
    click_next(page)