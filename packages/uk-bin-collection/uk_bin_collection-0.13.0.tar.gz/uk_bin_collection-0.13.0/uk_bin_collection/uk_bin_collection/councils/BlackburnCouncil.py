import json
from collections import OrderedDict
from datetime import datetime

import requests
from uk_bin_collection.uk_bin_collection.common import *
from uk_bin_collection.uk_bin_collection.get_bin_data import \
    AbstractGetBinDataClass


class CouncilClass(AbstractGetBinDataClass):
    """
    Concrete classes have to implement all abstract operations of the
    base class. They can also override some operations with a default
    implementation.
    """

    def parse_data(self, page: str, **kwargs) -> dict:
        # Make a BS4 object

        data = {"bins": []}
        uprn = kwargs.get("uprn")
        current_month = datetime.today().strftime("%m")
        current_year = datetime.today().strftime("%Y")
        url = (
            f"https://mybins.blackburn.gov.uk/api/mybins/getbincollectiondays?uprn={uprn}&month={current_month}"
            f"&year={current_year}"
        )

        # Build request header string, then parse it and get response
        response_header_str = (
            "Accept: application/json, text/plain, */*|Accept-Encoding: gzip, deflate, "
            "br|Accept-Language: en-GB,en;q=0.9|Connection: keep-alive|Host: "
            "mybins.blackburn.gov.uk|Referer: "
            "https://mybins.blackburn.gov.uk/calendar/MTAwMDEwNzUwNzQy|Sec-Fetch-Dest: "
            "empty|Sec-Fetch-Mode: cors|Sec-Fetch-Site: same-origin|Sec-GPC: 1|User-Agent: "
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/103.0.5060.134 Safari/537.36 "
        )
        response_headers = parse_header(response_header_str)
        requests.packages.urllib3.disable_warnings()
        response = requests.get(url, headers=response_headers, verify=False)

        # Return JSON from response and loop through collections
        json_result = json.loads(response.content)
        bin_collections = json_result["BinCollectionDays"]
        for collection in bin_collections:
            if collection is not None:
                bin_type = collection[0].get("BinType")
                current_collection_date = datetime.strptime(
                    collection[0].get("CollectionDate"), "%Y-%m-%d"
                )
                next_collection_date = datetime.strptime(
                    collection[0].get("NextScheduledCollectionDate"), "%Y-%m-%d"
                )

                # Work out the most recent collection date to display
                if (
                        datetime.today().date()
                        <= current_collection_date.date()
                        < next_collection_date.date()
                ):
                    collection_date = current_collection_date
                else:
                    collection_date = next_collection_date

                dict_data = {
                    "type": bin_type,
                    "collectionDate": collection_date.strftime(date_format),
                }
                data["bins"].append(dict_data)

                data["bins"].sort(
                    key=lambda x: datetime.strptime(x.get("collectionDate"), date_format)
                )

        return data
