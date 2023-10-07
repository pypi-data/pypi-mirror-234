"""
API for imdb.com
"""

import functools
import re

from ... import utils
from ..types import ReleaseType
from . import common
from .base import WebDbApiBase

import logging  # isort:skip
_log = logging.getLogger(__name__)


class ImdbApi(WebDbApiBase):
    """API for imdb.com"""

    name = 'imdb'
    label = 'IMDb'

    default_config = {}

    _url_base = 'https://www.imdb.com'
    _soup_cache = {}

    async def _get_soup(self, path, params={}):
        path = path.rstrip('/')

        cache_id = (path, tuple(sorted(params.items())))
        if cache_id in self._soup_cache:
            return self._soup_cache[cache_id]

        text = await utils.http.get(
            url=f'{self._url_base}/{path}/',
            params=params,
            user_agent=await utils.http.get_popular_user_agent(),
            cache=True,
        )

        self._soup_cache[cache_id] = utils.html.parse(text)
        return self._soup_cache[cache_id]

    _title_types = {
        ReleaseType.movie: 'feature,tv_movie,documentary,short,video,tv_short',
        ReleaseType.season: 'tv_series,tv_miniseries',
        # Searching for single episodes is currently not supported
        ReleaseType.episode: 'tv_series,tv_miniseries',
    }

    def sanitize_query(self, query):
        """
        Deal with IMDb-specific quirks

        - Remove ``"and"`` from :attr:`.Query.title` because IMDb doesn't find
          ``"Foo & Bar"`` if we search for ``"Foo and Bar"``. It's seems to work
          vice versa, i.e. the query ``"Foo and Bar"`` finds ``"Foo & Bar"``, so
          we keep any ``"&"``.

        - Replace ``"dont"`` with ``"don't"``, ``"cant"`` with ``"can't"``.
        """
        query = super().sanitize_query(query)
        query.title = re.sub(r'\s(?i:and)(\s)', r'\1', query.title)
        query.title = re.sub(r'\b(?i:dont)(\b)', "don't", query.title)
        query.title = re.sub(r'\b(?i:cant)(\b)', "can't", query.title)
        query.title = re.sub(r'\b(?i:wont)(\b)', "won't", query.title)
        return query

    def get_id_from_text(self, text):
        # Example: https://www.imdb.com/title/tt0048918/
        match = re.search(r'\b(tt\d+)\b', text)
        if match:
            return match.group(1)

    async def search(self, query):
        _log.debug('Searching IMDb for %s', query)

        if query.id:
            title_english = await self.title_english(query.id)
            title_original = await self.title_original(query.id)
            return [_ImdbSearchResult(
                imdb_api=self,
                cast=functools.partial(self.cast, query.id),
                countries=functools.partial(self.countries, query.id),
                directors=functools.partial(self.directors, query.id),
                genres=functools.partial(self.genres, query.id),
                id=query.id,
                summary=functools.partial(self.summary, query.id),
                title=title_english or title_original,
                title_english=title_english,
                title_original=title_original,
                type=await self.type(query.id),
                url=await self.url(query.id),
                year=await self.year(query.id),
            )]

        elif not query.title:
            return []

        else:
            path = 'search/title/'
            params = {'title': query.title_normalized if not query.id else query.id}
            if query.type is not ReleaseType.unknown:
                params['title_type'] = self._title_types[query.type]
            if query.year is not None:
                params['release_date'] = f'{query.year}-01-01,{query.year}-12-31'

            def is_search_result(tag):
                if tag.get('class') == ['lister-item-content']:
                    header = tag.find(class_='lister-item-header')
                    if not header or 'Episode:' not in header.strings:
                        return True

            soup = await self._get_soup(path, params=params)
            items = soup.find_all(is_search_result)
            results = [
                _ImdbSearchResult(soup=item, imdb_api=self)
                for item in items
            ]
            return results

    _person_url_path_regex = re.compile(r'(/name/nm\d+)')

    def _get_persons(self, tag):
        a_tags = tag.find_all('a', href=self._person_url_path_regex)
        persons = []
        for a_tag in a_tags:
            if a_tag.string:
                name = a_tag.string.strip()
                url_path = self._person_url_path_regex.match(a_tag["href"]).group(1)
                url = f'{self._url_base.rstrip("/")}/{url_path.lstrip("/")}'
                persons.append(common.Person(name, url))
        return tuple(persons)

    async def cast(self, id):
        cast = []
        if id:
            soup = await self._get_soup(f'title/{id}/')
            # New website
            cast_tag = soup.find(class_='title-cast__grid')
            if cast_tag is None:
                # Old website
                cast_tag = soup.find(class_='cast_list')
            if cast_tag:
                cast.extend(self._get_persons(cast_tag))
        return tuple(cast)

    async def _countries(self, id):
        countries = []
        if id:
            soup = await self._get_soup(f'title/{id}/')
            a_tags = soup.find_all(href=re.compile(r'/search/title.*?country_of_origin='))
            for a_tag in a_tags:
                country = ''.join(a_tag.stripped_strings)
                countries.append(country)
        return tuple(countries)

    _creators_label_regex = re.compile('^Creators?:?$')

    async def creators(self, id):
        if id:
            soup = await self._get_soup(f'title/{id}/')
            # Old website design
            credits_tags = soup.find_all(class_='credit_summary_item')
            if not credits_tags:
                # New website design
                credits_tags = soup.find_all(class_='ipc-metadata-list__item')
            for tag in credits_tags:
                if any(self._creators_label_regex.search(string)
                       for string in tag.stripped_strings):
                    return self._get_persons(tag)
        return ()

    _directors_label_regex = re.compile('^Directors?:?$')

    async def directors(self, id):
        if id:
            soup = await self._get_soup(f'title/{id}/')
            # Old website design
            credits_tags = soup.find_all(class_='credit_summary_item')
            if not credits_tags:
                # New website design
                credits_tags = soup.find_all(class_='ipc-metadata-list__item')
            for tag in credits_tags:
                if any(self._directors_label_regex.search(string)
                       for string in tag.stripped_strings):
                    return self._get_persons(tag)
        return ()

    async def genres(self, id):
        if id:
            soup = await self._get_soup(f'title/{id}/')
            genres = []
            genre_links = soup.find_all('a', href=re.compile(r'/search/title\?.*genres='))
            for genre_link in genre_links:
                match = re.search(r'genres=([^&]+)', genre_link['href'])
                if match:
                    genre = match.group(1).lower()
                    if genre not in genres:
                        genres.append(genre)
            return tuple(genres)
        return ()

    async def poster_url(self, id, season=None):
        if id and await self.type(id) != ReleaseType.episode:  # noqa: E721: do not compare types
            soup = await self._get_soup(f'title/{id}/reference')
            tag = soup.select_one('meta [property="og:image"]')
            if tag:
                url = tag.get('content')
                if url:
                    if '@' in url:
                        # Remove any cropping instructions and other stuff
                        url = re.sub(r'_CR[\d+,]+', r'', url)
                    return url

        return ''

    rating_min = 0.0
    rating_max = 10.0

    async def rating(self, id):
        if id:
            soup = await self._get_soup(f'title/{id}/')

            # Old website design
            rating_tag = soup.find(itemprop='ratingValue')

            if not rating_tag:
                # New website design
                rating_tag = soup.find(attrs={'data-testid': 'hero-rating-bar__aggregate-rating__score'})
                if rating_tag and rating_tag.children:
                    rating_tag = rating_tag.contents[0]

            if rating_tag:
                try:
                    return float(rating_tag.string)
                except (ValueError, TypeError):
                    pass

        return None

    _ignored_runtimes_keys = (
        re.compile(r'^(?i:approx)\w*$'),
    )

    async def _runtimes(self, id):
        if id:
            soup = await self._get_soup(f'title/{id}/technical')
            label_tags = soup.select('.ipc-metadata-list__item > .ipc-metadata-list-item__label')
            for tag in label_tags:
                if 'Runtime' in utils.html.as_text(tag):
                    values_tag = tag.next_sibling
                    if values_tag:
                        return self._parse_runtimes(values_tag)
        return {}

    def _parse_runtimes(self, tag):
        runtimes = {}
        for li_tag in tag.find_all('li'):
            li_text = ' '.join(li_tag.stripped_strings)

            # Examples: 2h 13m (133 min)
            #           2h 28m (148 min) (extended) (United States)
            #           2h 42m (162 min) 3h 6m (186 min) (director's cut) 3h 35m (215 min) (Ultimate Cut)
            #           55m
            match = re.search(r'\((\d+)\s*(?:min|m)\)\s*(?:\((.+?)\)|)', li_text)
            if not match:
                match = re.search(r'^(\d+)\s*(?:min|m)$', li_text)

            if match:
                groups = match.groups()
                minutes = int(groups[0])
                if len(groups) >= 2:
                    key = utils.string.capitalize(groups[1]) if groups[1] else 'default'
                else:
                    key = 'default'

                if not any(regex.search(key) for regex in self._ignored_runtimes_keys):
                    runtimes[key] = minutes

        return runtimes

    async def summary(self, id):
        if id:
            soup = await self._get_soup(f'title/{id}/')

            # Get summary from the top
            candidates = (
                # Old website design
                soup.find(class_='summary_text'),
                # New website design
                soup.find(attrs={'data-testid': 'plot-xl'}),
            )
            for tag in candidates:
                if tag:
                    string = ''.join(tag.stripped_strings).strip()
                    link_texts = ('See full summary»', 'Read all', 'Add a Plot»')
                    if all(not string.endswith(text) for text in link_texts):
                        return string

            # Get summary from dedicated page
            soup = await self._get_soup(f'title/{id}/plotsummary')
            candidates = (
                # Old website design
                utils.html.get(soup.find(id='plot-summaries-content'), 'li', 'p'),
                # New website design
                soup.find(attrs={'data-testid': 'sub-section-summaries'}),
            )
            for tag in candidates:
                if tag:
                    text = utils.html.as_text(tag)
                    return re.sub(r'—.*$', '', text).strip()

        return ''

    async def _title_original(self, id):
        # /title/tt.../releaseinfo/#akas: Find "(original title)" row in table
        # Example: https://www.imdb.com/title/tt1405737/releaseinfo/#akas
        soup = await self._get_soup(f'title/{id}/releaseinfo')
        for tag in soup.select('.ipc-metadata-list__item > .ipc-metadata-list-item__label'):
            text = utils.html.as_text(tag)
            if 'original' in text:
                return utils.html.as_text(tag.next_sibling)

        return ''

    async def _titles_english(self, id):
        soup = await self._get_soup(f'title/{id}/releaseinfo')

        # Get the main (usually English) title from the <head>
        tag = soup.select_one('head meta[property="og:title"]')
        if tag:
            match = re.search(r'^(.*)\s+\(.*?\)\s*', tag['content'])
            if match:
                return [match.group(1).strip()]

        return ['']

    async def type(self, id):
        if id:
            soup = await self._get_soup(f'title/{id}/reference')

            tag = soup.find(class_='ipl-inline-list')
            text = ' '.join(reversed(tuple(tag.stripped_strings))).lower()

            if 'episode' in text:
                return ReleaseType.episode
            elif 'tv series' in text:
                return ReleaseType.season
            elif re.search(r'tv mini[- ]series', text):
                return ReleaseType.season
            elif 'tv movie' in text:
                return ReleaseType.movie
            elif 'movie' in text:
                return ReleaseType.movie
            elif 'short' in text:
                return ReleaseType.movie
            elif 'video' in text:
                return ReleaseType.movie

        return ReleaseType.unknown

    async def url(self, id):
        if id:
            return f'{self._url_base.rstrip("/")}/title/{id}'
        return ''

    async def year(self, id):
        if id:
            soup = await self._get_soup(f'title/{id}/reference')

            tag = soup.find(class_='titlereference-title-year')
            if tag:
                text = ' '.join(reversed(tuple(tag.stripped_strings))).lower()
                match = re.search(r'\b(\d{4})\b', text)
                if match:
                    return match.group(1)

        return ''


class _ImdbSearchResult(common.SearchResult):
    def __init__(self, *, imdb_api, soup=None, cast=None, countries=None,
                 directors=None, id=None, genres=None, summary=None, title=None,
                 title_english=None, title_original=None, type=None, url=None,
                 year=None):
        soup = soup or utils.html.parse('')
        id = id or self._get_id(soup)
        return super().__init__(
            cast=cast or self._get_cast(soup),
            countries=countries or functools.partial(imdb_api.countries, id),
            directors=directors or self._get_directors(soup),
            genres=genres or self._get_genres(soup),
            id=id or self._get_id(soup),
            summary=summary or self._get_summary(soup),
            title=title or self._get_title(soup),
            title_english=title_english or functools.partial(imdb_api.title_english, id),
            title_original=title_original or functools.partial(imdb_api.title_original, id),
            type=type or self._get_type(soup),
            url=url or self._get_url(soup),
            year=year or self._get_year(soup),
        )

    def _get_cast(self, soup):
        people = soup.find(string=re.compile(r'Stars?.*'))
        if people:
            names = tuple(name.string.strip() for name in people.parent.find_all('a'))
            return names[1:]
        else:
            return ()

    def _get_directors(self, soup):
        people = soup.find(string=re.compile(r'Director?.*'))
        if people:
            director = people.parent.find('a')
            if director:
                return (director.string.strip(),)
        else:
            return ()

    def _get_id(self, soup):
        a_tag = soup.find('a')
        if a_tag:
            href = a_tag.get('href')
            return re.sub(r'^.*/([t0-9]+)/.*$', r'\1', href)
        return ''

    def _get_genres(self, soup):
        try:
            genres = soup.find(class_='genre').string.strip()
        except AttributeError:
            genres = ''
        if genres:
            return tuple(g.strip().casefold() for g in genres.split(','))
        else:
            return ()

    def _get_summary(self, soup):
        summary = ''

        tags = soup.find_all(class_='text-muted')
        if len(tags) >= 3:
            strings = tuple(tags[2].strings)
            if strings and 'Add a Plot' not in strings:
                summary = (''.join(strings) or '').strip()

        # Look for "See full summary" link. Preceding text is summary.
        if not summary:
            summary_link = soup.find('a', string=re.compile(r'(?i:full\s+summary)'))
            if summary_link:
                summary_tag = summary_link.parent
                if summary_tag:
                    summary = ''.join(summary_tag.strings)

        summary = re.sub(r'(?i:see full summary).*', '', summary).strip()
        summary = re.sub(r'\s*\.\.\.\s*$', '…', summary)

        return summary

    def _get_title(self, soup):
        a_tag = soup.find('a')
        if a_tag:
            return a_tag.string.strip()
        return ''

    def _get_type(self, soup):
        if soup.find(string=re.compile(r'Directors?:')):
            return ReleaseType.movie
        else:
            return ReleaseType.series

    def _get_url(self, soup):
        id = self._get_id(soup)
        if id:
            return f'{ImdbApi._url_base}/title/{id}'
        return ''

    def _get_year(self, soup):
        try:
            year = soup.find(class_='lister-item-year').string or ''
        except AttributeError:
            return ''
        # Year may be preceded by roman number
        year = re.sub(r'\([IVXLCDM]+\)\s*', '', year)
        # Remove parentheses
        year = year.strip('()')
        # Possible formats:
        # - YYYY
        # - YYYY–YYYY  ("–" is NOT "U+002D / HYPHEN-MINUS" but "U+2013 / EN DASH")
        # - YYYY–
        try:
            return str(int(year[:4]))
        except (ValueError, TypeError):
            return ''
