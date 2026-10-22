"""
auto_email_verifier.py
Autonomous Chrome DevTools Protocol (CDP port 9223) Email & OTP Verification Engine
for Gary Pearce / ADI Communications (admin@adicommunications.co.uk & aiagent1510@gmail.com).

Interface Contract (PROJECT.md):
- get_recent_emails(max_count=10, account=...) -> list of dicts {subject, sender, snippet, fullText, link}
- find_verification_link(platform_domain, account=..., timeout_secs=30) -> string URL or None
- find_otp_code(platform_name, account=..., timeout_secs=30) -> string 4-8 digit/alphanumeric code or None
- get_latest_verification_data() -> backwards-compatible list of dicts {text, code}
"""

import asyncio
import json
import re
import sys
import urllib.parse
import urllib.request
import urllib.error
import websockets

CDP_BASE = "http://127.0.0.1:9223"
DEFAULT_ACCOUNT = "aiagent1510@gmail.com"
BANNED_YEARS = {str(y) for y in range(1900, 2100)}  # Disqualify all years 1900-2099
DISQUALIFIED_PREFIXES = (
    "status code", "error code", "http error", "promo code",
    "discount code", "coupon code", "voucher code", "referral code",
    "postal code", "zip code", "area code", "country code"
)


class AutoEmailVerifier:
    def __init__(self, cdp_base=CDP_BASE):
        self.cdp_base = cdp_base
        self._msg_id = 100

    def _next_id(self):
        self._msg_id += 1
        return self._msg_id

    async def _send_cdp(self, ws, method, params=None, timeout=10.0):
        """Send CDP command over WebSocket and correlate response by msg_id."""
        msg_id = self._next_id()
        msg = {"id": msg_id, "method": method, "params": params or {}}
        try:
            await ws.send(json.dumps(msg))
        except Exception:
            return {}

        loop = asyncio.get_event_loop()
        start = loop.time()
        while loop.time() - start < timeout:
            remaining = max(0.01, timeout - (loop.time() - start))
            try:
                raw = await asyncio.wait_for(ws.recv(), timeout=remaining)
                try:
                    data = json.loads(raw)
                except (json.JSONDecodeError, UnicodeDecodeError, ValueError):
                    continue
                if not isinstance(data, dict):
                    continue
                if data.get("id") == msg_id:
                    res = data.get("result")
                    return res if isinstance(res, dict) else {}
            except (websockets.ConnectionClosed, ConnectionResetError, OSError):
                return {}
            except asyncio.TimeoutError:
                break
            except Exception:
                return {}
        return {}

    def _get_tabs(self):
        """Fetch active browser tabs from CDP endpoint with complete error suppression."""
        req = urllib.request.Request(f"{self.cdp_base}/json")
        try:
            with urllib.request.urlopen(req, timeout=3) as resp:
                raw_bytes = resp.read()
                try:
                    data = json.loads(raw_bytes.decode("utf-8", errors="ignore"))
                    return data if isinstance(data, list) else []
                except (json.JSONDecodeError, UnicodeDecodeError, ValueError):
                    return []
        except (urllib.error.URLError, TimeoutError, OSError, ConnectionRefusedError, Exception):
            return []

    async def get_or_create_gmail_tab(self, account=DEFAULT_ACCOUNT, create_if_missing=False):
        """Select existing Gmail inbox tab or optionally launch an ephemeral one."""
        try:
            raw_tabs = self._get_tabs()
            if not raw_tabs or not isinstance(raw_tabs, list):
                return None, False

            # Filter strictly for genuine top-level page targets on mail.google.com/
            mail_tabs = []
            for t in raw_tabs:
                if not isinstance(t, dict):
                    continue
                if t.get("type") != "page":
                    continue
                url = t.get("url")
                if not isinstance(url, str) or not url.startswith("https://mail.google.com/"):
                    continue
                if url.endswith("/sw.js") or "RotateCookiesPage" in url or "accounts.google.com" in url:
                    continue
                mail_tabs.append(t)

            target_acc = str(account or DEFAULT_ACCOUNT).lower().strip()

            # 1. Match by email in title or URL authuser parameter
            for t in mail_tabs:
                title = str(t.get("title") or "").lower()
                url = str(t.get("url") or "").lower()
                if target_acc in title or f"authuser={target_acc}" in url:
                    return t, False

            # 2. Match standard multi-account URL paths
            if target_acc == "aiagent1510@gmail.com":
                for t in mail_tabs:
                    if "/u/0/" in str(t.get("url") or ""):
                        return t, False
            elif target_acc == "admin@adicommunications.co.uk":
                for t in mail_tabs:
                    if "/u/1/" in str(t.get("url") or ""):
                        return t, False

            # 3. If any mail tab is open and default account requested
            if mail_tabs and target_acc == DEFAULT_ACCOUNT:
                return mail_tabs[0], False

            if not create_if_missing:
                return None, False

            # 4. If target account not currently open and creation requested, launch ephemeral tab via CDP /json/new
            auth_url = f"https://mail.google.com/mail/u/?authuser={urllib.parse.quote(target_acc)}#inbox"
            quoted = urllib.parse.quote(auth_url, safe="")
            endpoint = f"{self.cdp_base}/json/new?{quoted}"
            req_new = urllib.request.Request(endpoint, method="PUT")
            with urllib.request.urlopen(req_new, timeout=5) as resp:
                new_tab = json.loads(resp.read().decode("utf-8", errors="ignore"))
            await asyncio.sleep(4)
            if isinstance(new_tab, dict):
                return new_tab, True
            return None, False
        except Exception as e:
            print(f"[EMAIL-VERIFIER] Tab selection error: {e}")
            return None, False

    def _close_tab(self, tab_id):
        """Close an ephemeral tab by target id."""
        if not tab_id:
            return
        try:
            req = urllib.request.Request(f"{self.cdp_base}/json/close/{tab_id}")
            with urllib.request.urlopen(req, timeout=3):
                pass
        except Exception:
            pass

    async def get_recent_emails(self, max_count=10, account=DEFAULT_ACCOUNT):
        """Extract recent emails from Gmail inbox with guaranteed tab cleanup."""
        tab = None
        is_ephemeral = False
        tab_id = None
        try:
            tab, is_ephemeral = await self.get_or_create_gmail_tab(account)
            if not isinstance(tab, dict):
                return []
            tab_id = tab.get("id")
            ws_url = tab.get("webSocketDebuggerUrl")
            if not ws_url or not isinstance(ws_url, str):
                return []

            async with websockets.connect(ws_url, max_size=20 * 1024 * 1024) as ws:
                extract_js = f"""
                (() => {{
                    const rows = Array.from(document.querySelectorAll('div[role=main] tr[role=row], tr.zA'));
                    return rows.slice(0, {max_count}).map((r, i) => {{
                        const senderEl = r.querySelector('span[email], [data-hovercard-id], td[role=gridcell]:nth-child(4)');
                        const sender = senderEl ? (senderEl.getAttribute('email') || senderEl.innerText || '') : '';
                        const subjectEl = r.querySelector('span[data-thread-id], .bog');
                        const subject = subjectEl ? subjectEl.innerText : '';
                        const snippetEl = r.querySelector('.y2');
                        const snippet = snippetEl ? snippetEl.innerText.replace(/^[\\s\\-\\u200c\\u200b]+/, '').trim() : '';
                        const fullText = (r.innerText || r.textContent || '').replace(/\\s+/g, ' ').trim();
                        return {{
                            index: i,
                            sender: sender.trim(),
                            subject: subject.trim(),
                            snippet: snippet.trim(),
                            fullText: fullText.trim(),
                            link: null
                        }};
                    }});
                }})()
                """
                res = await self._send_cdp(ws, "Runtime.evaluate", {"expression": extract_js, "returnByValue": True})
                emails = res.get("result", {}).get("value", []) if isinstance(res.get("result"), dict) else []
                return emails if isinstance(emails, list) else []
        except Exception as e:
            print(f"[EMAIL-VERIFIER] Error reading emails: {e}")
            return []
        finally:
            if is_ephemeral and tab_id:
                self._close_tab(tab_id)

    @staticmethod
    def extract_otp_from_text(text):
        """Extract OTP / verification code with rigorous false-positive rejection."""
        if not text or not isinstance(text, str):
            return None

        # Clean HTML entities if present
        cleaned = re.sub(r'&[a-zA-Z]+;', ' ', text)
        cleaned_lower = cleaned.lower()

        # Reject promo codes, discount codes, coupon codes unless explicit verification phrase present
        if any(p in cleaned_lower for p in ["promo code", "discount code", "coupon code"]):
            if not any(k in cleaned_lower for k in ["verification code", "verify code", "security code", "one-time", "otp", "confirmation pin"]):
                return None

        def is_valid_otp(val):
            if not val or not isinstance(val, str):
                return False
            val = val.strip()
            digits = re.sub(r'\D', '', val)
            if len(val) < 4:
                return False
            if val.isdigit():
                if len(val) < 4 or len(val) > 8:
                    return False
                # Disqualify all years 1900-2099
                if len(val) == 4 and 1900 <= int(val) <= 2099:
                    return False
                # Disqualify 8-digit date timestamps (YYYYMMDD)
                if len(val) == 8 and val.startswith(("19", "20")):
                    return False
                if val in BANNED_YEARS:
                    return False
            else:
                clean_alpha = re.sub(r'[^A-Za-z0-9]', '', val)
                if len(clean_alpha) < 4:
                    return False
                if len(digits) < 1:
                    return False
                if re.search(r'(?:off|save|disc|promo|deal|free|sale)', val, re.IGNORECASE):
                    return False
            return True

        # Pattern 0: Targeted phrase with spaced 6-digit or 8-digit OTP (e.g. "123 456", "492 847")
        m_spaced = re.search(
            r'(?:verification\s+code|verify\s+code|security\s+code|confirmation\s+(?:pin|code)|one-time\s+(?:passcode|code)|login\s+code|access\s+code|auth(?:entication)?\s+code|otp|pin)[\s:]+(?:is[\s:]+)?(?:please\s+use\s+the\s+following\s+verification\s+code:\s*)?(\d{3}[\s-]\d{3}|\d{4}[\s-]\d{4})\b',
            cleaned, re.IGNORECASE
        )
        if m_spaced:
            val = re.sub(r'[\s-]', '', m_spaced.group(1))
            if is_valid_otp(val):
                return val

        # Pattern A: Labeled verification phrases (alphanumeric like V7042-492847 and 7-digit 0370019)
        m_phrase = re.search(
            r'(?:verification\s+code|verify\s+code|security\s+code|confirmation\s+(?:pin|code)|one-time\s+(?:passcode|code)|login\s+code|access\s+code|auth(?:entication)?\s+code|otp|pin)[\s:]+(?:is[\s:]+)?(?:please\s+use\s+the\s+following\s+verification\s+code:\s*)?([A-Za-z0-9-]*\d[A-Za-z0-9-]*)\b',
            cleaned, re.IGNORECASE
        )
        if m_phrase:
            val = m_phrase.group(1).strip()
            if is_valid_otp(val):
                return val

        # Pattern B: Explicit 'code is: 123456' (excluding status/error codes)
        if not any(dp in cleaned_lower for dp in DISQUALIFIED_PREFIXES):
            m_code = re.search(r'\bcode[:\s]+(?:is[:\s]+)?([A-Za-z0-9-]*\d[A-Za-z0-9-]*)\b', cleaned, re.IGNORECASE)
            if m_code:
                val = m_code.group(1).strip()
                if is_valid_otp(val):
                    return val

        # Pattern C: Standalone 6-to-8 digit numeric code (isolated from phone numbers)
        for match in re.finditer(r'(?<!\d)(?<!\d\s)\b(\d{6,8})\b(?!\s*\d)', cleaned):
            val = match.group(1)
            if is_valid_otp(val):
                return val

        # Pattern D: Standalone spaced 6-digit (e.g. "123 456") if verification keywords present (isolated from phone numbers)
        if any(k in cleaned_lower for k in ["verify", "code", "pin", "confirm", "otp", "passcode"]):
            for match in re.finditer(r'(?<!\d)(?<!\d\s)\b(\d{3})\s+(\d{3})\b(?!\s*\d)', cleaned):
                val = f"{match.group(1)}{match.group(2)}"
                if is_valid_otp(val):
                    return val

        # Pattern E: Standalone 4-to-5 digit numeric code if verification keywords present
        if any(k in cleaned_lower for k in ["verify", "code", "pin", "confirm", "otp", "passcode"]):
            for match in re.finditer(r'(?<!\d)(?<!\d\s)\b(\d{4,5})\b(?!\s*\d)', cleaned):
                val = match.group(1)
                if is_valid_otp(val):
                    return val

        return None

    async def find_otp_code(self, platform_name, account=DEFAULT_ACCOUNT, timeout_secs=30):
        """Poll recent emails for OTP matching target platform."""
        loop = asyncio.get_event_loop()
        start_time = loop.time()
        plat_lower = str(platform_name or "").lower().strip()

        while loop.time() - start_time < timeout_secs:
            emails = await self.get_recent_emails(max_count=10, account=account)
            for e in emails:
                if not isinstance(e, dict):
                    continue
                full = str(e.get("fullText") or "")
                subject = str(e.get("subject") or "")
                sender = str(e.get("sender") or "")

                matches_platform = (
                    plat_lower in full.lower() or
                    plat_lower in subject.lower() or
                    plat_lower in sender.lower()
                )
                if matches_platform:
                    code = self.extract_otp_from_text(full)
                    if code:
                        return code
            await asyncio.sleep(2)
        return None

    async def find_verification_link(self, platform_domain, account=DEFAULT_ACCOUNT, timeout_secs=30):
        """Find and extract activation link scoped strictly to platform domain."""
        tab = None
        is_ephemeral = False
        tab_id = None
        try:
            tab, is_ephemeral = await self.get_or_create_gmail_tab(account)
            if not isinstance(tab, dict):
                return None

            tab_id = tab.get("id")
            ws_url = tab.get("webSocketDebuggerUrl")
            if not ws_url or not isinstance(ws_url, str):
                return None

            loop = asyncio.get_event_loop()
            start_time = loop.time()
            plat_domain_clean = str(platform_domain or "").lower().replace("https://", "").replace("http://", "").split("/")[0].strip()
            plat_name = plat_domain_clean.split(".")[0] if "." in plat_domain_clean else plat_domain_clean

            async with websockets.connect(ws_url, max_size=20 * 1024 * 1024) as ws:
                while loop.time() - start_time < timeout_secs:
                    find_row_js = f"""
                    (() => {{
                        const rows = Array.from(document.querySelectorAll('div[role=main] tr[role=row], tr.zA'));
                        const platDomain = '{plat_domain_clean}';
                        const platName = '{plat_name}';
                        
                        // Pass 1: Row matches platform AND contains verification intent keywords
                        for (let i = 0; i < Math.min(rows.length, 15); i++) {{
                            const text = (rows[i].innerText || '').toLowerCase();
                            const matchesPlatform = text.includes(platDomain) || (platName.length >= 3 && text.includes(platName));
                            const hasIntent = text.includes('verify') || text.includes('confirm') || text.includes('activate') || text.includes('welcome') || text.includes('code') || text.includes('auth');
                            if (matchesPlatform && hasIntent) {{
                                return {{ found: true, index: i }};
                            }}
                        }}
                        
                        // Pass 2: Row matches platform domain or name
                        for (let i = 0; i < Math.min(rows.length, 15); i++) {{
                            const text = (rows[i].innerText || '').toLowerCase();
                            const matchesPlatform = text.includes(platDomain) || (platName.length >= 3 && text.includes(platName));
                            if (matchesPlatform) {{
                                return {{ found: true, index: i }};
                            }}
                        }}
                        return {{ found: false }};
                    }})()
                    """
                    row_res = await self._send_cdp(ws, "Runtime.evaluate", {"expression": find_row_js, "returnByValue": True})
                    row_data = row_res.get("result", {}).get("value", {}) if isinstance(row_res.get("result"), dict) else {}

                    if row_data.get("found"):
                        idx = row_data.get("index")
                        # Click into email thread
                        click_js = f"""
                        (() => {{
                            const rows = Array.from(document.querySelectorAll('div[role=main] tr[role=row], tr.zA'));
                            if (rows[{idx}]) {{
                                rows[{idx}].click();
                                return true;
                            }}
                            return false;
                        }})()
                        """
                        await self._send_cdp(ws, "Runtime.evaluate", {"expression": click_js, "returnByValue": True})
                        await asyncio.sleep(2)

                        # Extract candidate links from inside the thread
                        extract_links_js = """
                        (() => {
                            const links = Array.from(document.querySelectorAll('div[role=main] a[href]')).map(a => ({
                                href: a.href || '',
                                text: (a.innerText || a.textContent || '').trim().toLowerCase()
                            }));
                            return links;
                        })()
                        """
                        res_links = await self._send_cdp(ws, "Runtime.evaluate", {"expression": extract_links_js, "returnByValue": True})
                        raw_links = res_links.get("result", {}).get("value", []) if isinstance(res_links.get("result"), dict) else []
                        if not isinstance(raw_links, list):
                            raw_links = []

                        disqualified = [
                            "google.com", "gstatic.com", "googleusercontent.com", "youtube.com",
                            "facebook.com", "twitter.com", "x.com", "linkedin.com", "instagram.com",
                            "unsubscribe", "privacy", "terms", "support.google.com", "mail.google.com"
                        ]

                        candidate_links = []
                        for l in raw_links:
                            if not isinstance(l, dict):
                                continue
                            href = str(l.get("href") or "").strip()
                            txt = str(l.get("text") or "").strip().lower()
                            if not href.startswith("http://") and not href.startswith("https://"):
                                continue
                            href_lower = href.lower()
                            if any(d in href_lower for d in disqualified):
                                continue
                            candidate_links.append((href, txt))

                        # Priority 1: Link matches platform domain AND verification keywords
                        target_link = None
                        for href, txt in candidate_links:
                            href_lower = href.lower()
                            matches_plat = (plat_domain_clean in href_lower) or (len(plat_name) >= 3 and plat_name in href_lower)
                            has_intent = any(k in href_lower or k in txt for k in ["confirm", "verify", "activate", "token", "signup", "auth", "validate"])
                            if matches_plat and has_intent:
                                target_link = href
                                break

                        # Priority 2: Link matches platform domain
                        if not target_link:
                            for href, txt in candidate_links:
                                href_lower = href.lower()
                                if (plat_domain_clean in href_lower) or (len(plat_name) >= 3 and plat_name in href_lower):
                                    target_link = href
                                    break

                        # Priority 3: Generic verification link not in disqualified
                        if not target_link:
                            for href, txt in candidate_links:
                                href_lower = href.lower()
                                if any(k in href_lower or k in txt for k in ["confirm", "verify", "activate", "token"]):
                                    target_link = href
                                    break

                        # Reset back to inbox hash
                        await self._send_cdp(ws, "Runtime.evaluate", {"expression": "window.location.hash = '#inbox'; true", "returnByValue": True})
                        await asyncio.sleep(1)

                        if target_link:
                            return target_link

                    await asyncio.sleep(2)
            return None
        except Exception as e:
            print(f"[EMAIL-VERIFIER] Error in find_verification_link: {e}")
            return None
        finally:
            if is_ephemeral and tab_id:
                self._close_tab(tab_id)

    async def get_latest_verification_data(self):
        """Backwards compatibility wrapper for existing callers."""
        tab, _ = await self.get_or_create_gmail_tab()
        if not tab:
            print("[EMAIL-VERIFIER] No active Gmail tab found on port 9223")
            return None

        title_safe = str(tab.get("title") or "").encode("ascii", "replace").decode("ascii")
        print(f"[EMAIL-VERIFIER] Inspecting inbox tab: {title_safe}")

        emails = await self.get_recent_emails(max_count=15)
        print(f"[EMAIL-VERIFIER] Found {len(emails)} recent emails in inbox:")

        results = []
        for e in emails:
            if not isinstance(e, dict):
                continue
            full = str(e.get("fullText") or "")
            code = self.extract_otp_from_text(full)
            is_verify = any(k in full.lower() for k in ["verify", "verification", "confirm", "code", "activate", "welcome"])
            if is_verify:
                results.append({"text": full[:100], "code": code})
                safe_text = full[:80].encode("ascii", "replace").decode("ascii")
                print(f"  -> [MATCH] {safe_text} | Code: {code}")
        return results


# Module-level convenience functions matching PROJECT.md interface contract
_verifier = AutoEmailVerifier()

async def get_recent_emails(max_count=10, account=DEFAULT_ACCOUNT):
    return await _verifier.get_recent_emails(max_count=max_count, account=account)

async def find_verification_link(platform_domain, account=DEFAULT_ACCOUNT, timeout_secs=30):
    return await _verifier.find_verification_link(platform_domain, account=account, timeout_secs=timeout_secs)

async def find_otp_code(platform_name, account=DEFAULT_ACCOUNT, timeout_secs=30):
    return await _verifier.find_otp_code(platform_name, account=account, timeout_secs=timeout_secs)

async def get_latest_verification_data():
    return await _verifier.get_latest_verification_data()


if __name__ == "__main__":
    asyncio.run(get_latest_verification_data())
