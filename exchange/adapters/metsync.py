import urllib2
import base64
import os
import json
from decimal import Decimal
from django.conf import settings
from exchange.adapters import BaseAdapter


class MetsyncAdapter(BaseAdapter):
    """
    This Adapter uses Metglobals' internal data api to get rates from base
    systems.
    """

    def _request(self, endpoint):
        user = getattr(settings, 'METSYNC_USERNAME', False)
        password = getattr(settings, 'METSYNC_PASSWORD', False)
        url = getattr(settings, 'METSYNC_BASE_URL', False)
        if not (user and password and url):
            raise Exception("Missing configuration")
        url = os.path.join(url, endpoint)

        request = urllib2.Request(url)
        base64auth = base64.b64encode('%s:%s' % (user, password))
        request.add_header("Authorization", "Basic %s" % base64auth)
        result = urllib2.urlopen(request)
        data = json.loads(result.read())
        return data

    def get_currencies(self):
        data = self._request('Currencies/getCurrencyRates')
        result = []
        for k in data:
            result.append((k, k))
        return result

    def get_exchangerates(self, base):
        data = self._request('Currencies/getCurrencyRates')
        result = []
        for k in data:
            result.append((k, Decimal(str(data[k]))))
        return result
