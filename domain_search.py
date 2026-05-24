import fastly
import time
from fastly.api import domain_research_api
from pprint import pprint

FASTLY_API_TOKEN = "FASTLYAPI"

configuration = fastly.Configuration(
    host="https://api.fastly.com"
)
configuration.api_token = FASTLY_API_TOKEN.strip()

free_domains = []

domain_characters = list("abcdefghijklmnopqrstuvwxyz0123456789")


def domain_has_live_service(domain_to_check: str) -> bool:
    """
    Returns True if Fastly says the domain appears to have a live service.
    Returns False if the domain is unavailable / not live.
    Raises authentication errors rather than hiding them.
    """

    with fastly.ApiClient(configuration) as api_client:
        api_instance = domain_research_api.DomainResearchApi(api_client)

        try:
            api_response = api_instance.domain_status(domain_to_check)
            pprint(api_response)

            # Adjust this after seeing the exact response object.
            return True

        except fastly.ApiException as e:
            print(f"\nFastly API error for {domain_to_check}")
            print(e)

            if e.status in [401, 403]:
                raise RuntimeError(
                    "Fastly authentication failed. Token is missing, invalid, expired, "
                    "restricted, or not authorised for Domain Research API."
                ) from e

            return False


for first in domain_characters:
    for second in domain_characters:
        try_domain = f"{first}{second}.com"

        if domain_has_live_service(try_domain) is False:
            free_domains.append(try_domain)

        print(f"\r{try_domain} checked.", end="", flush=True)
        time.sleep(0.05)

print(f"\n\n{len(free_domains)} Domains without live service:")
for domain in free_domains:
    print(domain)