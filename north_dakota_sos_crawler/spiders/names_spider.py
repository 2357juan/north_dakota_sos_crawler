import logging
from urllib.parse import urljoin
import scrapy

single_entity_types = {
    "Owner Name",
    "Commercial Registered Agent",
    "Registered Agent"}
multi_entity_types = {"Owners"}


class NamesSpider(scrapy.Spider):
    name = "names"

    base_url = "https://firststop.sos.nd.gov/api/"

    search_url = urljoin(base_url, "Records/businesssearch")

    company_template_url = urljoin(base_url, "FilingDetail/business/{0}/false")

    def start_requests(self):

        self.starting_char = getattr(self, "starting_char", "X")
        request = scrapy.http.JsonRequest(
            url=self.search_url,
            data={
                "SEARCH_VALUE": self.starting_char,
                "STARTS_WITH_YN": "true",
                "ACTIVE_ONLY_YN": True},
            callback=self.parse_table
        )

        yield request

    def parse_table(self, response):
        self.log(
            f"The table response has been received with a status code of \
                {response.status}.",
            level=logging.INFO)
        data = response.json()
        self.log(
            f"The table response has been received with a status code of \
                {response.status}. There are {len(data['rows'])} \
                    rows in the table.",
            level=logging.INFO)
        for company_id, company_name in get_companies(
                data,self.starting_char):
            request = scrapy.http.JsonRequest(
                url=self.company_template_url.format(company_id),
                method="GET",
                headers={
                    "authority": "firststop.sos.nd.gov",
                    "authorization": "undefined",
                },
                callback=self.parse_company,
                meta={"company_name": company_name}
            )
            yield request

    def parse_company(self, response):
        self.log(
            f"The company {response.meta['company_name']} data \
                has been received with a status code of {response.status}.",
            level=logging.INFO)
        data = response.json()
        names = get_names(data)
        names["company_name"] = response.meta['company_name']
        yield names


def get_companies(data,starting_char):
    for company_id, labled_data in data["rows"].items():
        company_name = labled_data["TITLE"][0]
        if company_name.startswith(starting_char):
            yield company_id, company_name


def get_names(data):
    names = []
    details = [{"entiy_type": row["LABEL"], "name": row["VALUE"].split(
        "\n")[0]} for row in data["DRAWER_DETAIL_LIST"]]

    for i in range(len(details)):
        entity_type = details[i]["entiy_type"]
        name = details[i]["name"]
        if entity_type in multi_entity_types:
            names.append(name)
            j = i + 1
            # works for the case where there can be many owners
            while j < len(details) and details[j]["entiy_type"] == "":
                name = details[j]["name"]
                names.append(name)
                j += 1
            break
        elif entity_type in single_entity_types:
            names.append(name)
            break
    return {"entities": names}
