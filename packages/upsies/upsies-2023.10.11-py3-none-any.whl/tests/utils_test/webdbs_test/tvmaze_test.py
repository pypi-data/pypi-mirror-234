from itertools import zip_longest
from unittest.mock import AsyncMock, call

import pytest

from upsies.utils.types import ReleaseType
from upsies.utils.webdbs import Query, SearchResult, tvmaze


@pytest.fixture
def api():
    return tvmaze.TvmazeApi()


def test_sanitize_query(api):
    q = Query('The Foo', type='movie', year='2000')
    assert api.sanitize_query(q) == Query('The Foo', type='unknown', year='2000')
    with pytest.raises(TypeError, match=r'^Not a Query instance: 123$'):
        api.sanitize_query(123)


@pytest.mark.parametrize(
    argnames='text, exp_id',
    argvalues=(
        ('Some Title', None),
        ('1899', None),
        ('myshows/123', None),
        ('shows/123arf', None),
        ('shows/123', '123'),
        ('https://www.tvmaze.com/shows/123', '123'),
        ('https://www.tvmaze.com/shows/123/', '123'),
        ('https://www.tvmaze.com/shows/123/gary-and-his-demons', '123'),
        ('junk shows/123 more junk', '123'),
        ('junk https://www.tvmaze.com/shows/123/stuff more junk', '123'),
    ),
    ids=lambda value: str(value),
)
def test_get_id_from_text(text, exp_id, api, store_response):
    return_value = api.get_id_from_text(text)
    assert return_value == exp_id


@pytest.mark.asyncio
async def test_search_handles_id_in_query(api, store_response):
    results = await api.search(Query(id=35724))
    assert len(results) == 1
    assert results[0].id == 35724
    assert results[0].title == 'Karppi'
    assert results[0].type == ReleaseType.season
    assert results[0].url == 'https://www.tvmaze.com/shows/35724/karppi'
    assert results[0].year == '2018'

    # Make sure we're not awaiting the same coroutine again on subsequent calls
    for _ in range(2):
        assert (await results[0].cast())[:3] == ('Pihla Viitala', 'Lauri Tilkanen', 'Mimosa Willamo')
        assert (await results[0].countries()) == ('Finland',)
        assert (await results[0].directors()) == ()
        assert (await results[0].genres()) == ('drama', 'crime', 'thriller')
        assert (await results[0].summary()) == ('Just months after a tragic loss, detective '
                                                'Sofia Karppi investigates the murder of a '
                                                'woman with ties to a Helsinki construction company.')
        assert (await results[0].title_english()) == 'Deadwind'
        assert (await results[0].title_original()) == 'Karppi'


@pytest.mark.asyncio
async def test_search_returns_empty_list_if_title_is_empty(api, store_response):
    assert await api.search(Query('', year='2009')) == []

@pytest.mark.asyncio
async def test_search_returns_list_of_SearchResults(api, store_response):
    results = await api.search(Query('Star Wars'))
    for result in results:
        assert isinstance(result, SearchResult)


@pytest.mark.parametrize(
    argnames=('query', 'exp_titles'),
    argvalues=(
        (Query('Star Wars', year=2003), ('Star Wars: Clone Wars',)),
        (Query('Star Wars', year='2003'), ('Star Wars: Clone Wars',)),
        (Query('Star Wars', year=2014), ('Star Wars: Rebels',)),
        (Query('Star Wars', year='1990'), ()),
    ),
    ids=lambda value: str(value),
)
@pytest.mark.asyncio
async def test_search_for_year(query, exp_titles, api, store_response):
    results = await api.search(query)
    titles = {r.title for r in results}
    assert titles == set(exp_titles)


@pytest.mark.parametrize(
    argnames=('query', 'exp_titles'),
    argvalues=(
        (Query('star wars clone', type=ReleaseType.series), ('Star Wars: Clone Wars', 'Star Wars: The Clone Wars')),
        (Query('yes minister', type=ReleaseType.series), ('Yes Minister', 'Yes, Prime Minister', 'Yes, Prime Minister')),
    ),
    ids=lambda value: str(value),
)
@pytest.mark.asyncio
async def test_search_for_series(query, exp_titles, api, store_response):
    results = await api.search(query)
    titles = {r.title for r in results}
    assert titles == set(exp_titles)


@pytest.mark.parametrize(
    argnames=('query', 'exp_titles'),
    argvalues=(
        (Query('star wars', type=ReleaseType.movie), ()),
        (Query('yes minister', type=ReleaseType.movie), ()),
    ),
    ids=lambda value: str(value),
)
@pytest.mark.asyncio
async def test_search_for_movie(query, exp_titles, api, store_response):
    assert await api.search(query) == []


@pytest.mark.parametrize(
    argnames=('title', 'exp_cast'),
    argvalues=(
        ('Star Wars: Clone Wars', ('André Sogliuzzo', 'John DiMaggio')),
        ('Star Wars: Rebels', ('Taylor Gray', 'Vanessa Marshall')),
        ('Star Wars Resistance', ('Christopher Sean', 'Suzie McGrath')),
    ),
    ids=lambda value: str(value),
)
@pytest.mark.asyncio
async def test_search_result_cast(title, exp_cast, api, store_response):
    results = await api.search(Query('Star Wars'))
    results_dict = {r.title: r for r in results}
    cast = await results_dict[title].cast()
    for member in exp_cast:
        assert member in cast


@pytest.mark.parametrize(
    argnames=('title', 'exp_countries'),
    argvalues=(
        ('Star Wars: Clone Wars', ('United States',)),
        ('Something in the Rain', ('South Korea',)),
        ('Le Chalet', ('France',)),
        ('Bron / Broen', ('Sweden',)),
    ),
)
@pytest.mark.asyncio
async def test_search_result_countries(title, exp_countries, api, store_response):
    results = await api.search(Query(title))
    results_dict = {r.title: r for r in results}
    countries = await results_dict[title].countries()
    assert countries == exp_countries


@pytest.mark.parametrize(
    argnames=('title', 'exp_id'),
    argvalues=(
        ('Star Wars: Clone Wars', 1259),
        ('Star Wars: Rebels', 117),
        ('Star Wars Resistance', 36483),
    ),
)
@pytest.mark.asyncio
async def test_search_result_id(title, exp_id, api, store_response):
    results = await api.search(Query('Star Wars'))
    results_dict = {r.title: r for r in results}
    assert results_dict[title].id == exp_id


@pytest.mark.asyncio
async def test_search_result_directors(api, store_response):
    results = await api.search(Query('Star Wars'))
    for result in results:
        directors = await result.directors()
        assert directors == ()


@pytest.mark.parametrize(
    argnames=('title', 'exp_genres'),
    argvalues=(
        ('Star Wars: Clone Wars', ('action', 'science-fiction')),
        ('Something in the Rain', ('drama', 'romance')),
        ('Le Chalet', ('thriller', 'mystery')),
    ),
)
@pytest.mark.asyncio
async def test_search_result_genres(title, exp_genres, api, store_response):
    results = await api.search(Query(title))
    results_dict = {r.title: r for r in results}
    for kw in exp_genres:
        genres = await results_dict[title].genres()
        assert kw in genres


@pytest.mark.parametrize(
    argnames=('title', 'exp_summary'),
    argvalues=(
        ('Star Wars: Clone Wars', 'downfall of the Jedi'),
        ('Star Wars: Rebels', 'set five years before the events of Star Wars: Episode IV'),
        ('Star Wars Resistance', 'Kazuda Xiono'),
    ),
)
@pytest.mark.asyncio
async def test_search_result_summary(title, exp_summary, api, store_response):
    results = await api.search(Query('Star Wars'))
    results_dict = {r.title: r for r in results}
    summary = await results_dict[title].summary()
    assert exp_summary in summary


@pytest.mark.asyncio
async def test_search_result_title_english(api, store_response, mocker):
    mock_title_english = mocker.patch.object(
        api, 'title_english', AsyncMock(return_value='The English Title')
    )
    results = await api.search(Query('Star Wars'))
    for result in results:
        assert await result.title_english() == 'The English Title'
    assert sorted(mock_title_english.call_args_list) == [
        call(result.id) for result in sorted(results, key=lambda r: r.id)
    ]


@pytest.mark.asyncio
async def test_search_result_title_original(api, store_response, mocker):
    mock_title_original = mocker.patch.object(
        api, 'title_original', AsyncMock(return_value='The Original Title')
    )
    results = await api.search(Query('Star Wars'))
    for result in results:
        assert await result.title_original() == 'The Original Title'
    assert sorted(mock_title_original.call_args_list) == [
        call(result.id) for result in sorted(results, key=lambda r: r.id)
    ]


@pytest.mark.parametrize(
    argnames=('id', 'exp_title'),
    argvalues=(
        (1259, 'Star Wars: Clone Wars'),
        (117, 'Star Wars: Rebels'),
        (36483, 'Star Wars Resistance'),
    ),
)
@pytest.mark.asyncio
async def test_search_result_title(id, exp_title, api, store_response):
    results = await api.search(Query('Star Wars'))
    results_dict = {r.id: r for r in results}
    assert results_dict[id].title == exp_title


@pytest.mark.asyncio
async def test_search_result_type(api, store_response):
    results = await api.search(Query('Star Wars'))
    for result in results:
        assert result.type is ReleaseType.series


@pytest.mark.parametrize(
    argnames=('title', 'exp_url'),
    argvalues=(
        ('Star Wars: Clone Wars', 'https://www.tvmaze.com/shows/1259/star-wars-clone-wars'),
        ('Star Wars: Rebels', 'https://www.tvmaze.com/shows/117/star-wars-rebels'),
        ('Star Wars Resistance', 'https://www.tvmaze.com/shows/36483/star-wars-resistance'),
    ),
)
@pytest.mark.asyncio
async def test_search_result_url(title, exp_url, api, store_response):
    results = await api.search(Query('Star Wars'))
    results_dict = {r.title: r for r in results}
    assert results_dict[title].url == exp_url


@pytest.mark.parametrize(
    argnames=('title', 'exp_year'),
    argvalues=(
        ('Star Wars: Clone Wars', '2003'),
        ('Star Wars: Rebels', '2014'),
        ('Star Wars Resistance', '2018'),
    ),
)
@pytest.mark.asyncio
async def test_search_result_year(title, exp_year, api, store_response):
    results = await api.search(Query('Star Wars'))
    results_dict = {r.title: r for r in results}
    assert results_dict[title].year == exp_year


@pytest.mark.parametrize(
    argnames=('id', 'exp_cast'),
    argvalues=(
        # Star Wars: Clonse Wars
        (1259, (('André Sogliuzzo', 'https://www.tvmaze.com/people/53172/andre-sogliuzzo'),
                ('Anthony Daniels', 'https://www.tvmaze.com/people/49258/anthony-daniels'))),
        # Karppi / Deadwind
        (35724, (('Pihla Viitala', 'https://www.tvmaze.com/people/100790/pihla-viitala'),
                 ('Lauri Tilkanen', 'https://www.tvmaze.com/people/214175/lauri-tilkanen'))),
        # La Foret
        (32614, (('Samuel Labarthe', 'https://www.tvmaze.com/people/83285/samuel-labarthe'),
                 ('Suzanne Clément', 'https://www.tvmaze.com/people/190609/suzanne-clement'))),
        # Terror in the Woods
        (32430, ()),
        # Bron / Broen
        (1910, (('Sofia Helin', 'https://www.tvmaze.com/people/60479/sofia-helin'),
                ('Kim Bodnia', 'https://www.tvmaze.com/people/60480/kim-bodnia'))),
        (None, ()),
    ),
    ids=lambda value: str(value),
)
@pytest.mark.asyncio
async def test_cast(id, exp_cast, api, store_response):
    cast = (await api.cast(id))[:2]
    if not exp_cast:
        assert cast == ()
    else:
        for person, (name, url) in zip_longest(cast, exp_cast):
            assert str(person) == name
            assert person.url == url

@pytest.mark.asyncio
async def test_cast_deduplicates_actors_with_multiple_roles(api, store_response):
    cast = await api.cast(83)  # The Simpsons
    assert cast.count('Dan Castellaneta') == 1
    assert cast.count('Julie Kavner') == 1
    assert cast.count('Yeardley Smith') == 1
    assert cast.count('Nancy Cartwright') == 1
    assert cast.count('Harry Shearer') == 1


@pytest.mark.parametrize(
    argnames=('id', 'exp_countries'),
    argvalues=(
        # Star Wars: Clonse Wars
        (1259, ('United States',)),
        # Karppi / Deadwind
        (35724, ('Finland',)),
        # La Foret
        (32614, ('France',)),
        # Terror in the Woods
        (32430, ('United States',)),
        # Bron / Broen
        (1910, ('Sweden',)),
        (None, ()),
    ),
)
@pytest.mark.asyncio
async def test_countries(id, exp_countries, api, store_response):
    countries = await api.countries(id)
    assert countries == exp_countries


@pytest.mark.parametrize(
    argnames=('id', 'exp_creators'),
    argvalues=(
        # Star Wars: Clonse Wars
        # TODO: George Luce is wrong. Maybe it'll get fixed.
        # (1259, (('Genndy Tartakovsky', 'https://www.tvmaze.com/people/56151/genndy-tartakovsky'),)),
        (1259, (('George Lucas', 'https://www.tvmaze.com/people/49259/george-lucas'),)),
        # Karppi / Deadwind
        (35724, (('Rike Jokela', 'https://www.tvmaze.com/people/214183/rike-jokela'),
                 ('Kirsi Porkka', 'https://www.tvmaze.com/people/214184/kirsi-porkka'),
                 ('Jari Olavi Rantala', 'https://www.tvmaze.com/people/214185/jari-olavi-rantala'))),
        # La Foret
        (32614, (('Delinda Jacobs', 'https://www.tvmaze.com/people/79543/delinda-jacobs'),)),
        # Terror in the Woods
        (32430, ()),
        # Bron / Broen
        (1910, (('Hans Rosenfeldt', 'https://www.tvmaze.com/people/76345/hans-rosenfeldt'),
                ('Camilla Ahlgren', 'https://www.tvmaze.com/people/120427/camilla-ahlgren'))),
        (None, ()),
    ),
    ids=lambda value: str(value),
)
@pytest.mark.asyncio
async def test_creators(id, exp_creators, api, store_response):
    creators = await api.creators(id)
    if not exp_creators:
        assert creators == ()
    else:
        for person, (name, url) in zip_longest(creators, exp_creators):
            assert str(person) == name
            assert person.url == url


@pytest.mark.parametrize(
    argnames=('id', 'exp_directors'),
    argvalues=(
        # Star Wars: Clonse Wars
        (1259, ()),
        # Karppi / Deadwind
        (35724, ()),
        # La Foret
        (32614, ()),
        # Terror in the Woods
        (32430, ()),
        # Bron / Broen
        (1910, ()),
        (None, ()),
    ),
    ids=lambda value: str(value),
)
@pytest.mark.asyncio
async def test_directors(id, exp_directors, api, store_response):
    directors = await api.directors(id)
    assert directors == exp_directors


@pytest.mark.parametrize(
    argnames=('id', 'exp_genres'),
    argvalues=(
        # Star Wars: Clonse Wars
        (1259, ('action', 'family', 'science-fiction')),
        # Karppi / Deadwind
        (35724, ('drama', 'crime', 'thriller')),
        # La Foret
        (32614, ('drama', 'crime')),
        # Terror in the Woods
        (32430, ('mystery', 'supernatural')),
        # Bron / Broen
        (1910, ('drama', 'crime', 'thriller')),
        (None, ()),
    ),
)
@pytest.mark.asyncio
async def test_genres(id, exp_genres, api, store_response):
    genres = await api.genres(id)
    assert genres == exp_genres


@pytest.mark.parametrize(
    argnames='id, season, exp_url',
    argvalues=(
        # Star Wars: Clonse Wars
        (1259, None, 'https://static.tvmaze.com/uploads/images/original_untouched/393/983792.jpg'),
        (1259, 1, 'https://static.tvmaze.com/uploads/images/original_untouched/393/983796.jpg'),
        (1259, 2, 'https://static.tvmaze.com/uploads/images/original_untouched/393/983792.jpg'),
        # Karppi / Deadwind
        (35724, None, 'https://static.tvmaze.com/uploads/images/original_untouched/151/377808.jpg'),
        (35724, 1, 'https://static.tvmaze.com/uploads/images/original_untouched/151/377808.jpg'),
        (35724, 2, 'https://static.tvmaze.com/uploads/images/original_untouched/151/377808.jpg'),
        # La Foret
        (32614, None, 'https://static.tvmaze.com/uploads/images/original_untouched/130/327264.jpg'),
        (32614, 1, 'https://static.tvmaze.com/uploads/images/original_untouched/130/327264.jpg'),
        # Terror in the Woods
        (32430, None, 'https://static.tvmaze.com/uploads/images/original_untouched/356/891645.jpg'),
        (32430, 1, 'https://static.tvmaze.com/uploads/images/original_untouched/240/601573.jpg'),
        (32430, 2, 'https://static.tvmaze.com/uploads/images/original_untouched/356/891645.jpg'),
        # Bron / Broen
        (1910, None, 'https://static.tvmaze.com/uploads/images/original_untouched/11/27700.jpg'),
        (1910, 1, 'https://static.tvmaze.com/uploads/images/original_untouched/252/631183.jpg'),
        (1910, 2, 'https://static.tvmaze.com/uploads/images/original_untouched/252/631184.jpg'),
        (None, None, ''),
    ),
)
@pytest.mark.asyncio
async def test_poster_url(id, season, exp_url, api, store_response):
    poster_url = await api.poster_url(id, season=season)
    assert poster_url == exp_url


@pytest.mark.parametrize(
    argnames=('id', 'exp_rating'),
    argvalues=(
        # Star Wars: Clonse Wars
        (1259, 8.2),
        # Karppi / Deadwind
        (35724, 6.4),
        # La Foret
        (32614, 6.4),
        # Terror in the Woods
        (32430, 7.7),
        # Bron / Broen
        (1910, 8.5),
        (None, None),
    ),
)
@pytest.mark.asyncio
async def test_rating(id, exp_rating, api, store_response):
    rating = await api.rating(id)
    assert rating == exp_rating


@pytest.mark.parametrize(
    argnames=('id', 'exp_runtimes'),
    argvalues=(
        # Star Wars: Clonse Wars
        (1259, {'default': 15}),
        # Karppi / Deadwind
        (35724, {'default': 45}),
        # La Foret
        (32614, {'default': 60}),
        # Terror in the Woods
        (32430, {'default': 60}),
        # Bron / Broen
        (1910, {'default': 60}),
        (None, {}),
    ),
)
@pytest.mark.asyncio
async def test_runtimes(id, exp_runtimes, api, store_response):
    runtimes = await api.runtimes(id)
    assert runtimes == exp_runtimes


@pytest.mark.parametrize(
    argnames=('id', 'exp_summary'),
    argvalues=(
        # Star Wars: Clone Wars
        (1259, ('The Clone Wars television series chronicles the events taking place '
                'between Star Wars Episode II: Attack of the Clones and '
                'Star Wars Episode III: Revenge of the Sith. The Clone Wars will ultimately lead '
                'to the downfall of the Jedi and the rise of the Galactic Empire.')),
        # Karppi
        (35724, ('Just months after a tragic loss, detective Sofia Karppi investigates '
                 'the murder of a woman with ties to a Helsinki construction company.')),
        # Le Foret
        (32614, ('A sixteen-year-old girl has been reported missing from her village '
                 'in the Ardennes. With the help of a lonely and mysterious woman, '
                 'Capt. Gaspard Decker and local cop Virginie Musso are tasked to locate her.')),
        # Terror in the Woods
        (32430, ("The great outdoors aren't always so great. In fact, the woods are filled "
                 "with mysteries that sometimes cannot be explained. These are the true accounts "
                 "of people who ventured deep into the forest only to come screaming out with "
                 "stories that defy reality.")),
        # Bron / Broen
        (1910, ('When a body is found on the bridge between Denmark and Sweden, '
                'right on the border, Danish inspector Martin Rohde and Swedish Saga Norén '
                'have to share jurisdiction and work together to find the killer.')),
        (None, ''),
    ),
)
@pytest.mark.asyncio
async def test_summary(id, exp_summary, api, store_response):
    assert await api.summary(id) == exp_summary


@pytest.mark.parametrize(
    argnames=('id', 'exp_title_english', 'exp_title_original'),
    argvalues=(
        (1259, '', 'Star Wars: Clone Wars'),
        (35724, 'Deadwind', 'Karppi'),
        (32614, 'The Forest', 'La Forêt'),
        (32430, 'Terror in the Woods', 'These Woods Are Haunted'),
        (1910, 'The Bridge', 'Bron/Broen'),
        (None, '', ''),
    ),
)
@pytest.mark.asyncio
async def test_title_english_original(id, exp_title_english, exp_title_original, api, store_response):
    assert await api.title_original(id) == exp_title_original
    assert await api.title_english(id) == exp_title_english
    assert await api.title_english(id, default_to_original=False) == exp_title_english
    if exp_title_english:
        assert await api.title_english(id, default_to_original=True) == exp_title_english
    else:
        assert await api.title_english(id, default_to_original=True) == exp_title_original


@pytest.mark.parametrize('id', (1259, 35256, 36072, None))
@pytest.mark.asyncio
async def test_type(id, api, store_response):
    await api.type(id) == ReleaseType.unknown  # noqa: E721: do not compare types


@pytest.mark.parametrize(
    argnames=('id', 'exp_url'),
    argvalues=(
        (1259, 'https://www.tvmaze.com/shows/1259/star-wars-clone-wars'),
        (35724, 'https://www.tvmaze.com/shows/35724/karppi'),
        (32614, 'https://www.tvmaze.com/shows/32614/la-foret'),
        (32430, 'https://www.tvmaze.com/shows/32430/these-woods-are-haunted'),
        (None, ''),
    ),
)
@pytest.mark.asyncio
async def test_url(id, exp_url, api, store_response):
    assert await api.url(id) == exp_url


@pytest.mark.parametrize(
    argnames=('id', 'exp_year'),
    argvalues=(
        # Star Wars: Clonse Wars
        (1259, '2003'),
        # Karppi / Deadwind
        (35724, '2018'),
        # La Foret
        (32614, '2017'),
        # Terror in the Woods
        (32430, '2017'),
        # Bron / Broen
        (1910, '2011'),
        (None, ''),
    ),
)
@pytest.mark.asyncio
async def test_year(id, exp_year, api, store_response):
    assert await api.year(id) == exp_year


@pytest.mark.parametrize(
    argnames=('id', 'exp_imdb_id'),
    argvalues=(
        # Star Wars: Clonse Wars
        (1259, 'tt0361243'),
        # Karppi / Deadwind
        (35724, 'tt6616260'),
        # La Foret
        (32614, 'tt6560040'),
        # Terror in the Woods
        (32430, 'tt7534328'),
        # Bron / Broen
        (1910, 'tt1733785'),
        (None, ''),
    ),
)
@pytest.mark.asyncio
async def test_imdb_id(id, exp_imdb_id, api, store_response):
    assert await api.imdb_id(id) == exp_imdb_id


@pytest.mark.parametrize(
    argnames=('id', 'season', 'episode', 'exp_episode'),
    argvalues=(
        # Star Wars: Clonse Wars
        (1259, 1, 5, {
            'date': '2003-11-13',
            'episode': '5',
            'season': '1',
            'summary': ('On Mon Calamari, Kit Fisto and his Scuba Troopers defends the '
                        'Calamari council against Manta Droid sub fighters army of the '
                        'Quarren Isolation league. Mon Calamari Knights riding giant '
                        "Keelkana's provide the Republic forces with back up."),
            'title': 'Chapter V',
            'url': 'https://www.tvmaze.com/episodes/109474/star-wars-clone-wars-1x05-chapter-v',
        }),

        # Karppi / Deadwind
        (35724, 3, 4, {
            'date': '2021-10-29',
            'episode': '4',
            'season': '3',
            'summary': ('Laura is the target of an assassination attempt and the '
                        'management of the pharmaceutical company is entangled in a '
                        'tangle. Karppi and Nurmi find their way to the hideout used by '
                        'the murderer and at the same time access the traces of the symbol '
                        'seen in connection with the bodies. The dual role takes Henna '
                        'deeper into the underworld.'),
            'title': 'Kos',
            'url': 'https://www.tvmaze.com/episodes/2204669/karppi-3x04-kos',
        }),

        # La Foret
        (32614, 1, 2, {
            'date': '2017-05-30',
            'episode': '2',
            'season': '1',
            'summary': ('Capt. Decker questions Maya, stoking tensions at the station. A '
                        'grim discovery in the woods and two more disappearances put the '
                        'town on edge.'),
            'title': 'Épisode 2',
            'url': 'https://www.tvmaze.com/episodes/1329360/la-foret-1x02-episode-2',
        }),

        (None, 1, 3, {
            'date': '',
            'episode': '',
            'season': '',
            'summary': '',
            'title': '',
            'url': '',
        }),
    ),
)
@pytest.mark.asyncio
async def test_episode(id, season, episode, exp_episode, api, store_response):
    assert await api.episode(id, season, episode) == exp_episode


@pytest.mark.parametrize(
    argnames=('id', 'exp_status'),
    argvalues=(
        # Star Wars: Clonse Wars
        (1259, 'Ended'),
        # Karppi / Deadwind
        (35724, 'Ended'),
        # La Foret
        (32614, 'Ended'),
        # Terror in the Woods
        (32430, 'Running'),
        # Bron / Broen
        (1910, 'Ended'),
        (None, ''),
    ),
)
@pytest.mark.asyncio
async def test_status(id, exp_status, api, store_response):
    assert await api.status(id) == exp_status
