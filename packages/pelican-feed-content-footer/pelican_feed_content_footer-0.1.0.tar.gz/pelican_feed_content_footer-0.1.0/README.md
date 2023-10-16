# Feed Content Footer: A Plugin for Pelican

Pelican plugin that adds a footer to RSS/Atom feed items content.

## Installation

This plugin can be installed via:

    python -m pip install pelican-feed-content-footer

As long as you have not explicitly added a `PLUGINS` setting to your Pelican settings file, then the newly-installed plugin should be automatically detected and enabled. Otherwise, you must add `feed_content_footer` to your existing `PLUGINS` list. For more information, please see the [How to Use Plugins](https://docs.getpelican.com/en/latest/plugins.html#how-to-use-plugins) documentation.

## Usage

Add the following to your settings file:

## `FEED_CONTENT_FOOTER`

A string that will be appended to the content of every entry in your Atom feed and, if `RSS_FEED_SUMMARY_ONLY` is `False`, to the description of every item in your RSS feed inside a HTML footer tag.

## License

This project is licensed under the AGPL-3.0 license.
