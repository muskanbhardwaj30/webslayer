import os
import pandas as pd
import advertools as adv
from utils import url_to_hash, setup_logger
from markdownify import markdownify as md
import mdformat
import re

logger = setup_logger()

CUSTOM_SETTINGS_CRAWLER = {
    "LOG_SHORT_NAMES": True,
    "LOG_LEVEL": "WARNING",
    "SPIDER_LOADER_WARN_ONLY": False,
    "ROBOTSTXT_OBEY": False,
    "RETRY_ENABLED": False,
    "USER_AGENT": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/115.0.0.0 Safari/537.36"
    ),
}


def process_page_data(row: pd.Series, markdown: bool = False):
    page_url = ""

    try:
        if row.get("redirect_urls", ""):
            if isinstance(row["redirect_urls"], str):
                page_url = row["redirect_urls"]
            elif isinstance(row["redirect_urls"], dict):
                page_url = row["redirect_urls"][0]
            elif isinstance(row["redirect_urls"], list):
                page_url = row["redirect_urls"][0]
    except Exception as e:
        logger.warning(
            f"Redirected Link but Problem in URL Parsing: Moving With Same URL: {e}"
        )
        pass

    if not page_url:
        page_url = row.get("url", "")

    full_html = row.get("full_html")

    if markdown and isinstance(full_html, str):
        markdown_text = md(html=full_html)
        cleaned_text = mdformat.text(markdown_text)
    else:
        logger.warning(f"No Data(full_html) found in the Website: {page_url}")
        logger.warning('Using Body Text if available else "" ')
        raw_text = row.get("body_text", "")
        cleaned_text = (
            re.sub(r"\s+", " ", raw_text).strip() if isinstance(raw_text, str) else ""
        )

    return {
        "url": page_url,
        "content": (cleaned_text if len(cleaned_text) >= 100 else ""),
    }


def process_crawl_data(crawl_df: pd.DataFrame, markdown: bool = False):

    seen = set()
    analysis_data = []

    for _, row in crawl_df.iterrows():
        page_data = process_page_data(row, markdown)

        if not page_data:
            continue

        content_hash = hash(page_data["content"])
        unique_key = f"{page_data['url']}-{content_hash}"

        if unique_key not in seen:
            seen.add(unique_key)
            analysis_data.append(page_data)

    return analysis_data


def fetch_and_convert(url: str, cache_dir=".cache", md: bool = True):
    url_hash = url_to_hash(url)
    os.makedirs(cache_dir, exist_ok=True)
    md_path = os.path.join(cache_dir, f"{url_hash}.md")

    if os.path.exists(md_path):
        logger.info(f"[CACHE HIT] Using cached markdown for {url}")
        with open(md_path, "r", encoding="utf-8") as f:
            markdown = f.read()
    else:
        logger.info(f"[SCRAPE] Crawling {url}")
        json_path = os.path.join(cache_dir, f"{url_hash}.jsonl")
        adv.crawl(
            url_list=[url],
            output_file=str(json_path),
            follow_links=False,
            exclude_url_regex=r".*\b(cloudflare|cdn-cgi|cfcdn|cf-images|cf-ipfs|cf-cache|cf-ray|cf-)\b.*",
            custom_settings=CUSTOM_SETTINGS_CRAWLER,
            xpath_selectors={"full_html": "/html"},
        )
        df = pd.read_json(json_path, lines=True)
        try:
            df = df.dropna(subset=["url", "body_text"])

            df = df.loc[
                df.groupby("url")["body_text"].apply(lambda x: x.str.len().idxmax())
            ].reset_index(drop=True)

        except Exception as e:
            logger.warning(f"Deduplication error: {e}")
            pass

        analysis_data = process_crawl_data(df, markdown=md)

        markdown = ""
        with open(md_path, "w", encoding="utf-8") as f:
            for x in analysis_data:
                f.write(str(x))
                markdown += str(x)

        logger.info(f"[CACHE SAVE] Markdown saved to {md_path}")

    return url_hash, markdown
