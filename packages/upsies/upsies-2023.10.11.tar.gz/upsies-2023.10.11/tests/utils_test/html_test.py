from types import SimpleNamespace

import pytest
from bs4 import BeautifulSoup

from upsies.utils import html


class Soup(BeautifulSoup):
    def __init__(self, html):
        super().__init__(html, features='html.parser')


@pytest.mark.parametrize(
    argnames='string, exp_prettified_html',
    argvalues=(
        ('<html>foo</html>', '<html>\n foo\n</html>'),
        ('<html>foo</html', '<html>\n foo&lt;/html\n</html>'),
        (Soup('<html>foo</html>'), '<html>\n foo\n</html>'),
        (Soup('<html>foo<b>B<i>A</i>R</b></html>').html.b, '<b>\n B\n <i>\n  A\n </i>\n R\n</b>'),
    ),
    ids=lambda v: repr(v),
)
def test_parse(string, exp_prettified_html):
    assert html.parse(string).prettify().strip() == exp_prettified_html.strip()


def test_dump_writes_string(tmp_path):
    html.dump('<html>foo</html>', tmp_path / 'foo.html')
    assert (tmp_path / 'foo.html').read_text().strip() == '<html>\n foo\n</html>'

def test_dump_writes_BeautifulSoup_instance(tmp_path):
    from bs4 import BeautifulSoup
    doc = BeautifulSoup('<html>foo</html>', features='html.parser')
    html.dump(doc, tmp_path / 'foo.html')
    assert (tmp_path / 'foo.html').read_text().strip() == '<html>\n foo\n</html>'


@pytest.mark.parametrize(
    argnames='html_string, exp_text',
    argvalues=(
        ('<html>foo</html>', 'foo'),
        ('\n<html>  f o   o\n\n bar</html>\n\n', 'f o o\nbar'),
        ('<textarea>Check <b>this</b>   out<i>! </i></textarea>\n\n', 'Check this out!'),
        ('<textarea>Multiple\n<br />lines<br>with\n<br/><br>different<br />\n<br />newlines\n</textarea>\n\n',
         'Multiple\nlines\nwith\ndifferent\nnewlines'),
    ),

)
def test_as_text(html_string, exp_text):
    assert html.as_text(html_string) == exp_text


class Soup(SimpleNamespace):
    pass

@pytest.mark.parametrize(
    argnames='doc, attributes, exp_return_value',
    argvalues=(
        # All tags are found
        (
            Soup(table=Soup(tr=Soup(td='hello'))),
            ('table', 'tr', 'td'),
            'hello',
        ),
        (
            Soup(table=Soup(tr=Soup(td='hello'))),
            ('table', 'tr'),
            Soup(td='hello'),
        ),
        (
            Soup(table=Soup(tr=Soup(td='hello'))),
            ('table',),
            Soup(tr=Soup(td='hello')),
        ),
        (
            Soup(table=Soup(tr=Soup(td='hello'))),
            (),
            Soup(table=Soup(tr=Soup(td='hello'))),
        ),
        # Tag is None
        (
            Soup(table=Soup(tr=Soup(td=None))),
            ('table', 'tr', 'td'),
            None,
        ),
        (
            Soup(table=Soup(tr=Soup(td=None))),
            ('table', 'tr', 'td', 'div'),
            None,
        ),
        # Tag is not found
        (
            Soup(table=Soup(tr=Soup(td='hello'))),
            ('table', 'tr', 'TD'),
            None,
        ),
        (
            Soup(table=Soup(tr=Soup(td='hello'))),
            ('table', 'TR', 'td'),
            None,
        ),
        (
            Soup(table=Soup(tr=Soup(td='hello'))),
            ('TABLE', 'tr', 'td'),
            None,
        ),
    ),
    ids=lambda v: repr(v),
)
def test_get(doc, attributes, exp_return_value):
    return_value = html.get(doc, *attributes)
    assert return_value == exp_return_value


def test_purge_javascript():
    string = (
        '<html>\n'
        'a\n'
        '<script>foo</script>\n'
        'b<script with="attribute">bar</script>\n'
        'c\n'
        '<script>\n'
        '    baz\n'
        '</script>\n'
        '</html>\n'
    )
    assert html.purge_javascript(string) == (
        '<html>\n'
        'a\n'
        '\n'
        'b\n'
        'c\n'
        '\n'
        '</html>\n'
    )
