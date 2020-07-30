import argparse
import requests
import xmltodict

from pprint import pprint
from tqdm import tqdm

from downloader import Downloader
from validator import Validator


class PyCMR:
    """
        Takes concept_ids and runs downloader/validator on each

        1. Can generate list of concept_ids from CMR query
        2. Accepts custom list of concept_ids
    """

    def __init__(self, query=None, input_concept_ids=[], validation_paths=[]):
        self.input_concept_ids = input_concept_ids
        self.query = query
        self.validation_paths = validation_paths

        self.concept_ids = self._cmr_query() if self.query else self.input_concept_ids

        self.errors = []

    def _cmr_query(self):
        # TODO: Make the page_size dynamic and use page_num to advance through multiple pages of results
        response = requests.get(self.query)

        if response.status_code != 200:
            return {"error": "CMR Query failed"}

        response_dict = xmltodict.parse(response.text)

        concept_ids = [
            result["id"]
            for result in response_dict["results"]["references"]["reference"]
        ]

        return concept_ids

    def validate(self):
        if self.query and self.input_concept_ids:
            return {
                "error": "PyCMR received both CMR query and concept_ids. It can only accept one of those."
            }

        if not self.query and not self.input_concept_ids:
            return {
                "error": "PyCMR expects either a CMR query or a list of concept_ids."
            }

        for concept_id in tqdm(self.concept_ids):
            downloader = Downloader(concept_id)
            content = downloader.download()
            # with open("myfile", "w") as myfile:
            #     myfile.write(content)
            validator = Validator(
                downloader.metadata_format, validation_paths=self.validation_paths
            )

            # with open("myfile", "r") as myfile:
            #     content = myfile.read()
            validation_errors = validator.validate(content)

            [{"concept_id": "...", "errors": [], "checked_fields": []}]

            self.errors.append(
                {
                    "concept_id": concept_id,
                    "errors": validation_errors,
                    "checked_fields": self.validation_paths or "all",
                }
            )

        return self.errors


if __name__ == "__main__":
    # parse command line arguments (argparse)
    # --query
    # --concept_ids

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--query", action="store", type=str, help="CMR query URL.")
    group.add_argument(
        "--concept_ids",
        nargs="+",
        action="store",
        type=str,
        help="List of concept IDs.",
    )
    parser.add_argument(
        "--fields_to_validate",
        nargs="+",
        action="store",
        type=str,
        help="List of fields to validate in the schema. By default, it takes all of them. For example, Collection/Temporal/RangeDateTime only validates that field.",
    )
    args = parser.parse_args()

    pycmr = PyCMR(
        query=args.query,
        input_concept_ids=args.concept_ids or [],
        validation_paths=args.fields_to_validate or [],
    )
    results = pycmr.validate()

    pprint(results)

# "https://cmr.earthdata.nasa.gov/search/collections?provider=GES_DISC&project=MERRA&page_size=2000"
# demo video
# normal: list key fields we're checking
# show it's working
# make changes and show changes so it's catching the cahnges
# run for multiple concept ids
# cmr query
# only doing this for echo10 right now
# haven't gone beyond this
# schema is incomplete (but we can show in video)
