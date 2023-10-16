import logging

from feedgenerator import Atom1Feed, Rss201rev2Feed

from pelican import signals

log = logging.getLogger(__name__)

FEED_CONTENT_FOOTER = 'FEED_CONTENT_FOOTER'


def add_feed_content_footer(context, feed):
    feed_content_footer = context.get(FEED_CONTENT_FOOTER)
    if not feed_content_footer:
        return

    match feed:
        case Atom1Feed():
            for item in feed.items:
                item['content'] += f'\n<footer>{feed_content_footer}</footer>'
        case Rss201rev2Feed():
            if not context.get('RSS_FEED_SUMMARY_ONLY', True):
                for item in feed.items:
                    item['description'] += f'\n<footer>{feed_content_footer}</footer>'
        case _:
            log.warning('Unsupported feed object %s.', feed)


def register():
    signals.feed_generated.connect(add_feed_content_footer)
