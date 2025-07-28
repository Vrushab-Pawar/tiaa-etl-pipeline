import scrapy
from datetime import datetime

class BankrateSpider(scrapy.Spider):
    name = "bankrate_spider"
    allowed_domains = ["bankrate.com"]
    start_urls = ["https://www.bankrate.com/mortgages/mortgage-rates/"]

    def parse(self, response):
        today = datetime.now().strftime("%Y-%m-%d")
        rows = response.css('div[aria-labelledby="purchase-0"] table.Table tbody tr')

        for row in rows:
            try:
                product = row.css("th a::text").get()
                rate = row.css("td:nth-of-type(1)::text").get()
                apr = row.css("td:nth-of-type(2)::text").get()

                if not product or not rate or not apr:
                    continue

                yield {
                    "loan_product": product.strip(),
                    "interest_rate": float(rate.replace("%", "").strip()),
                    "apr": float(apr.replace("%", "").strip()),
                    "loan_term_years": self.extract_term(product),
                    "lender_name": "Bankrate",
                    "updated_date": today
                }
            except Exception as e:
                self.logger.warning(f"Error parsing row: {e}")

    def extract_term(self, product):
        for word in product.split():
            if "year" in word.lower():
                return int(word.lower().replace("-year", "").strip())
            elif word.isdigit():
                return int(word)
        return None