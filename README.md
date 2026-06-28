# Arbitrage Pipeline

Scrapes product listings from Google Shopping, Walmart, and eBay, normalizes them into a relational schema, and queries cross-source price gaps.

## How it works

Breadth scrapers collect product listings by search query. Each listing is stored and tied to its source. A matching layer links the same product across sources using SKU first, fuzzy title matching as a fallback. The arbitrage query runs against matched products and ranks by price gap percentage. Airflow schedules daily runs.

## Schema notes

*The schema is available in the db folder as schema.sql*

`product_id` is nullable — unmatched listings are preserved rather than dropped. `is_matched` tracks confidence at the product level. `price_scraped` is separate from `product_listings` to support price history without duplicating listing data.

## Arbitrage query

```sql
SELECT
    p.title,
    ps1.price_usd AS google_price,
    ps2.price_usd AS walmart_price,
    ROUND(((ps2.price_usd - ps1.price_usd) / ps2.price_usd) * 100, 2) AS discount_pct
FROM products p
JOIN product_listings l1  ON p.id = l1.product_id
JOIN sources s1           ON l1.source_id = s1.id AND s1.name = 'google'
JOIN price_scraped ps1    ON l1.id = ps1.product_listings_id
JOIN product_listings l2  ON p.id = l2.product_id
JOIN sources s2           ON l2.source_id = s2.id AND s2.name = 'walmart'
JOIN price_scraped ps2    ON l2.id = ps2.product_listings_id
WHERE ps2.price_usd > ps1.price_usd
ORDER BY discount_pct DESC;
```

## Stack

- Python 3.11+
- Playwright + playwright-stealth
- MySQL
- Airflow
- uv

## Setup

```bash
uv sync
uv run playwright install chromium
mysql -u root -p < db/schema.sql
```

## Structure

```
scraper/
  google_scraper.py
  walmart_scraper.py
  ebay_scraper.py
  loader.py
  logger.py
db/
  schema.sql
dags/
  arbitrage_dag.py
main.py
```
