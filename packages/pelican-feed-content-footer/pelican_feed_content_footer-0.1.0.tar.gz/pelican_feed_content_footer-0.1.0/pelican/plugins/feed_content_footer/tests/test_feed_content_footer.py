from pathlib import Path
from xml.etree.ElementTree import ElementTree

import pytest

import pelican


@pytest.fixture
def settings_file():
    return str(Path(__file__).parent / 'pelicanconf.py')


def test_atom(tmp_path: Path, settings_file):
    pelican.main(
        [
            'pelican',
            '-s',
            settings_file,
            '-o',
            str(tmp_path),
            '-e',
            'FEED_CONTENT_FOOTER="Test footer"',
            'FEED_ALL_ATOM="feeds/all.atom.xml"',
        ]
    )
    document = ElementTree(file=tmp_path / 'feeds' / 'all.atom.xml')
    contents = document.findall(
        './atom:entry/atom:content', {'atom': 'http://www.w3.org/2005/Atom'}
    )
    assert contents
    for content in contents:
        assert content.text.endswith('<footer>Test footer</footer>')


def test_atom_no_footer(tmp_path: Path, settings_file):
    pelican.main(
        [
            'pelican',
            '-s',
            settings_file,
            '-o',
            str(tmp_path),
            '-e',
            'FEED_CONTENT_FOOTER=null',
            'FEED_ALL_ATOM="feeds/all.atom.xml"',
        ],
    )
    document = ElementTree(file=tmp_path / 'feeds' / 'all.atom.xml')
    contents = document.findall(
        './atom:entry/atom:content', {'atom': 'http://www.w3.org/2005/Atom'}
    )
    assert contents
    for content in contents:
        assert '<footer>' not in content.text


def test_rss(tmp_path: Path, settings_file):
    pelican.main(
        [
            'pelican',
            '-D',
            '-s',
            settings_file,
            '-o',
            str(tmp_path),
            '-e',
            'FEED_CONTENT_FOOTER="Test footer"',
            'FEED_ALL_RSS="feeds/all.rss.xml"',
            'RSS_FEED_SUMMARY_ONLY=false',
        ],
    )
    document = ElementTree(file=tmp_path / 'feeds' / 'all.rss.xml')
    descriptions = document.findall('./channel/item/description')
    assert descriptions
    for description in descriptions:
        assert description.text.endswith('<footer>Test footer</footer>')


def test_rss_summary_only(tmp_path: Path, settings_file):
    pelican.main(
        [
            'pelican',
            '-D',
            '-s',
            settings_file,
            '-o',
            str(tmp_path),
            '-e',
            'FEED_CONTENT_FOOTER="Test footer"',
            'FEED_ALL_RSS="feeds/all.rss.xml"',
            'RSS_FEED_SUMMARY_ONLY=true',
        ],
    )
    document = ElementTree(file=tmp_path / 'feeds' / 'all.rss.xml')
    descriptions = document.findall('./channel/item/description')
    assert descriptions
    for description in descriptions:
        assert '<footer>' not in description.text
