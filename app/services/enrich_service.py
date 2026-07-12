import httpx
import re
from bs4 import BeautifulSoup
from app.schemas.maps import Enrichment, EmailInfo, SocialLinks
from app.services.email_service import extract_emails_from_html, verify_emails_batch


SOCIAL_PATTERNS = {
    "linkedin": re.compile(r'https?://(?:www\.)?linkedin\.com/(?:company|in)/[a-zA-Z0-9._-]+'),
    "instagram": re.compile(r'https?://(?:www\.)?instagram\.com/[a-zA-Z0-9._]+'),
    "facebook": re.compile(r'https?://(?:www\.)?facebook\.com/[a-zA-Z0-9._-]+'),
    "twitter": re.compile(r'https?://(?:www\.)?(?:twitter|x)\.com/[a-zA-Z0-9._]+'),
    "youtube": re.compile(r'https?://(?:www\.)?youtube\.com/(?:@|channel/|c/)[a-zA-Z0-9._-]+'),
}


def find_social_links(html: str) -> SocialLinks:
    links = SocialLinks()
    for platform, pattern in SOCIAL_PATTERNS.items():
        match = pattern.search(html)
        if match:
            url = match.group(0)
            if platform == "instagram" and not url.startswith("http"):
                url = "https://" + url
            setattr(links, platform, url)
    return links


async def scrape_website_for_emails(url: str) -> tuple[list[str], SocialLinks]:
    emails = []
    social = SocialLinks()

    pages_to_check = [url]
    if not url.endswith('/'):
        url += '/'
    pages_to_check.extend([
        url + 'contact',
        url + 'contacto',
        url + 'contacto/',
        url + 'about',
        url + 'sobre-nosotros',
        url + 'equipo',
    ])

    async with httpx.AsyncClient(
        timeout=10.0,
        follow_redirects=True,
        headers={"User-Agent": "Mozilla/5.0 (compatible; LeadGenBot/1.0)"}
    ) as client:
        for page_url in pages_to_check:
            try:
                resp = await client.get(page_url)
                if resp.status_code == 200:
                    html = resp.text
                    found_emails = extract_emails_from_html(html)
                    emails.extend(found_emails)

                    page_social = find_social_links(html)
                    if page_social.linkedin and not social.linkedin:
                        social.linkedin = page_social.linkedin
                    if page_social.instagram and not social.instagram:
                        social.instagram = page_social.instagram
                    if page_social.facebook and not social.facebook:
                        social.facebook = page_social.facebook
                    if page_social.twitter and not social.twitter:
                        social.twitter = page_social.twitter
                    if page_social.youtube and not social.youtube:
                        social.youtube = page_social.youtube
            except Exception:
                continue

    unique_emails = list(dict.fromkeys(emails))
    return unique_emails[:5], social


async def enrich_business(website: str | None) -> Enrichment:
    if not website:
        return Enrichment()

    if not website.startswith('http'):
        website = 'https://' + website

    emails_raw, social = await scrape_website_for_emails(website)

    if emails_raw:
        verified = verify_emails_batch(emails_raw)
    else:
        verified = []

    return Enrichment(
        emails=verified,
        social=social
    )
