#!/usr/bin/env python3
"""Convert markdown files to HTML.

Note:
    RSS dates (pubDate, lastBuildDate) must conform to RFC 822:
        dd mm yy hh:mm:ss zzz
"""
import argparse
from datetime import datetime, timezone
from html.parser import HTMLParser
from importlib.metadata import version
import io
import os
import shutil

from mako.template import Template
from mako.lookup import TemplateLookup
import markdown
import yaml

parser = argparse.ArgumentParser(prog='thera', usage='%(prog)s [options]')
parser.add_argument('files', nargs='*', help='markdown file(s)')
parser.add_argument('-b', '--blog', help='blog index template path')
parser.add_argument('-c', '--config', help='config file path')
parser.add_argument('-r', '--rss', help='rss template path')
parser.add_argument(
    '-s', '--static', default=[], nargs='*',
    help='static directory paths')
parser.add_argument('-t', '--template', help='template path')
parser.add_argument(
    '-v', '--version', action='version',
    version='Thera version ' + version('thera'))

cfg = {
    'BUILD_DIR': 'build',
    'DISPLAY_DATE_FORMAT': '%d %b %Y',
    'SOURCE_DATE_FORMAT': '%Y-%m-%d %H:%M %z',
    'RSS_ARTICLE_COUNT': 50,
    'RSS_DATE_FORMAT': '%a %d %b %Y %H:%M %Z',
}


class TitleParser(HTMLParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = None
        self.capture = False

    def handle_data(self, data):
        if self.capture:
            self.title = data

    def handle_starttag(self, tag, attrs):
        if tag == 'h1':
            self.capture = True

    def handle_endtag(self, tag):
        if tag == 'h1':
            self.capture = False


class Converter:
    def __init__(self, args=None):
        self.args = parser.parse_args()
        self.config = cfg
        self.mdconverter = markdown.Markdown(
            extensions=[
                'footnotes',
                'meta',
                'smarty',
                'tables',
                'toc'],
            output_format='html5')

    def build(self):
        self.read_config()
        self.build_dir = os.path.join(
            os.getcwd(), self.config.get('BUILD_DIR'))
        os.makedirs(self.build_dir, exist_ok=True)

        # Copy static assets to build directory
        for dir in self.args.static:
            dest = os.path.join(self.build_dir, dir)
            print(f'{dir} -> {dest}')
            shutil.rmtree(dest, ignore_errors=True)
            shutil.copytree(dir, dest)

        articles = [self.create_page(path) for path in self.args.files]
        if self.args.blog:
            datefmt = self.config['SOURCE_DATE_FORMAT']
            # Sort articles newest first.
            articles.sort(
                key=lambda r: datetime.strptime(r['date'], datefmt), reverse=True)
            self.create_blog_index(articles, self.args.blog)
        if self.args.rss:
            self.create_RSS_feed(articles, self.args.rss)

    def convert(self, mdpath, temppath=''):
        """Convert markdown file to HTML.

        Parameters:
            mdpath (s): path to markdown file.
            temppath (s): path to template file.

        Returns:
            data (dict), html (s): html with template.
        """
        with io.open(mdpath, 'r', encoding='ISO-8859-1') as f:
            md = f.read()
        content = self.mdconverter.reset().convert(md)
        metadata = self.mdconverter.Meta
        data = self.normalize(metadata)
        data['title'] = self.create_title(data, content)
        data['slug'] = self.create_slug(data, mdpath)
        data['path'] = os.path.join(self.build_dir, os.path.dirname(mdpath))

        if data.get('date'):
            rss_date_format = self.config.get('RSS_DATE_FORMAT')
            if rss_date_format:
                data['utc-date'] = self.convert_utc(
                    data['date'],
                    self.config.get('SOURCE_DATE_FORMAT'),
                    rss_date_format)
            data['display-date'] = self.convert_utc(
                data['date'],
                self.config.get('SOURCE_DATE_FORMAT'),
                self.config['DISPLAY_DATE_FORMAT'])

        data['content'] = content
        if temppath:
            lookup = TemplateLookup(directories=[os.getcwd()])
            temp = Template(filename=temppath, lookup=lookup)
            html = temp.render(data=data)
        else:
            html = content
        return data, html

    def convert_datetime(self, datestring, fin, fout):
        """Convert datetime string from old format to new format.

        Parameters:
            datestring (s): date time string.
            fin (s): input date string format.
            fout (s): output date string format.
        """
        return datetime.strptime(
            datestring, fin).strftime(fout)

    def convert_utc(self, datestring, fin, fout):
        """Convert datetime string to UTC.

        Parameters:
            datestring (s): date time string.
            fin (s): input date string format.
            fout (s): output date string format.

        Note:
            The input format string must use %z for offset (-0400) instead
            of %Z for abbreviation (EDT). The output format string can
            use either. Per Python datetime docs: "Changed in version 3.2:
            When the %z directive is provided to the strptime() method,
            an aware datetime object will be produced."
        """
        din = datetime.strptime(datestring, fin)
        utc = din.astimezone(timezone.utc)
        return utc.strftime(fout)

    def create_blog_index(self, articles, temppath):
        """Create blog index page.

        Parameters:
            articles (list): presorted newest to oldest.
            temppath (s): path to template file.

        Data format:
            data[year] = [list of articles]
        """
        print('Creating blog index page')
        datefmt = self.config['SOURCE_DATE_FORMAT']
        data = {}
        blog_path = articles[0].get('path')
        for article in articles:
            year = datetime.strptime(article['date'], datefmt).year
            if year in data:
                data[year].append(article)
            else:
                data[year] = [article]
        lookup = TemplateLookup(directories=[os.getcwd()])
        temp = Template(filename=temppath, lookup=lookup)
        html = temp.render(data=data)
        dest = os.path.join(blog_path, 'index.html')
        print(f'Creating {dest}')
        self.write(dest, html)

    def create_page(self, path):
        """Create HTML file.

        Parameters:
            path (s): markdown file path.

        Returns:
            Page data in dictionary.
        """
        print(f'Converting {path}')
        data, html = self.convert(path, self.args.template)
        os.makedirs(data['path'], exist_ok=True)
        dest = os.path.join(data['path'], data['slug'] + '.html')
        print(f'Creating {dest}')
        self.write(dest, html)
        return data

    def create_RSS_feed(self, articles, temppath):
        """Create blog RSS feed page.

        Parameters:
            articles (list): presorted newest to oldest.
            temppath (s): path to template file.
        """
        print('Creating RSS feed')
        articles = articles[:self.config.get('RSS_ARTICLE_COUNT')]
        blog_path = articles[0].get('path')
        os.makedirs(blog_path, exist_ok=True)
        lookup = TemplateLookup(directories=[os.getcwd()])
        temp = Template(filename=temppath, lookup=lookup)
        xml = temp.render(now=self.now(), articles=articles)
        dest = os.path.join(blog_path, 'rss.xml')
        print(f'Creating {dest}')
        self.write(dest, xml)

    def now(self):
        """Return now timestamp in UTC."""
        fmt = self.config['RSS_DATE_FORMAT']
        return datetime.now(timezone.utc).strftime(fmt)

    def create_slug(self, metadata, filename):
        """Return metadata slug or file name."""
        slug = metadata.get('slug', '')
        if slug:
            return slug
        name, ext = os.path.splitext(os.path.basename(filename))
        return name

    def create_title(self, metadata, html):
        """Return metadata title or h1."""
        title = metadata.get('title', '')
        if title:
            return title
        parser = TitleParser()
        parser.feed(html)
        return parser.title

    def normalize(self, d):
        """Return a copy of dict d, but without lists.

        The Python markdown meta extension creates a dictionary of
        lists.
        """
        return {key: d[key][0] for key in d}

    def read_config(self):
        if self.args.config:
            with open(self.args.config, 'r') as f:
                d = yaml.safe_load(f)
            self.config.update(d)

    def write(self, path, s):
        """Write string s to file if the file string changed."""
        olds = None
        if os.path.exists(path):
            with io.open(path, 'r', encoding='ISO-8859-1') as f:
                olds = f.read()
        if s != olds:
            with io.open(path, 'w', encoding='ISO-8859-1') as f:
                f.write(s)


def main():
    converter = Converter()
    converter.build()


if __name__ == "__main__":
    main()

