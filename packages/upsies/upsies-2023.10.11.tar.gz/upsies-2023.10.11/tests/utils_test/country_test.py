import pytest

from upsies import utils


@pytest.mark.parametrize(
    argnames='country, exp_name',
    argvalues=(
        ('Peoples Republic of China', 'China'),
        ('tAiWaN', 'Taiwan'),
        ('asdf', 'asdf'),
        (('iceland', 'tv', 'GhA', 'Britain', 'asdf'), ('Iceland', 'Tuvalu', 'Ghana', 'United Kingdom', 'asdf')),
    ),
    ids=lambda v: repr(v),
)
def test_country_name(country, exp_name):
    name = utils.country.name(country)
    assert name == exp_name


@pytest.mark.parametrize(
    argnames='country, exp_code',
    argvalues=(
        ('Britain', 'GB'),
        ('United States', 'US'),
        ('Republic of InDoNeSiA', 'ID'),
        (('iceland', 'tv', 'GhA', 'britain', 'asdf'), ('IS', 'TV', 'GH', 'GB', 'asdf')),
    ),
    ids=lambda v: repr(v),
)
def test_country_code_2letter(country, exp_code):
    code = utils.country.iso2(country)
    assert code == exp_code


@pytest.mark.parametrize(
    argnames='country, exp_tld',
    argvalues=(
        ('United Kingdom', 'uk'),
        ('asdf', 'asdf'),
        (('iceland', 'tv', 'GhA', 'britain', 'asdf'), ('is', 'tv', 'gh', 'uk', 'asdf')),
    ),
    ids=lambda v: repr(v),
)
def test_country_tld(country, exp_tld):
    tld = utils.country.tld(country)
    assert tld == exp_tld
