#!/usr/bin/env python3
"""
workspace_2fa_daemon.py
Autonomous Workspace Verification & 2FA Daemon for Gary Pearce / ADI Communications.
Monitors Chrome DevTools Protocol (CDP port 9223) Gmail inbox (aiagent1510@gmail.com & admin@adicommunications.co.uk).

Features:
- Chrome CDP port 9223 Gmail listener
- SHA-256 fingerprint message deduplication
- OTP regex extraction (filtering Gary Pearce phone 07860 244 274, years, promo codes)
- Dual-tier activation: headless HTTP probe via urllib + CDP Page.navigate ephemeral tab for cookie-dependent platforms
- Non-blocking IPC state (2fa_daemon_state.json, pending_verifications.json, TwoFactorDaemonClient)
- Append-only JSON-Lines audit log (verification_audit.log)
"""

import argparse
import asyncio
import datetime
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import websockets

REPO_ROOT = Path(__file__).resolve().parent

# Defaults
DEFAULT_CDP_HOST = "127.0.0.1"
DEFAULT_CDP_PORT = 9223
DEFAULT_ACCOUNT = "aiagent1510@gmail.com"
DEFAULT_POLL_INTERVAL = 30.0
DEFAULT_BURST_INTERVAL = 5.0

# Sanitization & Filtering Invariants
GARY_PHONE_REGEX = re.compile(
    r"(?:\+?44[\s/.-]*(?:\(0\)|0)?[\s/.-]*)?\(?0?7860\)?[\s/.-]*244[\s/.-]*274\b",
    re.IGNORECASE,
)
GENERIC_UK_PHONE_REGEX = re.compile(
    r"(?:\+?44[\s/.-]*(?:\(0\)|0)?[\s/.-]*|\b0)\(?\d{2,5}\)?[\s/.-]+\d{3,4}[\s/.-]+\d{3,4}\b"
)
BANNED_YEARS = {str(y) for y in range(1900, 2100)}

DISQUALIFIED_PREFIXES = (
    "status code", "error code", "http error", "promo code",
    "discount code", "coupon code", "voucher code", "referral code",
    "postal code", "zip code", "area code", "country code"
)

EXPLICIT_VERIFICATION_KEYWORDS = (
    "verification code", "verify code", "security code",
    "one-time", "otp", "pin", "passcode", "confirmation code", "auth code"
)

DISQUALIFIED_LINK_DOMAINS = (
    "google.com", "gstatic.com", "youtube.com", "facebook.com",
    "twitter.com", "x.com", "linkedin.com", "instagram.com",
    "mail.google.com", "support.google.com", "accounts.google.com"
)

DISQUALIFIED_LINK_FRAGMENTS = (
    "unsubscribe", "optout", "opt-out", "preferences", "privacy", "terms", "help"
)

TARGET_LINK_KEYWORDS = (
    "confirm", "verify", "activate", "signup", "sign-up", "validate", "token", "auth", "welcome"
)


# ==============================================================================
# Configuration Data Model
# ==============================================================================

@dataclass
class TwoFactorDaemonConfig:
    cdp_host: str = DEFAULT_CDP_HOST
    cdp_port: int = DEFAULT_CDP_PORT
    target_account: str = DEFAULT_ACCOUNT
    poll_interval: float = DEFAULT_POLL_INTERVAL
    burst_interval: float = DEFAULT_BURST_INTERVAL
    state_file: Path = REPO_ROOT / "2fa_daemon_state.json"
    pending_file: Path = REPO_ROOT / "pending_verifications.json"
    log_file: Path = REPO_ROOT / "verification_audit.log"
    activate_links: bool = True

    @property
    def cdp_base(self) -> str:
        return f"http://{self.cdp_host}:{self.cdp_port}"


# ==============================================================================
# OTP & Link Extraction Engine
# ==============================================================================

def sanitize_text_for_otp(text: str) -> str:
    """Strips Gary Pearce direct telephone numbers and generic UK phone formats."""
    if not text:
        return ""
    # 1. Strip Gary Pearce phone numbers
    cleaned = GARY_PHONE_REGEX.sub(" ", text)
    # 2. Strip generic UK phone numbers
    cleaned = GENERIC_UK_PHONE_REGEX.sub(" ", cleaned)
    return cleaned


def is_valid_otp(candidate: str) -> bool:
    """Validates extracted candidate code against false positives."""
    if not candidate:
        return False
    norm = candidate.replace(" ", "").replace("-", "")
    length = len(norm)
    if length < 4 or length > 8:
        return False

    # Check numeric
    if norm.isdigit():
        if norm in BANNED_YEARS:
            return False
        # Reject 8-digit date timestamps starting with 19 or 20
        if length == 8 and norm.startswith(("19", "20")):
            return False
        return True

    # Check alphanumeric
    if norm.isalnum():
        # Must have at least one digit
        if not any(c.isdigit() for c in norm):
            return False
        # Reject discount words
        lower = norm.lower()
        if any(w in lower for w in ("off", "save", "free", "deal")):
            return False
        return True

    return False


def extract_otp_from_text(text: str) -> Optional[str]:
    """
    Extracts verification OTP from text using ranked regex patterns
    while eliminating telephone, promo code, year, and error code false positives.
    """
    if not text:
        return None

    cleaned = sanitize_text_for_otp(text)
    lower = cleaned.lower()

    # Check disqualified prefixes
    has_explicit_keyword = any(k in lower for k in EXPLICIT_VERIFICATION_KEYWORDS)
    if not has_explicit_keyword:
        for prefix in DISQUALIFIED_PREFIXES:
            if prefix in lower:
                # Remove matching prefix line/phrase to avoid false matches
                cleaned = re.sub(re.escape(prefix) + r"[^\n\.\,]*", " ", cleaned, flags=re.IGNORECASE)

    # Pattern 1: Spaced multi-digit codes (e.g. "verification code: 123 456" or "security code 123-456")
    p1 = re.search(
        r"(?:verification\s+code|verify\s+code|security\s+code|confirmation\s+(?:pin|code)|one-time\s+(?:passcode|code)|login\s+code|access\s+code|auth(?:entication)?\s+code|verification|security|confirmation|one-time|login|access|auth|otp|pin)(?:\s+(?:code|pin|passcode|token))?[\s:]+(?:is[\s:]+)?(?:please\s+use\s+the\s+following\s+verification\s+code:\s*)?(\d{3}[\s-]\d{3}|\d{4}[\s-]\d{4})\b",
        cleaned,
        re.IGNORECASE,
    )
    if p1:
        cand = p1.group(1).replace(" ", "").replace("-", "")
        if is_valid_otp(cand):
            return cand

    # Pattern 2: Labeled alphanumeric or numeric codes
    p2 = re.search(
        r"(?:verification\s+code|verify\s+code|security\s+code|confirmation\s+(?:pin|code)|one-time\s+(?:passcode|code)|login\s+code|access\s+code|auth(?:entication)?\s+code|verification|security|confirmation|one-time|login|access|auth|otp|pin)(?:\s+(?:code|pin|passcode|token))?[\s:]+(?:is[\s:]+)?(?:please\s+use\s+the\s+following\s+verification\s+code:\s*)?([A-Za-z0-9-]*\d[A-Za-z0-9-]*)\b",
        cleaned,
        re.IGNORECASE,
    )
    if p2:
        cand = p2.group(1).strip("-")
        if is_valid_otp(cand):
            return cand

    # Pattern 3: Reverse-labeled codes (e.g. "489201 is your verification code")
    p3 = re.search(
        r"\b(\d{3}[\s-]\d{3}|\d{4}[\s-]\d{4}|[A-Za-z0-9-]*\d[A-Za-z0-9-]*)\s+is\s+your\s+(?:(?:[A-Za-z]+\s+)?(?:verification|security|auth|one-time|confirmation)\s+|[A-Za-z]+\s+)?(?:code|pin|passcode)\b",
        cleaned,
        re.IGNORECASE,
    )
    if p3:
        cand = p3.group(1).replace(" ", "").replace("-", "").strip("-")
        if is_valid_otp(cand):
            return cand

    # Pattern 4: Standalone isolated 6-to-8 digits with boundary guards
    p4_matches = re.findall(
        r"(?<![\d\w-])(?<!\d\s)\b(\d{6,8})\b(?!\s*\d)(?!-[\d\w])",
        cleaned,
    )
    for cand in p4_matches:
        if is_valid_otp(cand):
            return cand

    # Pattern 5: Standalone 4-to-5 digits if verification context is present
    if any(k in lower for k in ("verify", "code", "pin", "confirm", "otp", "passcode")):
        p5_matches = re.findall(
            r"(?<![\d\w-])(?<!\d\s)\b(\d{4,5})\b(?!\s*\d)(?!-[\d\w])",
            cleaned,
        )
        for cand in p5_matches:
            if is_valid_otp(cand):
                return cand

    return None


def extract_candidate_links(links: List[str], platform_domain: str = "") -> List[str]:
    """Filters candidate links matching verification intent and platform domain."""
    valid_links = []
    clean_domain = platform_domain.lower().replace("www.", "").strip()

    for raw_url in links:
        if not raw_url or not isinstance(raw_url, str):
            continue
        url = raw_url.strip()
        parsed = urllib.parse.urlparse(url)
        netloc = (parsed.netloc or "").lower()
        path_lower = (parsed.path or "").lower()
        full_lower = url.lower()

        # Reject non-http
        if parsed.scheme not in ("http", "https"):
            continue

        # Reject disqualified link domains
        if any(bad in netloc for bad in DISQUALIFIED_LINK_DOMAINS):
            continue

        # Reject disqualified fragments
        if any(frag in path_lower or frag in full_lower for frag in DISQUALIFIED_LINK_FRAGMENTS):
            continue

        # Domain check if provided
        if clean_domain and clean_domain not in netloc and clean_domain not in full_lower:
            continue

        # Intent check
        if any(intent in path_lower or intent in full_lower for intent in TARGET_LINK_KEYWORDS):
            valid_links.append(url)

    return valid_links


# ==============================================================================
# CDP Driver & Tab Selector
# ==============================================================================

class CDPManager:
    """Manages raw HTTP and WebSocket interactions with Chrome on port 9223."""

    def __init__(self, cdp_base: str):
        self.cdp_base = cdp_base
        self._msg_id = 2000

    def _next_id(self) -> int:
        self._msg_id += 1
        return self._msg_id

    def list_tabs(self) -> List[Dict[str, Any]]:
        """Queries /json with error suppression."""
        req = urllib.request.Request(f"{self.cdp_base}/json")
        try:
            with urllib.request.urlopen(req, timeout=3.0) as resp:
                data = json.loads(resp.read().decode("utf-8", errors="ignore"))
                return data if isinstance(data, list) else []
        except Exception:
            return []

    def get_gmail_tab(self, target_account: str = DEFAULT_ACCOUNT, create_if_missing: bool = False) -> Tuple[Optional[Dict[str, Any]], bool]:
        """
        Selects genuine Gmail inbox tab with strict URL and type filtering,
        matching target account cascade.
        """
        tabs = self.list_tabs()
        if not tabs:
            return None, False

        candidate_tabs = []
        for t in tabs:
            if not isinstance(t, dict):
                continue
            if t.get("type") != "page":
                continue
            url = str(t.get("url") or "")
            if not url.startswith("https://mail.google.com/"):
                continue
            # Strictly reject internal background/worker/cookie routes
            if (
                url.endswith("/sw.js")
                or "RotateCookiesPage" in url
                or "accounts.google.com" in url
                or "accounts/SetOSID" in url
            ):
                continue
            candidate_tabs.append(t)

        if not candidate_tabs:
            if create_if_missing:
                new_tab = self.open_tab(f"https://mail.google.com/mail/u/?authuser={urllib.parse.quote(target_account)}#inbox")
                return new_tab, True
            return None, False

        target_lower = target_account.lower()
        # 1. Exact match on title or url
        for t in candidate_tabs:
            title = str(t.get("title") or "").lower()
            url = str(t.get("url") or "").lower()
            if target_lower in title or f"authuser={target_lower}" in url:
                return t, False

        # 2. Account index match (/u/0/ for aiagent1510@gmail.com)
        if "aiagent1510" in target_lower:
            for t in candidate_tabs:
                if "/u/0/" in str(t.get("url") or ""):
                    return t, False

        # 3. First valid Gmail tab
        return candidate_tabs[0], False

    def open_tab(self, url: str) -> Optional[Dict[str, Any]]:
        """Opens a new tab via PUT /json/new?{encoded_url}."""
        quoted = urllib.parse.quote(url, safe="")
        req = urllib.request.Request(f"{self.cdp_base}/json/new?{quoted}", method="PUT")
        try:
            with urllib.request.urlopen(req, timeout=5.0) as resp:
                return json.loads(resp.read().decode("utf-8", errors="ignore"))
        except Exception:
            return None

    def close_tab(self, tab_id: str) -> bool:
        """Closes tab via GET /json/close/{tab_id}."""
        if not tab_id:
            return False
        try:
            with urllib.request.urlopen(f"{self.cdp_base}/json/close/{tab_id}", timeout=3.0) as resp:
                return resp.status == 200
        except Exception:
            return False

    async def send_cdp(self, ws, method: str, params: Optional[Dict[str, Any]] = None, timeout: float = 10.0) -> Dict[str, Any]:
        """Sends a CDP command over WebSocket and returns result."""
        msg_id = self._next_id()
        payload = {"id": msg_id, "method": method, "params": params or {}}
        try:
            await ws.send(json.dumps(payload))
        except Exception:
            return {}

        start = time.time()
        while time.time() - start < timeout:
            rem = max(0.01, timeout - (time.time() - start))
            try:
                raw = await asyncio.wait_for(ws.recv(), timeout=rem)
                data = json.loads(raw)
                if isinstance(data, dict) and data.get("id") == msg_id:
                    res = data.get("result")
                    return res if isinstance(res, dict) else {}
            except Exception:
                return {}
        return {}


# ==============================================================================
# Dual-Tier Link Activation Engine
# ==============================================================================

class LinkActivationEngine:
    """Activates confirmation links via Tier A (urllib HTTP GET) or Tier B (CDP ephemeral tab)."""

    def __init__(self, cdp_manager: CDPManager):
        self.cdp = cdp_manager

    def activate_tier_a_http(self, link_url: str, timeout: float = 8.0) -> Dict[str, Any]:
        """
        Tier A: Lightweight HTTP GET probe via urllib with browser User-Agent.
        Returns dict with status_code, is_confirmed, final_url.
        """
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
            )
        }
        req = urllib.request.Request(link_url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                status = resp.status
                final_url = resp.geturl()
                body = resp.read().decode("utf-8", errors="ignore").lower()

                has_success = any(
                    w in body for w in ("verified", "confirmed", "activated", "success", "welcome", "dashboard")
                )
                has_error = any(
                    w in body for w in ("invalid token", "expired", "already used", "link has expired")
                )

                if status == 200 and has_success and not has_error:
                    return {
                        "activated": True,
                        "method": "urllib_probe",
                        "status_code": status,
                        "landing_url": final_url,
                        "status": "VERIFIED",
                    }
                return {
                    "activated": False,
                    "method": "urllib_probe",
                    "status_code": status,
                    "landing_url": final_url,
                    "status": "NEEDS_BROWSER" if status == 200 else "HTTP_ERROR",
                }
        except urllib.error.HTTPError as e:
            return {
                "activated": False,
                "method": "urllib_probe",
                "status_code": e.code,
                "landing_url": link_url,
                "status": "NEEDS_BROWSER" if e.code in (403, 401) else "HTTP_ERROR",
            }
        except Exception as e:
            return {
                "activated": False,
                "method": "urllib_probe",
                "status_code": 0,
                "landing_url": link_url,
                "status": "EXCEPTION",
                "detail": str(e),
            }

    async def activate_tier_b_cdp(self, link_url: str, timeout: float = 12.0) -> Dict[str, Any]:
        """
        Tier B: CDP Page.navigate inside an ephemeral tab for SPAs, cookie-dependent sessions, or auth walls.
        Guarantees tab cleanup in finally block.
        """
        tab_info = self.cdp.open_tab(link_url)
        if not tab_info:
            return {"activated": False, "method": "cdp_navigate", "status": "TAB_CREATION_FAILED"}

        tab_id = tab_info.get("id")
        ws_url = tab_info.get("webSocketDebuggerUrl")

        try:
            if not ws_url:
                return {"activated": False, "method": "cdp_navigate", "status": "NO_WS_URL"}

            async with websockets.connect(ws_url, max_size=15 * 1024 * 1024) as ws:
                await self.cdp.send_cdp(ws, "Page.enable")
                await self.cdp.send_cdp(ws, "Runtime.enable")

                # Wait for document completion
                wait_expr = """
                new Promise((resolve) => {
                    if (document.readyState === 'complete') resolve(window.location.href);
                    window.addEventListener('load', () => resolve(window.location.href));
                    setTimeout(() => resolve(window.location.href), 4000);
                })
                """
                await self.cdp.send_cdp(ws, "Runtime.evaluate", {"expression": wait_expr, "awaitPromise": True}, timeout=6.0)

                # Wait 2 seconds for client-side JS hydration / token exchange
                await asyncio.sleep(2.0)

                inspect_expr = """
                (() => {
                    const body = (document.body ? document.body.innerText : '').toLowerCase();
                    const url = window.location.href;
                    const isSuccess = body.includes('verified') || body.includes('confirmed') || 
                                      body.includes('activated') || body.includes('welcome') || 
                                      body.includes('dashboard') || body.includes('success');
                    const isError = body.includes('expired') || body.includes('invalid') || body.includes('already used');
                    return { isSuccess, isError, finalUrl: url };
                })()
                """
                res = await self.cdp.send_cdp(ws, "Runtime.evaluate", {"expression": inspect_expr, "returnByValue": True})
                val = res.get("result", {}).get("value", {})

                is_success = val.get("isSuccess", False)
                is_error = val.get("isError", False)
                final_url = val.get("finalUrl", link_url)

                status = "VERIFIED" if (is_success and not is_error) else ("TOKEN_EXPIRED" if is_error else "ACTIVATED")

                return {
                    "activated": True,
                    "method": "cdp_navigate",
                    "status_code": 200,
                    "landing_url": final_url,
                    "status": status,
                }
        except Exception as e:
            return {"activated": False, "method": "cdp_navigate", "status": "EXCEPTION", "detail": str(e)}
        finally:
            if tab_id:
                self.cdp.close_tab(tab_id)

    async def activate_link(self, link_url: str) -> Dict[str, Any]:
        """Dual-tier execution: Tier A HTTP probe, fallback to Tier B CDP navigate."""
        res_a = self.activate_tier_a_http(link_url)
        if res_a.get("activated") and res_a.get("status") == "VERIFIED":
            return res_a
        # Fallback to Tier B
        return await self.activate_tier_b_cdp(link_url)


# ==============================================================================
# Non-Blocking IPC & Client API
# ==============================================================================

class TwoFactorDaemonClient:
    """Non-blocking IPC client for communicating with workspace_2fa_daemon."""

    def __init__(self, repo_root: Optional[Path] = None):
        self.root = Path(repo_root or REPO_ROOT)
        self.state_file = self.root / "2fa_daemon_state.json"
        self.pending_file = self.root / "pending_verifications.json"

    def is_daemon_alive(self, max_heartbeat_age_seconds: float = 45.0) -> bool:
        """Verifies if daemon process is currently running and updating heartbeat."""
        if not self.state_file.exists():
            return False
        try:
            with open(self.state_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            hb_str = data.get("daemon", {}).get("last_heartbeat")
            if not hb_str:
                return False
            hb_time = datetime.datetime.fromisoformat(hb_str.replace("Z", "+00:00"))
            now = datetime.datetime.now(datetime.timezone.utc)
            return (now - hb_time).total_seconds() < max_heartbeat_age_seconds
        except Exception:
            return False

    def request_verification(
        self,
        platform_name: str,
        platform_domain: str,
        expected_type: str = "any",
        timeout_seconds: int = 60,
    ) -> str:
        """Enqueues a pending verification request in pending_verifications.json without blocking."""
        clean_domain = platform_domain.lower().replace("www.", "").strip()
        req_id = f"req_{clean_domain.replace('.', '_')}_{int(time.time())}"

        data = {"version": "1.0", "requests": {}}
        if self.pending_file.exists():
            try:
                with open(self.pending_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                data = {"version": "1.0", "requests": {}}

        if "requests" not in data:
            data["requests"] = {}

        data["requests"][clean_domain] = {
            "request_id": req_id,
            "platform_name": platform_name,
            "platform_domain": clean_domain,
            "account": DEFAULT_ACCOUNT,
            "expected_type": expected_type,
            "requested_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "timeout_seconds": timeout_seconds,
            "status": "PENDING",
        }
        data["updated_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()

        # Atomic write
        tmp = self.pending_file.with_suffix(".tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        os.replace(tmp, self.pending_file)
        return req_id

    def check_status(self, platform_domain: str) -> Optional[Dict[str, Any]]:
        """Non-blocking immediate state check from 2fa_daemon_state.json."""
        if not self.state_file.exists():
            return None
        clean_domain = platform_domain.lower().replace("www.", "").strip()
        try:
            with open(self.state_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            verified = data.get("verified_tokens", {})
            return verified.get(clean_domain)
        except Exception:
            return None

    async def await_token(
        self, platform_domain: str, timeout_seconds: float = 45.0, poll_interval: float = 1.5
    ) -> Optional[Dict[str, Any]]:
        """Asynchronous non-blocking poll with timeout."""
        start = time.time()
        while time.time() - start < timeout_seconds:
            token_data = self.check_status(platform_domain)
            if token_data and token_data.get("status") in ("VERIFIED", "TOKEN_READY"):
                return token_data
            await asyncio.sleep(poll_interval)
        return None


# ==============================================================================
# The Master 2FA Background Daemon
# ==============================================================================

class Workspace2FADaemon:
    """Master background worker polling Chrome CDP port 9223 Gmail inbox."""

    def __init__(self, config: Optional[TwoFactorDaemonConfig] = None):
        self.config = config or TwoFactorDaemonConfig()
        self.cdp = CDPManager(self.config.cdp_base)
        self.activation = LinkActivationEngine(self.cdp)
        self.processed_fingerprints: Set[str] = set()
        self.verified_tokens: Dict[str, Dict[str, Any]] = {}
        self.recent_feed: List[Dict[str, Any]] = []
        self.start_time = time.time()
        self.total_emails_scanned = 0
        self.total_tokens_extracted = 0
        self.total_links_activated = 0

    def _append_audit_log(self, entry: Dict[str, Any]) -> None:
        """Appends JSON-Line record to verification_audit.log."""
        try:
            with open(self.config.log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception:
            pass

    def _load_pending_requests(self) -> Dict[str, Dict[str, Any]]:
        """Reads active requests from pending_verifications.json."""
        if not self.config.pending_file.exists():
            return {}
        try:
            with open(self.config.pending_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data.get("requests", {})
        except Exception:
            return {}

    def _update_pending_request_status(self, domain: str, new_status: str) -> None:
        """Updates request status in pending_verifications.json."""
        if not self.config.pending_file.exists():
            return
        try:
            with open(self.config.pending_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            if domain in data.get("requests", {}):
                data["requests"][domain]["status"] = new_status
                data["updated_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
                tmp = self.config.pending_file.with_suffix(".tmp")
                with open(tmp, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2)
                os.replace(tmp, self.config.pending_file)
        except Exception:
            pass

    def _write_state(self, cdp_connected: bool, status: str = "RUNNING") -> None:
        """Writes 2fa_daemon_state.json atomically."""
        active_interval = (
            self.config.burst_interval
            if any(r.get("status") == "PENDING" for r in self._load_pending_requests().values())
            else self.config.poll_interval
        )
        payload = {
            "daemon": {
                "pid": os.getpid(),
                "status": status,
                "last_heartbeat": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "uptime_seconds": int(time.time() - self.start_time),
                "cdp_port": self.config.cdp_port,
                "cdp_connected": cdp_connected,
                "active_account": self.config.target_account,
                "poll_interval_seconds": active_interval,
                "total_emails_scanned": self.total_emails_scanned,
                "total_tokens_extracted": self.total_tokens_extracted,
                "total_links_activated": self.total_links_activated,
            },
            "verified_tokens": self.verified_tokens,
            "recent_feed": self.recent_feed[-25:],
        }
        try:
            tmp = self.config.state_file.with_suffix(".tmp")
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2)
            os.replace(tmp, self.config.state_file)
        except Exception:
            pass

    async def scan_inbox_once(self) -> Tuple[bool, int]:
        """
        Connects to Gmail tab on CDP port 9223, extracts recent messages,
        extracts OTPs / links, and activates pending verifications.
        """
        tab_info, _ = self.cdp.get_gmail_tab(self.config.target_account)
        if not tab_info:
            return False, 0

        ws_url = tab_info.get("webSocketDebuggerUrl")
        if not ws_url:
            return False, 0

        pending_requests = self._load_pending_requests()
        new_items_processed = 0

        try:
            async with websockets.connect(ws_url, max_size=15 * 1024 * 1024) as ws:
                await self.cdp.send_cdp(ws, "Runtime.enable")

                extract_expr = """
                (() => {
                    const rows = Array.from(document.querySelectorAll('div[role=main] tr[role=row], tr.zA'));
                    return rows.slice(0, 15).map((r, i) => {
                        const senderEl = r.querySelector('span[email], [data-hovercard-id], td[role=gridcell]:nth-child(4)');
                        const sender = senderEl ? (senderEl.getAttribute('email') || senderEl.innerText || '') : '';
                        const subjectEl = r.querySelector('span[data-thread-id], .bog');
                        const subject = subjectEl ? subjectEl.innerText : '';
                        const snippetEl = r.querySelector('.y2');
                        const snippet = snippetEl ? snippetEl.innerText.replace(/^[\\s\\-\\u200c\\u200b]+/, '').trim() : '';
                        const fullText = (r.innerText || r.textContent || '').replace(/\\s+/g, ' ').trim();
                        
                        // Extract links in row preview if visible
                        const links = Array.from(r.querySelectorAll('a[href]')).map(a => a.href);
                        return { index: i, sender: sender.trim(), subject: subject.trim(), snippet: snippet.trim(), fullText: fullText.trim(), links: links };
                    });
                })()
                """
                res = await self.cdp.send_cdp(ws, "Runtime.evaluate", {"expression": extract_expr, "returnByValue": True})
                emails = res.get("result", {}).get("value", [])
                if not emails or not isinstance(emails, list):
                    return True, 0

                self.total_emails_scanned += len(emails)

                for e in emails:
                    sender = re.sub(r"\s+", " ", str(e.get("sender") or "")).strip()
                    subject = re.sub(r"\s+", " ", str(e.get("subject") or "")).strip()
                    snippet = re.sub(r"\s+", " ", str(e.get("snippet") or "")).strip()
                    full_text = str(e.get("fullText") or "")
                    row_links = e.get("links") or []

                    fp = hashlib.sha256(f"{sender}|{subject}|{snippet[:40]}".encode()).hexdigest()[:16]
                    if fp in self.processed_fingerprints:
                        continue

                    self.processed_fingerprints.add(fp)
                    new_items_processed += 1

                    # Extract OTP
                    combined_text = f"{subject} {snippet} {full_text}"
                    otp_code = extract_otp_from_text(combined_text)

                    # Extract Links
                    links = extract_candidate_links(row_links)

                    # Determine associated platform / domain
                    matched_domain = None
                    for domain, req in pending_requests.items():
                        clean_dom = domain.lower().replace("www.", "")
                        plat_name = req.get("platform_name", "").lower()
                        if (
                            clean_dom in sender.lower()
                            or clean_dom in subject.lower()
                            or clean_dom in snippet.lower()
                            or (plat_name and plat_name in subject.lower())
                        ):
                            matched_domain = clean_dom
                            break

                    # Fallback domain from sender
                    if not matched_domain and "@" in sender:
                        matched_domain = sender.split("@")[-1].lower()

                    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()

                    # Handle OTP
                    if otp_code:
                        self.total_tokens_extracted += 1
                        tok_record = {
                            "platform_name": matched_domain or "Unknown",
                            "sender": sender,
                            "subject": subject,
                            "otp_code": otp_code,
                            "verification_link": None,
                            "activated": False,
                            "activation_status_code": None,
                            "landing_url": None,
                            "timestamp": now_iso,
                            "status": "TOKEN_READY",
                        }
                        if matched_domain:
                            self.verified_tokens[matched_domain] = tok_record
                            self._update_pending_request_status(matched_domain, "TOKEN_READY")

                        self.recent_feed.append({
                            "timestamp": now_iso,
                            "platform": matched_domain or sender,
                            "type": "otp",
                            "code": otp_code,
                            "status": "TOKEN_READY",
                        })

                        self._append_audit_log({
                            "timestamp": now_iso,
                            "platform": matched_domain,
                            "action": "OTP_EXTRACTED",
                            "code": otp_code,
                            "sender": sender,
                            "verified_by": "workspace_2fa_daemon",
                        })

                    # Handle Links
                    for link_url in links:
                        act_res = {"activated": False, "status": "SKIPPED"}
                        if self.config.activate_links:
                            act_res = await self.activation.activate_link(link_url)
                            if act_res.get("activated"):
                                self.total_links_activated += 1

                        status_val = act_res.get("status", "EXTRACTED")
                        link_record = {
                            "platform_name": matched_domain or "Unknown",
                            "sender": sender,
                            "subject": subject,
                            "otp_code": None,
                            "verification_link": link_url,
                            "activated": act_res.get("activated", False),
                            "activation_status_code": act_res.get("status_code"),
                            "landing_url": act_res.get("landing_url"),
                            "timestamp": now_iso,
                            "status": status_val,
                        }
                        if matched_domain:
                            self.verified_tokens[matched_domain] = link_record
                            self._update_pending_request_status(matched_domain, status_val)

                        self.recent_feed.append({
                            "timestamp": now_iso,
                            "platform": matched_domain or sender,
                            "type": "link",
                            "status": status_val,
                            "url": link_url,
                        })

                        self._append_audit_log({
                            "timestamp": now_iso,
                            "platform": matched_domain,
                            "action": "LINK_ACTIVATION",
                            "method": act_res.get("method"),
                            "status": act_res.get("status_code"),
                            "landing_url": act_res.get("landing_url"),
                            "verified_by": "workspace_2fa_daemon",
                        })

                return True, new_items_processed

        except Exception as e:
            return False, 0

    async def run_daemon(self) -> None:
        """Main continuous polling loop with dynamic bursting."""
        print(f"[2FA-DAEMON] Starting Workspace 2FA Daemon on CDP port {self.config.cdp_port}")
        print(f"[2FA-DAEMON] Monitoring account: {self.config.target_account}")
        print(f"[2FA-DAEMON] Base poll interval: {self.config.poll_interval}s, Burst interval: {self.config.burst_interval}s")

        while True:
            try:
                ok, processed_count = await self.scan_inbox_once()
                self._write_state(cdp_connected=ok, status="RUNNING")

                # Dynamic Burst Cadence: if any pending requests exist, poll fast (5s)
                pending = self._load_pending_requests()
                has_pending = any(r.get("status") == "PENDING" for r in pending.values())
                interval = self.config.burst_interval if has_pending else self.config.poll_interval

                await asyncio.sleep(interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                self._write_state(cdp_connected=False, status="ERROR")
                await asyncio.sleep(10.0)

    async def run_once(self) -> int:
        """Single-pass inspection (health check)."""
        ok, count = await self.scan_inbox_once()
        status_label = "HEALTHY_ONCE" if ok else "CDP_UNREACHABLE_ONCE"
        self._write_state(cdp_connected=ok, status=status_label)
        print(f"[2FA-DAEMON ONCE] CDP Connected: {ok}, Items Processed: {count}")
        return 0 if ok else 1


# ==============================================================================
# CLI Entrypoint
# ==============================================================================

def parse_args():
    parser = argparse.ArgumentParser(
        description="Autonomous Workspace Verification & 2FA Daemon for Gary Pearce / ADI Communications."
    )
    parser.add_argument("--daemon", action="store_true", help="Run continuously in background polling loop")
    parser.add_argument("--once", action="store_true", help="Execute single-pass inspection, update state, and exit")
    parser.add_argument("--poll-interval", type=float, default=DEFAULT_POLL_INTERVAL, help="Base polling interval")
    parser.add_argument("--burst-interval", type=float, default=DEFAULT_BURST_INTERVAL, help="Burst polling interval")
    parser.add_argument("--port", type=int, default=DEFAULT_CDP_PORT, help="Chrome CDP port")
    parser.add_argument("--host", type=str, default=DEFAULT_CDP_HOST, help="Chrome CDP host")
    parser.add_argument("--account", type=str, default=DEFAULT_ACCOUNT, help="Target Gmail account")
    parser.add_argument("--state-file", type=Path, default=REPO_ROOT / "2fa_daemon_state.json", help="Path to state file")
    parser.add_argument("--pending-file", type=Path, default=REPO_ROOT / "pending_verifications.json", help="Path to pending file")
    parser.add_argument("--log-file", type=Path, default=REPO_ROOT / "verification_audit.log", help="Path to log file")
    parser.add_argument("--activate-links", action="store_true", default=True, help="Auto-activate confirmation links")
    return parser.parse_args()


def main():
    args = parse_args()
    config = TwoFactorDaemonConfig(
        cdp_host=args.host,
        cdp_port=args.port,
        target_account=args.account,
        poll_interval=args.poll_interval,
        burst_interval=args.burst_interval,
        state_file=args.state_file,
        pending_file=args.pending_file,
        log_file=args.log_file,
        activate_links=args.activate_links,
    )
    daemon = Workspace2FADaemon(config)

    if args.daemon:
        try:
            asyncio.run(daemon.run_daemon())
        except KeyboardInterrupt:
            print("\n[2FA-DAEMON] Shutdown signal received. Exiting.")
            sys.exit(0)
    else:
        # Default to --once if not specified
        code = asyncio.run(daemon.run_once())
        sys.exit(code)


if __name__ == "__main__":
    main()
