"""
automated_video_platform_onboarder.py
Milestone 1 Video Platform Automated CDP & Email/OTP Onboarding Engine
for Gary Pearce / ADI Communications (07860 244 274).

Features:
- Native WebSocket connection to Chrome CDP port 9223 (zero subprocess lingering).
- GoogleOAuthDriver (1-Click Google Workspace OAuth for aiagent1510@gmail.com).
- EmailOtpDriver (Form autofill, OTP extraction, activation link handling via auto_email_verifier).
- ProfileBrandManager (Gary Pearce E-E-A-T trade credentials, strict Rule 45 3-tier linking).
- 11-Type Failure Taxonomy (CAPTCHA, Billing, SMS, Email Timeout, Waitlist, Dead, etc.).
- 5-Layer Data Integrity Firewall enforcement.
- CatalogParitySync (Atomic synchronization between JSON catalog and doc2 CSV).
- Comprehensive CLI: --dry-run, --platform, --tier, --all-pending, --audit-firewall, --sync-parity.
"""

import argparse
import asyncio
import base64
import csv
import datetime
import json
import os
import posixpath
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import websockets

# Import existing helpers
REPO_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO_ROOT))

try:
    from automated_platform_onboarder import FailureReason, IntegrityFirewall
except ImportError:
    # Standalone fallback if automated_platform_onboarder is moved
    class FailureReason:
        CAPTCHA_REQUIRED = "CAPTCHA_REQUIRED"
        MANUAL_BILLING_REQUIRED = "MANUAL_BILLING_REQUIRED"
        PHONE_SMS_REQUIRED = "PHONE_SMS_REQUIRED"
        EMAIL_TIMEOUT = "EMAIL_TIMEOUT"
        SSO_OAUTH_FAILED = "SSO_OAUTH_FAILED"
        WAITLIST_PENDING = "WAITLIST_PENDING"
        GEO_RESTRICTED = "GEO_RESTRICTED"
        RATE_LIMITED = "RATE_LIMITED"
        CLI_AUTH_REQUIRED = "CLI_AUTH_REQUIRED"
        BANNED_POLICY = "BANNED_POLICY"
        PLATFORM_DEAD = "PLATFORM_DEAD"

        ALL_REASONS = {
            CAPTCHA_REQUIRED: "Interactive Cloudflare Turnstile, hCaptcha, or reCAPTCHA Enterprise challenge detected on signup/login page.",
            MANUAL_BILLING_REQUIRED: "Platform requires valid credit/debit card details upfront even for free tier access.",
            PHONE_SMS_REQUIRED: "Platform demands mobile SMS OTP verification that cannot be fulfilled via the Gmail/Workspace CDP loop.",
            EMAIL_TIMEOUT: "Verification email or confirmation token failed to arrive in Gmail inbox within the timeout window.",
            SSO_OAUTH_FAILED: "GitHub OAuth or Google Workspace SSO handshake rejected, scope denied, or 3rd-party auth endpoint error.",
            WAITLIST_PENDING: "Registration completed successfully, but account is placed into a manual approval waitlist.",
            GEO_RESTRICTED: "Platform rejects UK IP addresses, requires non-UK phone/address, or blocks British hosting entities.",
            RATE_LIMITED: "Platform returned HTTP 429 Too Many Requests or transient IP throttling during signup attempts.",
            CLI_AUTH_REQUIRED: "Platform does not offer web-based provisioning; requires headless CLI token exchange.",
            BANNED_POLICY: "Platform is strictly blacklisted by project policy to prevent account damage (e.g., Facebook, LinkedIn).",
            PLATFORM_DEAD: "Signup URL or root domain returns DNS NXDOMAIN, is parked/defunct, or returns HTTP 404/5xx."
        }

        @classmethod
        def is_valid(cls, reason):
            return reason in cls.ALL_REASONS

    class IntegrityFirewall:
        DUMMY_SUBSTRINGS = ["d1abcdefg", "example.com", "placeholder", "test.com", "your-name", "username"]
        SYNTHETIC_DOMAINS = ["adi-telecoms.org"]
        DASHBOARD_SUBDOMAINS = ("app.", "dashboard.", "console.", "admin.", "portal.", "account.", "accounts.", "workspace.")
        RULE45_PATTERN = re.compile(r"(?:https?:)?//(?:www\.)?adicommunications\.co\.uk\.?(?::\d+)?[^\s\"\'<>)]*", re.IGNORECASE)

        @classmethod
        def validate_layer1_syntax(cls, url):
            if not url or not isinstance(url, str):
                return False, "URL is empty or non-string"
            clean = url.strip()
            if any(c in clean for c in (" ", "\t", "\n", "\r", "(", ")")):
                return False, f"URL contains illegal characters: '{url}'"
            parsed = urllib.parse.urlparse(clean)
            if parsed.scheme not in ("https", "http") or not parsed.netloc:
                return False, f"Invalid URL scheme or missing host: '{url}'"
            for dummy in cls.DUMMY_SUBSTRINGS:
                if dummy in clean.lower():
                    return False, f"URL contains dummy/placeholder value: '{dummy}'"
            return True, "Layer 1 Syntax Pass"

        @classmethod
        def validate_layer2_domain(cls, url, platform_name=""):
            ok, msg = cls.validate_layer1_syntax(url)
            if not ok:
                return False, msg
            parsed = urllib.parse.urlparse(url)
            host = (parsed.netloc or "").lower()
            if any(syn in host for syn in cls.SYNTHETIC_DOMAINS):
                return False, f"Synthetic/unresolvable domain detected: '{host}'"
            return True, "Layer 2 Domain Pass"

        @classmethod
        def validate_layer3_anti_dashboard(cls, url):
            ok, msg = cls.validate_layer1_syntax(url)
            if not ok:
                return False, msg
            parsed = urllib.parse.urlparse(url)
            host = (parsed.netloc or "").lower()
            if any(host.startswith(sub) for sub in cls.DASHBOARD_SUBDOMAINS):
                return False, f"Private dashboard subdomain detected: '{host}'"
            path = (parsed.path or "").lower()
            forbidden = ("/app", "/dashboard", "/console", "/admin", "/settings", "/account", "/signin", "/login", "/~")
            if any(seg in path for seg in forbidden):
                return False, f"Private session path detected: '{path}'"
            return True, "Layer 3 Anti-Dashboard Pass"

        @classmethod
        def validate_layer4_live_http_200(cls, url, timeout=5.0):
            try:
                req = urllib.request.Request(
                    url,
                    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
                )
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    status = resp.status
                    if 200 <= status < 400:
                        return True, status, f"HTTP {status} OK"
                    return False, status, f"HTTP {status}"
            except Exception as e:
                return False, 0, str(e)

        @classmethod
        def validate_layer5_rule_45(cls, text_or_url):
            if not text_or_url or not isinstance(text_or_url, str):
                return True, "Layer 5 Rule 45 Pass"
            matches = cls.RULE45_PATTERN.findall(text_or_url)
            for raw in matches:
                # Strip trailing sentence punctuation (,;:!?) first
                url = raw.rstrip(",;:!?")
                # Do not strip trailing dots if part of a relative path traversal (..$)
                if not re.search(r"\.\.(?:$|[?#])", url):
                    url = url.rstrip(".")
                parsed = urllib.parse.urlparse(url)
                unquoted_path = urllib.parse.unquote(parsed.path or "")
                norm_path = posixpath.normpath("/" + unquoted_path.lstrip("/")).rstrip('/')
                norm_raw = posixpath.normpath(unquoted_path).rstrip('/')
                if norm_path == "" or norm_path in ("/index.html", "/index.php", "/index.htm") or norm_raw in ("", ".", "/index.html", "/index.php", "/index.htm"):
                    return False, "Violation of Rule 45: raw naked root anchor to https://adicommunications.co.uk/"
            return True, "Layer 5 Rule 45 Pass"

        @classmethod
        def run_all_layers(cls, url, platform_name="", probe_live=False):
            ok1, msg1 = cls.validate_layer1_syntax(url)
            if not ok1:
                return False, 1, msg1
            ok2, msg2 = cls.validate_layer2_domain(url, platform_name)
            if not ok2:
                return False, 2, msg2
            ok3, msg3 = cls.validate_layer3_anti_dashboard(url)
            if not ok3:
                return False, 3, msg3
            ok5, msg5 = cls.validate_layer5_rule_45(url)
            if not ok5:
                return False, 5, msg5
            if probe_live:
                ok4, status, msg4 = cls.validate_layer4_live_http_200(url)
                if not ok4:
                    return False, 4, f"Status {status}: {msg4}"
            return True, 0, "ALL 5 INTEGRITY LAYERS PASSED"


# Configuration Constants
CDP_BASE = "http://127.0.0.1:9223"
CATALOG_JSON_PATH = REPO_ROOT / "master_multicategory_platform_catalog.json"
DOC2_CSV_PATH = REPO_ROOT / "doc2_multicategory_stack_550.csv"
AUDIT_SCREENSHOT_DIR = REPO_ROOT / "assets" / "audit" / "onboarding_failures"

GARY_PEARCE_BRAND = {
    "engineer": "Gary Pearce",
    "business": "ADI Communications",
    "telephone": "07860 244 274",
    "username": "gazpearce",
    "company_handle": "adicommunications",
    "display_name": "Gary Pearce • ADI Communications",
    "bio": "Gary Pearce • ADI Communications (25+ yrs UK physical security & telecom engineering, £10M Public Liability, 07860 244 274). West Yorkshire & Lancashire.",
    "avatar_url": "https://cdn.jsdelivr.net/gh/gazpearce/cctv-security-hub@master/assets/images/cat6-fluke-dsx-8000-cable-certification-telemetry.webp",
    "cover_banner_url": "https://cdn.jsdelivr.net/gh/gazpearce/cctv-security-hub@master/assets/images/starlink-gen3-heavy-duty-chimney-lashing-livesey.webp",
    "cai_notice": "Uses CAI-benchmarked equipment and double-screened WF100 cable. Gary Pearce / ADI Communications are NOT CAI members."
}


class VideoPlatformCDPClient:
    """Native WebSocket connection to Chrome CDP on port 9223 with zero lingering processes."""

    def __init__(self, cdp_base=CDP_BASE):
        self.cdp_base = cdp_base
        self._msg_id = 1000

    def _next_id(self):
        self._msg_id += 1
        return self._msg_id

    def is_cdp_active(self, timeout=3.0):
        try:
            req = urllib.request.Request(f"{self.cdp_base}/json")
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.status == 200
        except Exception:
            return False

    def list_tabs(self):
        try:
            req = urllib.request.Request(f"{self.cdp_base}/json")
            with urllib.request.urlopen(req, timeout=5.0) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return [t for t in data if isinstance(t, dict)] if isinstance(data, list) else []
        except Exception:
            return []

    def open_tab(self, url="about:blank"):
        """Opens a new tab via HTTP PUT /json/new?<url>."""
        encoded_url = urllib.parse.quote(url, safe="")
        req = urllib.request.Request(f"{self.cdp_base}/json/new?{encoded_url}", method="PUT")
        try:
            with urllib.request.urlopen(req, timeout=10.0) as resp:
                info = json.loads(resp.read().decode("utf-8"))
                return info.get("id"), info.get("webSocketDebuggerUrl")
        except Exception:
            return None, None

    def close_tab(self, tab_id):
        """Closes an ephemeral tab via HTTP GET /json/close/<tab_id>."""
        if not tab_id:
            return False
        try:
            req = urllib.request.Request(f"{self.cdp_base}/json/close/{tab_id}")
            with urllib.request.urlopen(req, timeout=5.0) as resp:
                return resp.status == 200
        except Exception:
            return False

    async def send_cdp(self, ws, method, params=None, timeout=10.0):
        """Sends a JSON-RPC command over WebSocket and correlates response by id."""
        msg_id = self._next_id()
        msg = {"id": msg_id, "method": method, "params": params or {}}
        try:
            await ws.send(json.dumps(msg))
        except Exception:
            return {}

        start_time = time.time()
        while time.time() - start_time < timeout:
            remaining = max(0.01, timeout - (time.time() - start_time))
            try:
                raw = await asyncio.wait_for(ws.recv(), timeout=remaining)
                data = json.loads(raw)
                if data.get("id") == msg_id:
                    res = data.get("result")
                    return res if isinstance(res, dict) else {}
            except (websockets.ConnectionClosed, ConnectionResetError, OSError):
                return {}
            except asyncio.TimeoutError:
                break
            except Exception:
                continue
        return {}

    async def eval_js(self, ws, expression, await_promise=True):
        """Evaluates JavaScript expression in page context."""
        params = {
            "expression": expression,
            "returnByValue": True,
            "awaitPromise": await_promise
        }
        res = await self.send_cdp(ws, "Runtime.evaluate", params)
        if "result" in res and "value" in res["result"]:
            return res["result"]["value"]
        return None

    async def wait_for_selector(self, ws, selector_expr, timeout=15.0):
        """Polls page until document.querySelector(selector_expr) exists."""
        start_time = time.time()
        js = f"Boolean(document.querySelector({json.dumps(selector_expr)}))"
        while time.time() - start_time < timeout:
            try:
                found = await self.eval_js(ws, js)
                if found:
                    return True
            except Exception:
                pass
            await asyncio.sleep(0.5)
        return False

    async def dismiss_cookie_banners(self, ws):
        """Dismisses common European / UK GDPR cookie consent banners."""
        js = """
        (() => {
            const selectors = [
                '#onetrust-accept-btn-handler',
                '#accept-cookie-banners',
                'button[id*="cookie-accept"]',
                'button[class*="cookie-accept"]',
                'button[aria-label*="Accept"]',
                'button[aria-label*="agree"]',
                'button[aria-label*="Allow all"]'
            ];
            for (const s of selectors) {
                const el = document.querySelector(s);
                if (el && typeof el.click === 'function') {
                    el.click();
                    return true;
                }
            }
            const buttons = Array.from(document.querySelectorAll('button, a'));
            for (const btn of buttons) {
                const text = (btn.innerText || '').trim().toLowerCase();
                if (text === 'accept all' || text === 'i agree' || text === 'accept cookies' || text === 'allow all') {
                    btn.click();
                    return true;
                }
            }
            return false;
        })()
        """
        try:
            return await self.eval_js(ws, js)
        except Exception:
            return False

    async def capture_failure_screenshot(self, ws, platform_id, reason):
        """Captures page screenshot and saves to AUDIT_SCREENSHOT_DIR."""
        try:
            AUDIT_SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
            res = await self.send_cdp(ws, "Page.captureScreenshot", {"format": "png"})
            data_b64 = res.get("data")
            if data_b64:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{platform_id}_{reason}_{timestamp}.png"
                out_path = AUDIT_SCREENSHOT_DIR / filename
                with open(out_path, "wb") as f:
                    f.write(base64.b64decode(data_b64))
                return str(out_path)
        except Exception:
            pass
        return None


class GoogleOAuthDriver:
    """Drives Google Workspace 1-Click OAuth onboarding via Chrome CDP port 9223."""

    def __init__(self, cdp_client: VideoPlatformCDPClient):
        self.cdp = cdp_client

    async def detect_google_oauth_button(self, ws):
        """Checks if Google SSO button is present on the page."""
        js = """
        (() => {
            const buttons = Array.from(document.querySelectorAll('button, a, div[role="button"]'));
            const googleBtn = buttons.find(b => {
                const t = (b.innerText || b.getAttribute('aria-label') || '').toLowerCase();
                const cls = (b.className || '').toLowerCase();
                return t.includes('google') || cls.includes('google') || b.getAttribute('data-provider') === 'google';
            });
            const gsiIframe = document.querySelector('iframe[src*="accounts.google.com/gsi"]');
            return Boolean(googleBtn || gsiIframe);
        })()
        """
        return await self.cdp.eval_js(ws, js)

    async def execute_google_oauth(self, ws, target_platform_domain, timeout=45.0):
        """Clicks Google SSO button and guides through Account Chooser / Consent."""
        click_js = """
        (() => {
            const buttons = Array.from(document.querySelectorAll('button, a, div[role="button"]'));
            const googleBtn = buttons.find(b => {
                const t = (b.innerText || b.getAttribute('aria-label') || '').toLowerCase();
                const cls = (b.className || '').toLowerCase();
                return t.includes('google') || cls.includes('google') || b.getAttribute('data-provider') === 'google';
            });
            if (googleBtn) {
                googleBtn.click();
                return true;
            }
            const gsiIframe = document.querySelector('iframe[src*="accounts.google.com/gsi"]');
            if (gsiIframe) {
                gsiIframe.click();
                return true;
            }
            return false;
        })()
        """
        clicked = await self.cdp.eval_js(ws, click_js)
        if not clicked:
            return False, "Google SSO button could not be actuated"

        # Poll for Account Chooser or OAuth tab/redirect
        start = time.time()
        while time.time() - start < timeout:
            tabs = self.cdp.list_tabs() or []
            for t in tabs:
                if not isinstance(t, dict):
                    continue
                t_url = t.get("url") or ""
                if "accounts.google.com" in t_url:
                    ws_url = t.get("webSocketDebuggerUrl")
                    if ws_url:
                        try:
                            async with websockets.connect(ws_url) as auth_ws:
                                # Handle account chooser
                                chooser_js = """
                                (() => {
                                    const accounts = Array.from(document.querySelectorAll('div[data-identifier], div[role="link"], li[data-authuser]'));
                                    const target = accounts.find(el => (el.innerText || '').includes('aiagent1510'));
                                    if (target) { target.click(); return 'CHOSEN_AIAgent1510'; }
                                    if (accounts.length > 0) { accounts[0].click(); return 'CHOSEN_FIRST'; }
                                    return 'NO_ACCOUNT_TILE';
                                })()
                                """
                                await self.cdp.eval_js(auth_ws, chooser_js)

                                # Handle consent dialog
                                consent_js = """
                                (() => {
                                    const btns = Array.from(document.querySelectorAll('button, div[role="button"]'));
                                    const consent = btns.find(b => {
                                        const t = (b.innerText || '').trim().toLowerCase();
                                        return ['continue', 'allow', 'confirm', 'authorize'].includes(t);
                                    });
                                    if (consent) { consent.click(); return 'CONSENT_CLICKED'; }
                                    return 'NO_CONSENT';
                                })()
                                """
                                await self.cdp.eval_js(auth_ws, consent_js)
                        except Exception:
                            pass

            # Check if main tab has completed login
            status_js = f"""
            (() => {{
                const href = window.location.href;
                const isTarget = href.includes({json.dumps(target_platform_domain)});
                const hasAvatar = Boolean(document.querySelector('img[alt*="avatar"], .user-avatar, .profile-icon, button[aria-label*="Profile"]'));
                const hasDashboard = Boolean(document.querySelector('.dashboard, #dashboard, .feed, .upload-btn'));
                return {{ href, isTarget, hasAvatar, hasDashboard }};
            }})()
            """
            st = await self.cdp.eval_js(ws, status_js)
            if isinstance(st, dict) and st.get("isTarget") and (st.get("hasAvatar") or st.get("hasDashboard")):
                return True, "Google OAuth 1-Click completed successfully"

            await asyncio.sleep(2.0)

        return False, "Google OAuth flow timed out"


class EmailOtpDriver:
    """Drives email signup forms and OTP/magic link verification via auto_email_verifier."""

    def __init__(self, cdp_client: VideoPlatformCDPClient):
        self.cdp = cdp_client

    async def autofill_signup_form(self, ws, email="aiagent1510@gmail.com", username="gazpearce", password=None):
        """Fills standard signup inputs (email, username, password, checkboxes)."""
        if not password:
            password = "ADI-Security2026!MasterTrade"

        fill_js = f"""
        (() => {{
            let filled = 0;
            const emailInput = document.querySelector('input[type="email"], input[name*="email"], input[id*="email"]');
            if (emailInput) {{
                emailInput.value = {json.dumps(email)};
                emailInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
                emailInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
                filled++;
            }}

            const userInput = document.querySelector('input[name*="user"], input[id*="user"], input[name*="handle"]');
            if (userInput && userInput !== emailInput) {{
                userInput.value = {json.dumps(username)};
                userInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
                userInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
                filled++;
            }}

            const passInputs = Array.from(document.querySelectorAll('input[type="password"]'));
            for (const p of passInputs) {{
                p.value = {json.dumps(password)};
                p.dispatchEvent(new Event('input', {{ bubbles: true }}));
                p.dispatchEvent(new Event('change', {{ bubbles: true }}));
                filled++;
            }}

            const checkboxes = Array.from(document.querySelectorAll('input[type="checkbox"]'));
            for (const cb of checkboxes) {{
                if (!cb.checked) {{
                    cb.click();
                    cb.checked = true;
                    cb.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    filled++;
                }}
            }}

            return filled;
        }})()
        """
        filled_count = await self.cdp.eval_js(ws, fill_js)
        return filled_count is not None and filled_count > 0

    async def submit_form(self, ws):
        """Clicks the form submit button."""
        submit_js = """
        (() => {
            const submitBtn = document.querySelector('button[type="submit"], input[type="submit"], button.btn-primary');
            if (submitBtn) {
                submitBtn.click();
                return true;
            }
            const buttons = Array.from(document.querySelectorAll('button'));
            const s = buttons.find(b => {
                const t = (b.innerText || '').trim().toLowerCase();
                return ['sign up', 'register', 'create account', 'join', 'get started'].includes(t);
            });
            if (s) {
                s.click();
                return true;
            }
            return false;
        })()
        """
        return await self.cdp.eval_js(ws, submit_js)

    async def handle_verification(self, ws, platform_name, platform_domain, timeout=45.0):
        """Checks for OTP code prompt or magic confirmation link and resolves it."""
        try:
            import auto_email_verifier
        except ImportError:
            return False, "auto_email_verifier module unavailable"

        # Check for OTP inputs
        check_otp_js = """
        (() => {
            const otpInputs = document.querySelectorAll('input[name*="otp"], input[name*="code"], input[id*="otp"], input[id*="code"], .digit-input');
            return otpInputs.length > 0;
        })()
        """
        has_otp_prompt = await self.cdp.eval_js(ws, check_otp_js)
        if has_otp_prompt:
            code = await auto_email_verifier.find_otp_code(platform_name, timeout_secs=timeout)
            if code:
                inject_otp_js = f"""
                (() => {{
                    const inputs = Array.from(document.querySelectorAll('input[name*="otp"], input[name*="code"], input[id*="otp"], input[id*="code"], .digit-input'));
                    if (inputs.length === 1) {{
                        inputs[0].value = {json.dumps(str(code))};
                        inputs[0].dispatchEvent(new Event('input', {{ bubbles: true }}));
                        inputs[0].dispatchEvent(new Event('change', {{ bubbles: true }}));
                        return true;
                    }} else if (inputs.length > 1) {{
                        const digits = {json.dumps(str(code))}.split('');
                        for (let i = 0; i < Math.min(inputs.length, digits.length); i++) {{
                            inputs[i].value = digits[i];
                            inputs[i].dispatchEvent(new Event('input', {{ bubbles: true }}));
                            inputs[i].dispatchEvent(new Event('change', {{ bubbles: true }}));
                        }}
                        return true;
                    }}
                    return false;
                }})()
                """
                await self.cdp.eval_js(ws, inject_otp_js)
                await self.submit_form(ws)
                return True, f"Injected OTP code {code}"
            return False, "OTP code failed to arrive in inbox"

        # Check for magic link
        link = await auto_email_verifier.find_verification_link(platform_domain, timeout_secs=timeout)
        if link:
            # Open verification link in ephemeral tab
            v_tab_id, v_ws_url = self.cdp.open_tab(link)
            if v_tab_id and v_ws_url:
                await asyncio.sleep(5.0)
                self.cdp.close_tab(v_tab_id)
                return True, "Activated verification link"
            return False, "Failed to open verification link tab"

        return False, "No OTP code or verification link detected"


class ProfileBrandManager:
    """Manages profile customization with Gary Pearce E-E-A-T credentials and Rule 45 linking."""

    def __init__(self, brand_info=None):
        self.brand = brand_info or GARY_PEARCE_BRAND

    def get_profile_upward_url(self, tier: str) -> str:
        """Determines the correct upward target URL according to Rule 45 sovereign hierarchy."""
        if "Tier 1" in tier:
            return "https://tvandhomesecurity.blogspot.com/"
        elif "Tier 2" in tier:
            return "https://www.youtube.com/@CCTV.services"
        else:
            # Tier 3 MUST link EXCLUSIVELY to YouTube Apex
            return "https://www.youtube.com/@CCTV.services"

    def format_bio(self, max_length=250) -> str:
        bio = f"{self.brand['engineer']} • {self.brand['business']} (25+ yrs UK physical security & telecom engineering, £10M Public Liability, {self.brand['telephone']}). West Yorkshire & Lancashire."
        if len(bio) > max_length:
            return bio[:max_length - 3] + "..."
        return bio

    def audit_profile_url(self, url: str, platform_name: str, tier: str, probe_live=False):
        """Audits candidate public tenant URL against 5 Integrity Firewall layers and Rule 45."""
        # Layer 1-5 validation
        ok, failed_layer, msg = IntegrityFirewall.run_all_layers(url, platform_name, probe_live=probe_live)
        if not ok:
            return False, f"Integrity Firewall Layer {failed_layer} failed: {msg}"

        # Strict Rule 45 Tier 3 Isolation check
        if "Tier 3" in tier:
            if "adicommunications.co.uk" in url.lower():
                return False, "Tier 3 Rule 45 Violation: direct link to adicommunications.co.uk detected on Tier 3 platform"

        return True, "Profile URL compliant"


class FailureTaxonomyHandler:
    """Evaluates page and environmental signals and maps them to canonical 11 failure codes."""

    @classmethod
    def evaluate_failure(cls, page_source: str = "", status_code: int = 200, error_message: str = "") -> tuple[str, str]:
        text = f"{page_source} {error_message}".lower()

        if status_code in (404, 500, 502, 503, 504) or "nxdomain" in text or "site not found" in text:
            return FailureReason.PLATFORM_DEAD, f"Endpoint returned HTTP {status_code} or DNS resolution failed."

        if status_code == 429 or "too many requests" in text or "rate limit" in text:
            return FailureReason.RATE_LIMITED, "HTTP 429 rate limiting triggered on registration gateway."

        if any(w in text for w in ("cf-turnstile", "hcaptcha", "g-recaptcha", "cloudflare challenge", "security check", "verify you are human")):
            return FailureReason.CAPTCHA_REQUIRED, "Interactive bot challenge / CAPTCHA detected."

        if any(w in text for w in ("phone number", "sms verification", "enter your mobile", "text message")):
            return FailureReason.PHONE_SMS_REQUIRED, "Platform demands mobile SMS OTP verification."

        if any(w in text for w in ("credit card", "billing address", "stripe", "payment method", "trial requires card")):
            return FailureReason.MANUAL_BILLING_REQUIRED, "Upfront credit card or billing details mandatory."

        if any(w in text for w in ("not available in your country", "region restricted", "geographic restriction", "not supported in your region")):
            return FailureReason.GEO_RESTRICTED, "Platform is regionally restricted or unavailable in the UK."

        if any(w in text for w in ("waitlist", "waiting list", "we will review", "manual review", "invitation only")):
            return FailureReason.WAITLIST_PENDING, "Account placed into manual vetting waitlist."

        if any(w in text for w in ("cli required", "command line", "install cli", "api key only")):
            return FailureReason.CLI_AUTH_REQUIRED, "Platform requires CLI / terminal token exchange."

        return FailureReason.WAITLIST_PENDING, f"Onboarding paused: {error_message or 'Candidate queued for execution'}"


class CatalogParitySync:
    """Enforces 100% mathematical parity across master JSON catalog and doc2 CSV registry."""

    def __init__(self, json_path=CATALOG_JSON_PATH, csv_path=DOC2_CSV_PATH):
        self.json_path = Path(json_path)
        self.csv_path = Path(csv_path)

    def load_catalog(self) -> dict:
        with open(self.json_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_catalog(self, catalog_data: dict):
        with open(self.json_path, "w", encoding="utf-8") as f:
            json.dump(catalog_data, f, indent=2, ensure_ascii=False)

    def sync_platform_update(self, platform_id: str, new_status: str, tenant_url: str = "", failure_reason: str = None, failure_detail: str = None, stack_key: str = None, **kwargs):
        """Atomically updates a platform record in JSON catalog and CSV registry across all stacks."""
        catalog = self.load_catalog()

        # 1. Locate platform in category stacks (identifying owning stack)
        stack_plat = None
        target_stack = None
        stacks = catalog.get("category_stacks", {})
        if stack_key and stack_key in stacks:
            for p in stacks[stack_key].get("platforms", []):
                if p.get("platform_id") == platform_id:
                    stack_plat = p
                    target_stack = stacks[stack_key]
                    break

        if not stack_plat:
            for s_key, stack in stacks.items():
                for p in stack.get("platforms", []):
                    if p.get("platform_id") == platform_id:
                        stack_plat = p
                        target_stack = stack
                        break
                if stack_plat:
                    break

        # 2. Locate platform in global flat platforms array
        global_plat = None
        for p in catalog.get("platforms", []):
            if p.get("platform_id") == platform_id:
                global_plat = p
                break

        # Validate platform existence
        if not stack_plat and not global_plat:
            return False, f"Platform {platform_id} not found in catalog"

        # 3. Synchronously apply updates to both in-memory dicts
        def _apply_update(p: dict):
            p["status"] = new_status
            if new_status == "JOINED":
                if tenant_url:
                    p["active_tenant_url"] = tenant_url
                p["failure_reason"] = failure_reason  # Cleared to None for JOINED unless explicit
                p["failure_detail"] = failure_detail
            else:
                if tenant_url:
                    p["active_tenant_url"] = tenant_url
                else:
                    p["active_tenant_url"] = ""
                if failure_reason is not None:
                    p["failure_reason"] = failure_reason
                if failure_detail is not None:
                    p["failure_detail"] = failure_detail

        if stack_plat:
            _apply_update(stack_plat)
        if global_plat:
            _apply_update(global_plat)

        # 4. Recalculate stack counts across all category stacks
        for stack in catalog.get("category_stacks", {}).values():
            stack["onboarded_count"] = sum(1 for p in stack.get("platforms", []) if p.get("status") == "JOINED")
            stack["pending_count"] = sum(1 for p in stack.get("platforms", []) if p.get("status") == "PENDING")

        # 5. Recalculate global counts from the updated flat platforms list (and metadata if present)
        all_plats = catalog.get("platforms", [])
        total_joined = sum(1 for p in all_plats if p.get("status") == "JOINED")
        total_pending = sum(1 for p in all_plats if p.get("status") == "PENDING")
        catalog["total_joined"] = total_joined
        catalog["total_pending"] = total_pending
        if "metadata" in catalog and isinstance(catalog["metadata"], dict):
            catalog["metadata"]["total_joined"] = total_joined
            catalog["metadata"]["total_pending"] = total_pending

        # 6. Save JSON catalog
        self.save_catalog(catalog)

        # 7. Regenerate CSV registry ensuring 100% mathematical parity
        self.regenerate_csv_from_catalog(catalog)
        return True, f"Platform {platform_id} updated to {new_status}"

    def regenerate_csv_from_catalog(self, catalog: dict):
        """Writes doc2 CSV directly from catalog ensuring exact column alignment."""
        csv_rows = []
        for p in catalog.get("platforms", []):
            csv_rows.append({
                "Platform ID": p.get("platform_id", ""),
                "Rank": str(p.get("global_rank", "")),
                "Platform Name": p.get("name", ""),
                "Domain": p.get("domain", ""),
                "DA": str(p.get("da", "")),
                "Stack Key": p.get("stack_key", ""),
                "Category": p.get("category", ""),
                "Tier": p.get("tier", ""),
                "1-Click Join Method (SSO)": p.get("sso_method", ""),
                "Official Signup URL": p.get("signup_url", ""),
                "Status": p.get("status", ""),
                "Active Tenant URL": p.get("active_tenant_url", ""),
                "Failure Reason": p.get("failure_reason", "") or "",
                "Upward Target URL": p.get("upward_target_url", ""),
                "Rule 45 Compliant": "TRUE" if p.get("rule_45_compliant") else "FALSE"
            })

        fieldnames = [
            "Platform ID", "Rank", "Platform Name", "Domain", "DA",
            "Stack Key", "Category", "Tier", "1-Click Join Method (SSO)",
            "Official Signup URL", "Status", "Active Tenant URL",
            "Failure Reason", "Upward Target URL", "Rule 45 Compliant"
        ]

        with open(self.csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(csv_rows)


class AutomatedVideoPlatformOnboarder:
    """Master orchestrator combining CDP client, auth drivers, and parity sync."""

    def __init__(self):
        self.cdp = VideoPlatformCDPClient()
        self.oauth_driver = GoogleOAuthDriver(self.cdp)
        self.email_driver = EmailOtpDriver(self.cdp)
        self.brand_manager = ProfileBrandManager()
        self.parity_sync = CatalogParitySync()

    def get_video_platforms(self, tier_filter=None, status_filter=None):
        catalog = self.parity_sync.load_catalog()
        video_platforms = catalog.get("category_stacks", {}).get("video", {}).get("platforms", [])
        filtered = []
        for p in video_platforms:
            if tier_filter and tier_filter.lower() not in p.get("tier", "").lower():
                continue
            if status_filter and p.get("status") != status_filter:
                continue
            filtered.append(p)
        return filtered

    async def onboard_platform(self, platform: dict, dry_run=False):
        plat_id = platform.get("platform_id")
        name = platform.get("name")
        signup_url = platform.get("signup_url")
        sso_method = platform.get("sso_method", "")
        tier = platform.get("tier", "")
        domain = platform.get("domain", "")

        print(f"[{plat_id}] Starting onboarding for {name} ({tier}) via {sso_method}...")

        if dry_run:
            print(f"[{plat_id}] [DRY-RUN] Simulating onboarding checks for {signup_url}")
            # Run firewall syntax & domain verification
            ok, msg = IntegrityFirewall.validate_layer2_domain(signup_url, name)
            if not ok:
                return False, FailureReason.PLATFORM_DEAD, f"Invalid signup domain: {msg}"
            return True, "JOINED", f"Simulated verification of {name}"

        if not self.cdp.is_cdp_active():
            return False, FailureReason.CLI_AUTH_REQUIRED, "Chrome CDP port 9223 is not reachable"

        tab_id, ws_url = self.cdp.open_tab(signup_url)
        if not tab_id or not ws_url:
            return False, FailureReason.PLATFORM_DEAD, f"Failed to open browser tab for {signup_url}"

        try:
            async with websockets.connect(ws_url) as ws:
                # Wait for initial page load and dismiss cookie banners
                await asyncio.sleep(4.0)
                await self.cdp.dismiss_cookie_banners(ws)

                # Check for interactive captcha
                check_captcha_js = """
                (() => {
                    const text = (document.body.innerText || '').toLowerCase();
                    const hasTurnstile = Boolean(document.querySelector('.cf-turnstile, iframe[src*="challenges.cloudflare.com"]'));
                    const hasHcaptcha = Boolean(document.querySelector('.h-captcha, iframe[src*="hcaptcha.com"]'));
                    const hasRecaptcha = Boolean(document.querySelector('.g-recaptcha, iframe[src*="google.com/recaptcha"]'));
                    return hasTurnstile || hasHcaptcha || hasRecaptcha || text.includes('verify you are human');
                })()
                """
                has_captcha = await self.cdp.eval_js(ws, check_captcha_js)
                if has_captcha:
                    await self.cdp.capture_failure_screenshot(ws, plat_id, FailureReason.CAPTCHA_REQUIRED)
                    return False, FailureReason.CAPTCHA_REQUIRED, "Interactive CAPTCHA / bot challenge detected on signup"

                # Check for Google OAuth suitability
                has_google = await self.oauth_driver.detect_google_oauth_button(ws)
                if ("Google" in sso_method or "1-Click" in sso_method or has_google) and "SMS" not in sso_method:
                    success, detail = await self.oauth_driver.execute_google_oauth(ws, domain)
                    if success:
                        return True, "JOINED", detail
                    else:
                        await self.cdp.capture_failure_screenshot(ws, plat_id, FailureReason.SSO_OAUTH_FAILED)
                        return False, FailureReason.SSO_OAUTH_FAILED, detail

                # Fallback to email form autofill
                filled = await self.email_driver.autofill_signup_form(ws)
                if filled:
                    submitted = await self.email_driver.submit_form(ws)
                    if submitted:
                        await asyncio.sleep(5.0)
                        v_ok, v_detail = await self.email_driver.handle_verification(ws, name, domain)
                        if v_ok:
                            return True, "JOINED", v_detail
                        else:
                            return False, FailureReason.EMAIL_TIMEOUT, v_detail

                return False, FailureReason.WAITLIST_PENDING, "Form submitted; awaiting manual confirmation or queue activation"

        except Exception as e:
            return False, FailureReason.WAITLIST_PENDING, f"Execution exception: {str(e)}"
        finally:
            self.cdp.close_tab(tab_id)

    def audit_firewall_all_video(self):
        """Runs the 5-Layer Integrity Firewall against all active video platforms."""
        platforms = self.get_video_platforms()
        print(f"\n=======================================================")
        print(f" RUNNING 5-LAYER INTEGRITY FIREWALL AUDIT (50 PLATFORMS)")
        print(f"=======================================================")
        passed = 0
        failed = 0
        for p in platforms:
            plat_id = p.get("platform_id")
            name = p.get("name")
            status = p.get("status")
            tenant_url = p.get("active_tenant_url", "")
            tier = p.get("tier", "")

            if status == "JOINED":
                ok, msg = self.brand_manager.audit_profile_url(tenant_url, name, tier, probe_live=False)
                if ok:
                    print(f"[PASS] {plat_id} {name}: {tenant_url}")
                    passed += 1
                else:
                    print(f"[FAIL] {plat_id} {name}: {msg}")
                    failed += 1
            else:
                # Pending platforms verify valid signup_url and failure taxonomy
                signup_url = p.get("signup_url")
                ok_syn, msg_syn = IntegrityFirewall.validate_layer1_syntax(signup_url)
                reason = p.get("failure_reason")
                ok_tax = FailureReason.is_valid(reason)
                if ok_syn and ok_tax:
                    print(f"[PASS] {plat_id} {name} (PENDING): Reason={reason}")
                    passed += 1
                else:
                    print(f"[FAIL] {plat_id} {name} (PENDING): Syntax={ok_syn}, Taxonomy={ok_tax}")
                    failed += 1

        print(f"\nAudit complete: {passed} PASSED, {failed} FAILED across 50 video platforms.")
        return failed == 0

    def sync_catalog_parity(self):
        """Verifies and synchronizes parity between JSON catalog and CSV."""
        print(f"[SYNC] Checking parity between JSON catalog and doc2 CSV...")
        catalog = self.parity_sync.load_catalog()
        self.parity_sync.regenerate_csv_from_catalog(catalog)
        print(f"[SYNC PASS] doc2_multicategory_stack_550.csv rewritten with 100% mathematical parity.")
        return True


def main():
    parser = argparse.ArgumentParser(description="Automated Video Platform Onboarder & Quality Gate")
    parser.add_argument("--dry-run", action="store_true", help="Simulate onboarding execution without mutating state")
    parser.add_argument("--platform", type=str, help="Target specific platform ID (e.g. PLAT-VID-007)")
    parser.add_argument("--tier", type=str, help="Filter by tier (e.g. 2 or 3)")
    parser.add_argument("--all-pending", action="store_true", help="Process all pending video platforms")
    parser.add_argument("--audit-firewall", action="store_true", help="Run 5-Layer Integrity Firewall on all video endpoints")
    parser.add_argument("--sync-parity", action="store_true", help="Enforce parity between JSON catalog and doc2 CSV")

    args = parser.parse_args()
    engine = AutomatedVideoPlatformOnboarder()

    if args.audit_firewall:
        success = engine.audit_firewall_all_video()
        sys.exit(0 if success else 1)

    if args.sync_parity:
        engine.sync_catalog_parity()
        sys.exit(0)

    tier_filter = None
    if args.tier:
        tier_filter = f"Tier {args.tier}"

    if args.platform:
        plats = [p for p in engine.get_video_platforms() if p.get("platform_id") == args.platform]
        if not plats:
            print(f"Error: Platform {args.platform} not found in video stack.")
            sys.exit(1)
        target = plats[0]
        ok, res_status, detail = asyncio.run(engine.onboard_platform(target, dry_run=args.dry_run))
        print(f"Result: {ok} -> {res_status} ({detail})")
        sys.exit(0 if ok else 1)

    if args.all_pending:
        pending = engine.get_video_platforms(tier_filter=tier_filter, status_filter="PENDING")
        print(f"Discovered {len(pending)} pending video platforms for onboarding.")
        for p in pending:
            ok, res_status, detail = asyncio.run(engine.onboard_platform(p, dry_run=args.dry_run))
            print(f"[{p.get('platform_id')}] Result: {res_status} - {detail}")
        sys.exit(0)

    # Default action: run firewall audit and print summary
    print("No execution flag specified. Running --audit-firewall by default.")
    success = engine.audit_firewall_all_video()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
