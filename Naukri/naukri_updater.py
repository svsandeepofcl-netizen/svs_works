import os
import sys
import time
import traceback
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

try:
    from playwright_stealth import Stealth
    STEALTH_AVAILABLE = True
except ImportError:
    STEALTH_AVAILABLE = False

from config import (
    get_credentials,
    LOGIN_URL,
    HOMEPAGE_URL,
    PROFILE_URL,
    TARGET_RESUME_HEADLINE,
    HEADLESS,
    BROWSER_TIMEOUT_MS,
    NAVIGATION_TIMEOUT_MS,
    USER_AGENT,
)
from logger import setup_logger, get_screenshot_path

logger = setup_logger("NaukriUpdater")


class NaukriUpdater:
    def __init__(self, headless: bool = HEADLESS, target_headline: str = None):
        self.headless = headless
        self.target_headline = target_headline or TARGET_RESUME_HEADLINE
        self.email, self.password = get_credentials()
        self.browser = None
        self.context = None
        self.page = None

    def validate_credentials(self) -> bool:
        if not self.email or not self.password:
            logger.error("Naukri credentials are missing! Please check .credentials file.")
            return False
        logger.info(f"Loaded credentials for user: {self.email}")
        return True

    def _init_browser(self, p):
        logger.info(f"Launching browser (headless={self.headless})...")
        
        launch_args = [
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-infobars",
            "--disable-extensions",
            "--start-maximized",
        ]

        # Prefer system Google Chrome if available, otherwise chromium
        try:
            self.browser = p.chromium.launch(
                headless=self.headless,
                channel="chrome",
                args=launch_args,
            )
            logger.info("Using installed Google Chrome browser channel.")
        except Exception as e:
            logger.warning(f"Could not launch Chrome channel: {e}. Falling back to default Chromium.")
            self.browser = p.chromium.launch(
                headless=self.headless,
                args=launch_args,
            )

        self.context = self.browser.new_context(
            viewport={"width": 1366, "height": 768},
            user_agent=USER_AGENT,
            locale="en-US",
            timezone_id="Asia/Kolkata",
            permissions=["geolocation"],
        )

        self.page = self.context.new_page()
        self.page.set_default_timeout(BROWSER_TIMEOUT_MS)

        if STEALTH_AVAILABLE:
            try:
                stealth = Stealth()
                stealth.apply_stealth_sync(self.page)
                logger.info("Playwright-stealth applied successfully.")
            except Exception as se:
                logger.warning(f"Failed to apply playwright-stealth: {se}")

    def login(self) -> bool:
        logger.info(f"Navigating to login page: {LOGIN_URL}")
        try:
            self.page.goto(LOGIN_URL, wait_until="domcontentloaded", timeout=NAVIGATION_TIMEOUT_MS)
            self.page.wait_for_timeout(3000)
        except Exception as e:
            logger.error(f"Navigation to login page failed: {e}")
            ss = get_screenshot_path("login_navigation_failed")
            self.page.screenshot(path=ss)
            return False

        logger.info(f"Page loaded: '{self.page.title()}' (URL: {self.page.url})")

        # 1. Locate username input
        username_selectors = [
            "input#usernameField",
            "input[placeholder*='Email' i]",
            "input[placeholder*='Username' i]",
            "input[name='email']",
            "input[type='text']",
        ]
        user_input = None
        for sel in username_selectors:
            el = self.page.query_selector(sel)
            if el and el.is_visible():
                user_input = el
                logger.info(f"Found username input field using selector: {sel}")
                break

        if not user_input:
            logger.error("Could not find username field on login page!")
            ss = get_screenshot_path("username_not_found")
            self.page.screenshot(path=ss)
            return False

        user_input.click()
        user_input.fill("")
        user_input.type(self.email, delay=50)

        # 2. Locate password input
        password_selectors = [
            "input#passwordField",
            "input[placeholder*='Password' i]",
            "input[name='password']",
            "input[type='password']",
        ]
        pass_input = None
        for sel in password_selectors:
            el = self.page.query_selector(sel)
            if el and el.is_visible():
                pass_input = el
                logger.info(f"Found password input field using selector: {sel}")
                break

        if not pass_input:
            logger.error("Could not find password field on login page!")
            ss = get_screenshot_path("password_not_found")
            self.page.screenshot(path=ss)
            return False

        pass_input.click()
        pass_input.fill("")
        pass_input.type(self.password, delay=50)

        # 3. Locate submit button
        submit_selectors = [
            "button[type='submit']",
            "button.loginButton",
            ".btn-primary.loginButton",
            "button:has-text('Login')",
        ]
        submit_btn = None
        for sel in submit_selectors:
            el = self.page.query_selector(sel)
            if el and el.is_visible():
                submit_btn = el
                logger.info(f"Found submit button using selector: {sel}")
                break

        if not submit_btn:
            logger.error("Could not find submit button on login page!")
            ss = get_screenshot_path("submit_not_found")
            self.page.screenshot(path=ss)
            return False

        logger.info("Submitting login form...")
        submit_btn.click()

        # Wait for navigation / redirect
        self.page.wait_for_timeout(5000)

        # Check for errors on login page
        error_el = self.page.query_selector(".server-err, .err-msg, div[class*='error-msg'], .server-error")
        if error_el and error_el.is_visible():
            err_text = error_el.inner_text().strip()
            logger.error(f"Login failed with error: {err_text}")
            ss = get_screenshot_path("login_error_displayed")
            self.page.screenshot(path=ss)
            return False

        # Check for OTP or Captcha verification
        otp_el = self.page.query_selector("input[placeholder*='OTP' i], .otp-container, [id*='otp' i]")
        if otp_el and otp_el.is_visible():
            logger.warning("Naukri prompted for OTP verification! Manual OTP is required.")
            ss = get_screenshot_path("otp_prompt_detected")
            self.page.screenshot(path=ss)
            return False

        # Confirm post-login state
        current_url = self.page.url
        logger.info(f"Post-login URL: {current_url}")

        if "login" not in current_url.lower() or "homepage" in current_url or "profile" in current_url:
            logger.info("Login successful!")
            ss = get_screenshot_path("login_success")
            self.page.screenshot(path=ss)
            return True

        # Check for user drawer/profile icon
        drawer = self.page.query_selector(".nI-gNb-drawer, .view-profile-wrapper, a[href*='profile']")
        if drawer:
            logger.info("Login confirmed via profile drawer presence.")
            return True

        logger.warning(f"Login status ambiguous. Current URL is {current_url}.")
        ss = get_screenshot_path("login_ambiguous")
        self.page.screenshot(path=ss)
        return True

    def update_profile(self) -> bool:
        logger.info(f"Navigating to profile page: {PROFILE_URL}")
        try:
            self.page.goto(PROFILE_URL, wait_until="domcontentloaded", timeout=NAVIGATION_TIMEOUT_MS)
            self.page.wait_for_timeout(4000)
        except Exception as e:
            logger.error(f"Failed to navigate to profile page: {e}")
            return False

        logger.info(f"Profile Page loaded: '{self.page.title()}' (URL: {self.page.url})")
        ss_before = get_screenshot_path("profile_before_update")
        self.page.screenshot(path=ss_before)

        # Strategy A: Update Resume Headline (standard and most effective way to touch profile)
        headline_updated = self._update_resume_headline()
        if headline_updated:
            logger.info("Successfully updated Resume Headline!")
        else:
            logger.warning("Resume Headline update failed or not found. Attempting fallback...")
            # Strategy B: Fallback to Profile Summary
            summary_updated = self._update_profile_summary()
            if not summary_updated:
                logger.error("All profile update strategies failed.")
                return False

        self.page.wait_for_timeout(3000)
        ss_after = get_screenshot_path("profile_after_update")
        self.page.screenshot(path=ss_after)

        # Inspect updated timestamp if visible
        try:
            mod_el = self.page.query_selector(".mod-date, .last-updated, [class*='last-updated' i]")
            if mod_el and mod_el.is_visible():
                logger.info(f"Profile status text: {mod_el.inner_text().strip()}")
        except Exception:
            pass

        return True

    def _update_resume_headline(self) -> bool:
        logger.info("Searching for Resume Headline section...")

        edit_selectors = [
            "div.resumeHeadline span.edit",
            "div.resumeHeadline .edit.icon",
            "div[widget-id='resumeHeadline'] span.edit",
            "//div[contains(@class, 'resumeHeadline')]//span[contains(@class, 'edit')]",
            "//div[contains(@class, 'widgetHead') and contains(., 'Resume headline')]//span[contains(@class, 'edit')]",
            "//span[contains(@class, 'edit') and preceding-sibling::span[contains(text(), 'Resume headline')]]",
            "//span[text()='Resume headline']/following::span[contains(@class, 'edit')][1]",
        ]

        edit_btn = None
        for sel in edit_selectors:
            try:
                el = self.page.wait_for_selector(sel, timeout=3000)
                if el and el.is_visible():
                    edit_btn = el
                    logger.info(f"Found Resume Headline edit button: {sel}")
                    break
            except Exception:
                continue

        if not edit_btn:
            logger.warning("Could not find Resume Headline edit icon.")
            return False

        logger.info("Clicking Resume Headline edit button...")
        edit_btn.click()
        self.page.wait_for_timeout(2000)

        # Locate textarea
        textarea_selectors = [
            "textarea#resumeHeadlineTxt",
            "div.resumeHeadline textarea",
            "div.modal textarea",
            "textarea[placeholder*='headline' i]",
            "textarea.materialize-textarea",
            "textarea",
        ]

        textarea = None
        for sel in textarea_selectors:
            el = self.page.query_selector(sel)
            if el and el.is_visible():
                textarea = el
                logger.info(f"Found headline textarea: {sel}")
                break

        if not textarea:
            logger.warning("Headline textarea not found after clicking edit.")
            return False

        current_val = textarea.input_value() or ""
        current_val = current_val.strip()
        logger.info(f"Current headline length: {len(current_val)} characters.")

        # Toggle trailing period to register a valid modification
        if current_val.endswith("."):
            new_val = current_val[:-1].strip()
        else:
            new_val = (current_val + ".").strip()

        if not new_val:
            new_val = "Experienced Professional seeking growth opportunities."

        logger.info(f"Updating headline with modified text (toggled dot indicator)...")
        textarea.fill("")
        textarea.fill(new_val)
        self.page.wait_for_timeout(1000)

        # Locate Save button
        save_selectors = [
            "div.resumeHeadline button.btn-primary",
            "div.action button:has-text('Save')",
            "button:has-text('Save')",
            "form[name='resumeHeadlineForm'] button[type='submit']",
            "//button[normalize-space()='Save']",
        ]

        save_btn = None
        for sel in save_selectors:
            el = self.page.query_selector(sel)
            if el and el.is_visible():
                save_btn = el
                logger.info(f"Found headline Save button: {sel}")
                break

        if not save_btn:
            logger.warning("Save button not found for resume headline.")
            return False

        save_btn.click()
        logger.info("Clicked Save button on Resume Headline.")

        # Wait for toast confirmation or modal dismissal
        try:
            self.page.wait_for_selector(
                "div.msg:has-text('saved'), div.toast, .save-msg",
                timeout=5000,
            )
            logger.info("Save confirmation message detected.")
        except Exception:
            logger.info("No explicit toast detected; waiting for state to settle.")

        self.page.wait_for_timeout(3000)
        return True

    def _update_profile_summary(self) -> bool:
        logger.info("Attempting Profile Summary update fallback...")
        summary_edit_selectors = [
            "div.profileSummary span.edit",
            "div[widget-id='profileSummary'] span.edit",
            "//div[contains(@class, 'profileSummary')]//span[contains(@class, 'edit')]",
        ]

        edit_btn = None
        for sel in summary_edit_selectors:
            try:
                el = self.page.wait_for_selector(sel, timeout=3000)
                if el and el.is_visible():
                    edit_btn = el
                    logger.info(f"Found Profile Summary edit button: {sel}")
                    break
            except Exception:
                continue

        if not edit_btn:
            logger.warning("Could not find Profile Summary edit icon.")
            return False

        edit_btn.click()
        self.page.wait_for_timeout(2000)

        textarea = self.page.query_selector("div.profileSummary textarea, textarea#profileSummaryTxt, textarea")
        if not textarea:
            return False

        current_val = textarea.input_value() or ""
        current_val = current_val.strip()
        if current_val.endswith("."):
            new_val = current_val[:-1].strip()
        else:
            new_val = (current_val + ".").strip()

        if not new_val:
            new_val = "Experienced specialist passionate about innovation and high-impact solutions."

        textarea.fill(new_val)
        self.page.wait_for_timeout(1000)

        save_btn = self.page.query_selector("div.profileSummary button:has-text('Save'), button:has-text('Save')")
        if save_btn:
            save_btn.click()
            logger.info("Clicked Save button on Profile Summary.")
            self.page.wait_for_timeout(3000)
            return True

        return False

    def run(self) -> dict:
        result = {
            "success": False,
            "message": "",
            "start_time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "end_time": None,
        }

        logger.info("=" * 60)
        logger.info("Starting Naukri Profile Automation Run")
        logger.info("=" * 60)

        if not self.validate_credentials():
            result["message"] = "Invalid or missing credentials."
            return result

        with sync_playwright() as p:
            try:
                self._init_browser(p)

                # Step 1: Login
                logged_in = self.login()
                if not logged_in:
                    result["message"] = "Login failed."
                    logger.error("Aborting run because login was unsuccessful.")
                    return result

                # Step 2: Update Profile
                updated = self.update_profile()
                if not updated:
                    result["message"] = "Profile update failed."
                    logger.error("Profile update could not be completed.")
                    return result

                result["success"] = True
                result["message"] = "Naukri profile updated successfully!"
                logger.info("Naukri profile update process completed with SUCCESS.")

            except Exception as e:
                result["message"] = f"Unexpected error: {str(e)}"
                logger.error(f"Exception during run: {e}")
                logger.error(traceback.format_exc())
                if self.page:
                    try:
                        err_ss = get_screenshot_path("unexpected_exception")
                        self.page.screenshot(path=err_ss)
                        logger.info(f"Error screenshot saved to: {err_ss}")
                    except Exception:
                        pass
            finally:
                if self.browser:
                    try:
                        self.browser.close()
                        logger.info("Browser closed.")
                    except Exception:
                        pass

        result["end_time"] = time.strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Run finished at {result['end_time']}. Status: {result['success']}")
        logger.info("=" * 60)
        return result

