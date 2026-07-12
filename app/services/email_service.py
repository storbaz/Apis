import dns.resolver
import socket
import re
import smtplib
from app.schemas.maps import EmailInfo


email_pattern = re.compile(
    r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
)


def extract_emails_from_html(html: str) -> list[str]:
    found = email_pattern.findall(html)
    unique = list(dict.fromkeys(found))
    return [e for e in unique if not e.endswith(('.png', '.jpg', '.gif', '.svg', '.css', '.js'))]


def check_syntax(email: str) -> bool:
    return bool(email_pattern.match(email))


def check_mx_domain(email: str) -> bool:
    domain = email.split('@')[1]
    try:
        records = dns.resolver.resolve(domain, 'MX')
        return len(records) > 0
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN,
            dns.resolver.NoNameservers, dns.exception.DNSException,
            socket.gaierror):
        return False


def verify_email_smtp(email: str) -> str:
    domain = email.split('@')[1]
    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        mx_host = str(mx_records[0].exchange).rstrip('.')
    except Exception:
        return "unknown"

    try:
        with smtplib.SMTP(timeout=10) as server:
            server.set_debuglevel(0)
            server.connect(mx_host, 25)
            server.helo("verify.example.com")
            server.mail("verify@example.com")
            code, _ = server.rcpt(email)
            if code == 250:
                return "deliverable"
            elif code == 550:
                return "undeliverable"
            else:
                return "risky"
    except smtplib.SMTPServerDisconnected:
        return "unknown"
    except smtplib.SMTPConnectError:
        return "unknown"
    except socket.timeout:
        return "unknown"
    except Exception:
        return "unknown"


def verify_email(email: str) -> EmailInfo:
    if not check_syntax(email):
        return EmailInfo(email=email, status="invalid", type="invalid")

    if not check_mx_domain(email):
        return EmailInfo(email=email, status="undeliverable", type="no_mx")

    status = verify_email_smtp(email)

    local_part = email.split('@')[0].lower()
    generic_words = ('info', 'contact', 'hello', 'admin', 'support', 'sales', 'office', 'mail', 'webmaster')
    email_type = "generic" if local_part in generic_words else "personal"

    return EmailInfo(email=email, status=status, type=email_type)


def verify_emails_batch(emails: list[str]) -> list[EmailInfo]:
    results = []
    for email in emails[:5]:
        result = verify_email(email)
        results.append(result)
    return results
