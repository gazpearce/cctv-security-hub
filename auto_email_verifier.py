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
BANNED_YEARS = {"2024", "2025", "2026", "2027"}


class AutoEmailVerifier:
    def __init__(self, cdp_base=CDP_BASE):
        self.cdp_base = cdp_base
        self._msg_id = 100

    def _next_id(self):
        self._msg_id += 1
        return self._msg_id

    async def _send_cdp(self, ws, method, params=None, timeout=10.0):
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
                data = json.loads(raw)
                if isinstance(data, dict) and data.get("id") == msg_id:
                    res = data.get("result")
                    return res if isinstance(res, dict) else {}
            except (json.JSONDecodeError, AttributeError, UnicodeDecodeError):
                continue
            except asyncio.TimeoutError:
                break
            except Exception:
                return {}
        return {}

    def _get_tabs(self):
        req = urllib.request.Request(f"{self.cdp_base}/json")
        try:
            with urllib.request.urlopen(req, timeout=3) as resp:
                data = json.loads(resp.read().decode())
                return data if isinstance(data, list) else []
        except Exception as e:
            return []

    async def get_or_create_gmail_tab(self, account=DEFAULT_ACCOUNT, create_if_missing=False):
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

        target_acc = (account or DEFAULT_ACCOUNT).lower().strip()

        # 1. Match by email in title or URL authuser parameter
        for t in mail_tabs:
            title = (t.get("title") or "").lower()
            url = (t.get("url") or "").lower()
            if target_acc in title or f"authuser={target_acc}" in url:
                return t, False

        # 2. Match standard multi-account URL paths
        if target_acc == "aiagent1510@gmail.com":
            for t in mail_tabs:
                if "/u/0/" in (t.get("url") or ""):
                    return t, False
        elif target_acc == "admin@adicommunications.co.uk":
            for t in mail_tabs:
                if "/u/1/" in (t.get("url") or ""):
                    return t, False

        # 3. If any mail tab is open and no specific non-default account was requested
        if mail_tabs and target_acc == DEFAULT_ACCOUNT:
            return mail_tabs[0], False

        if not create_if_missing:
            return None, False

        # 4. If target account not currently open and creation requested, launch ephemeral tab via CDP /json/new
        auth_url = f"https://mail.google.com/mail/u/?authuser={urllib.parse.quote(target_acc)}#inbox"
        quoted = urllib.parse.quote(auth_url, safe="")
        endpoint = f"{self.cdp_base}/json/new?{quoted}"
        try:
            req_new = urllib.request.Request(endpoint, method="PUT")
            with urllib.request.urlopen(req_new, timeout=5) as resp:
                new_tab = json.loads(resp.read().decode())
            await asyncio.sleep(4)
            return new_tab, True
        except Exception as e:
            print(f"[EMAIL-VERIFIER] Failed to launch tab for {account}: {e}")
            return None, False

    def _close_tab(self, tab_id):
        try:
            req = urllib.request.Request(f"{self.cdp_base}/json/close/{tab_id}")
            with urllib.request.urlopen(req, timeout=3):
                pass
        except Exception:
            pass

    async def get_recent_emails(self, max_count=10, account=DEFAULT_ACCOUNT):
        tab, is_ephemeral = await self.get_or_create_gmail_tab(account)
        if not tab:
            return []

        ws_url = tab.get("webSocketDebuggerUrl")
        tab_id = tab.get("id")
        if not ws_url:
            if is_ephemeral and tab_id:
                self._close_tab(tab_id)
            return []

        try:
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
                emails = res.get("result", {}).get("value", [])
                return emails or []
        except Exception as e:
            print(f"[EMAIL-VERIFIER] Error reading emails: {e}")
            return []
        finally:
            if is_ephemeral and tab_id:
                self._close_tab(tab_id)

    @staticmethod
    def extract_otp_from_text(text):
        if not text:
            return None

        # Clean HTML entities if present
        cleaned = re.sub(r'&[a-zA-Z]+;', ' ', text)
        cleaned_lower = cleaned.lower()

        # Reject promo codes, discount codes, coupon codes
        if any(p in cleaned_lower for p in ["promo code", "discount code", "coupon code"]):
            return None

        # Helper to validate candidates
        def is_valid_otp(val):
            if not val:
                return False
            digits = re.sub(r'\D', '', val)
            if len(digits) < 4:
                return False
            # Check year boundary (e.g. 1900-2099)
            if len(digits) == 4 and digits.isdigit():
                num = int(digits)
                if 1900 <= num <= 2099:
                    return False
            # Check 8-digit date timestamps (YYYYMMDD)
            if len(digits) == 8 and digits.isdigit():
                if digits.startswith(("19", "20")):
                    return False
            if val in BANNED_YEARS or digits in BANNED_YEARS:
                return False
            return True

        # Pattern 0: Spaced 6-digit codes (e.g. "123 456", "492 847", "829 103", "554 321")
        m_spaced = re.search(
            r'(?:verification code|verify code|security code|confirmation (?:pin|code)|one-time (?:passcode|code)|otp|pin)[\s:]+(?:is[\s:]+)?(\d{3}\s+\d{3})\b',
            cleaned, re.IGNORECASE
        )
        if m_spaced:
            return m_spaced.group(1).replace(" ", "")

        # Check general spaced 6-digit code if confirmation/verification keyword is present
        if any(k in cleaned_lower for k in ["verification", "security", "code", "pin", "otp", "confirm"]):
            m_gen_spaced = re.search(r'\b(\d{3})\s+(\d{3})\b', cleaned)
            if m_gen_spaced:
                return f"{m_gen_spaced.group(1)}{m_gen_spaced.group(2)}"

        # Pattern A: Labeled verification phrases (alphanumeric like V7042-492847 and 7-digit 0370019)
        if not any(k in cleaned_lower for k in ["error code", "status code", "http error"]):
            m_phrase = re.search(
                r'(?:verification code|verify code|security code|confirmation (?:pin|code)|one-time (?:passcode|code)|otp|pin)[\s:]+(?:is[\s:]+)?(?:please\s+use\s+the\s+following\s+verification\s+code:\s*)?([A-Za-z0-9-]*\d[A-Za-z0-9-]*)\b',
                cleaned, re.IGNORECASE
            )
            if m_phrase:
                val = m_phrase.group(1).strip()
                if is_valid_otp(val):
                    return val

        # Pattern B: Explicit 'code is: 123456'
        if not any(k in cleaned_lower for k in ["error code", "status code", "http error"]):
            m_code = re.search(r'\bcode[:\s]+(?:is[:\s]+)?([A-Za-z0-9-]*\d[A-Za-z0-9-]*)\b', cleaned, re.IGNORECASE)
            if m_code:
                val = m_code.group(1).strip()
                if is_valid_otp(val):
                    return val

        # Pattern C: Standalone 6-to-8 digit numeric code
        for match in re.finditer(r'\b(\d{6,8})\b', cleaned):
            val = match.group(1)
            if is_valid_otp(val):
                return val

        # Pattern D: Standalone 4-to-5 digit numeric code if verification keywords present
        if any(k in cleaned_lower for k in ["verify", "code", "pin", "confirm", "otp"]):
            for match in re.finditer(r'\b(\d{4,5})\b', cleaned):
                val = match.group(1)
                if is_valid_otp(val):
                    return val

        return None

    async def find_otp_code(self, platform_name, account=DEFAULT_ACCOUNT, timeout_secs=30):
        loop = asyncio.get_event_loop()
        start_time = loop.time()
        plat_lower = platform_name.lower().strip()

        while loop.time() - start_time < timeout_secs:
            emails = await self.get_recent_emails(max_count=10, account=account)
            for e in emails:
                full = e.get("fullText", "")
                subject = e.get("subject", "")
                sender = e.get("sender", "")

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
        tab, is_ephemeral = await self.get_or_create_gmail_tab(account)
        if not tab:
            return None

        ws_url = tab.get("webSocketDebuggerUrl")
        tab_id = tab.get("id")
        if not ws_url:
            if is_ephemeral and tab_id:
                self._close_tab(tab_id)
            return None

        loop = asyncio.get_event_loop()
        start_time = loop.time()
        plat_domain_clean = platform_domain.lower().replace("https://", "").replace("http://", "").split("/")[0].strip()

        try:
            async with websockets.connect(ws_url, max_size=20 * 1024 * 1024) as ws:
                while loop.time() - start_time < timeout_secs:
                    find_row_js = f"""
                    (() => {{
                        const rows = Array.from(document.querySelectorAll('div[role=main] tr[role=row], tr.zA'));
                        for (let i = 0; i < Math.min(rows.length, 10); i++) {{
                            const text = (rows[i].innerText || '').toLowerCase();
                            const matchesPlatform = text.includes('{plat_domain_clean}');
                            const hasIntent = text.includes('verify') || text.includes('confirm') || text.includes('activate') || text.includes('welcome') || text.includes('code');
                            if (matchesPlatform && hasIntent) {{
                                return {{ found: true, index: i }};
                            }}
                        }}
                        return {{ found: false }};
                    }})()
                    """
                    row_res = await self._send_cdp(ws, "Runtime.evaluate", {"expression": find_row_js, "returnByValue": True})
                    row_data = row_res.get("result", {}).get("value", {})

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
                                href: a.href,
                                text: (a.innerText || a.textContent || '').trim().toLowerCase()
                            }));
                            return links;
                        })()
                        """
                        res_links = await self._send_cdp(ws, "Runtime.evaluate", {"expression": extract_links_js, "returnByValue": True})
                        links = res_links.get("result", {}).get("value", [])

                        target_link = None
                        disqualified = ["google.com", "gstatic.com", "unsubscribe", "privacy", "terms", "twitter.com", "facebook.com", "support.google.com"]
                        for l in links:
                            href = l.get("href", "")
                            txt = l.get("text", "")
                            if any(d in href.lower() for d in disqualified):
                                continue
                            if any(k in href.lower() or k in txt for k in ["confirm", "verify", "activate", "token", "signup", "auth"]):
                                target_link = href
                                break
                            if plat_domain_clean in href.lower():
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

        title_safe = tab.get("title", "").encode("ascii", "replace").decode("ascii")
        print(f"[EMAIL-VERIFIER] Inspecting inbox tab: {title_safe}")

        emails = await self.get_recent_emails(max_count=15)
        print(f"[EMAIL-VERIFIER] Found {len(emails)} recent emails in inbox:")

        results = []
        for e in emails:
            full = e.get("fullText", "")
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
