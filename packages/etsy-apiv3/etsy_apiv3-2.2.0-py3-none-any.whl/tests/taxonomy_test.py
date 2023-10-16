from etsy_apiv3.models import Receipt, Transaction
from etsy_apiv3.utils import EtsySession, Response
from etsy_apiv3.resources import ListingResource
from etsy_apiv3.utils.RequestException import EtsyRequestException
import test_credentials

session = EtsySession(test_credentials.CLIENT_KEY, test_credentials.CLIENT_SECRET, test_credentials.TOKEN)

resource = ListingResource(session)

for taxonomy in resource.get_buyer_taxonomy_nodes().results:
    a = resource.get_properties_by_buyer_taxonomy_id(taxonomy.id)
    print(a)