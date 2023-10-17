from base64 import b64decode

from ... import errors
from .. import http
from . import base

import logging  # isort:skip
_log = logging.getLogger(__name__)


class PredbdeApi(base.PredbApiBase):
    name = 'predbde'
    label = 'PreDB.de'

    default_config = {}

    _url_base = b64decode('cHJlZGIuZGU=').decode('ascii')
    _search_url = f'https://{_url_base}/api/'

    async def _search(self, query):
        q = self._get_q(query.keywords, query.group)
        if q:
            return await self._request_all_pages(q)
        else:
            return ()

    def _get_q(self, keywords, group):
        kws = list(keywords)
        if group:
            kws.append(group)
        if kws:
            kws = (str(kw).lower().strip() for kw in kws)
            return ' '.join(kw for kw in kws if kw)
        else:
            return ''

    _max_pages = 1000

    async def _request_all_pages(self, q):
        combined_results = []
        page = 1
        while page < self._max_pages:
            results, next_page = await self._request_page(q, page)
            combined_results.extend(results)

            if next_page < 0:
                # Negative next page means there are no more pages
                break
            else:
                page += 1

        return combined_results

    _max_results_per_page = 20

    async def _request_page(self, q, page):

        params = {
            'q': q,
            'page': page,
        }
        _log.debug('%s search: %r, %r', self.label, self._search_url, params)
        response = (await http.get(self._search_url, params=params, cache=True)).json()

        if response.get('data'):
            # We found at least one release
            results = tuple(result['release'] for result in response['data'])

        elif (
                response.get('status') != 'success'
                and response.get('message')
                and response['message'].lower() != 'no results'
        ):
            # Report error from API
            raise errors.RequestError(f'{self.label}: {response["message"]}')

        else:
            results = ()

        # Is there another page of results?
        if len(results) >= self._max_results_per_page:
            next_page = page + 1
        else:
            next_page = -1

        return results, next_page

    async def _release_files(self, release_name):
        raise NotImplementedError()
