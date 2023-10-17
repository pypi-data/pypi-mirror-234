import io
import json
import os.path
import tempfile
import unittest

from thera import thera


# Override ConfigParser so we don't need a config file.
config = {
    'SOURCE_DATE_FORMAT': '%d %b %Y %I:%M %p %z',
    'DISPLAY_DATE_FORMAT': '%d %b %Y',
    'RSS_DATE_FORMAT': '%a, %d %b %Y %H:%M %Z',
    'RSS_ARTICLE_COUNT': 10,
    'RSS_FEED_TEMPLATE': 'templates/rss.xml',
    'BLOG_TEMPLATE': 'templates/blog.html',
    'BLOG_ARCHIVE_TEMPLATE': 'templates/archive.html'}


class TestTitle(unittest.TestCase):
    def setUp(self):
        self.converter = thera.Converter()
        self.dir = tempfile.TemporaryDirectory()
        self.converter.build_dir = os.path.join(self.dir.name, 'dist')

    def test_h1_title(self):
        md = '#Hello world'
        mdpath = os.path.join(self.dir.name, 'test.md')
        with io.open(mdpath, 'w', encoding='ISO-8859-1') as f:
            f.write(md)
        data, html = self.converter.convert(mdpath)
        self.assertEqual(data['title'], 'Hello world')

    def test_metadata_title(self):
        md = '---\nTitle: Hello world\n---\n# Goodbye'
        mdpath = os.path.join(self.dir.name, 'test.md')
        with io.open(mdpath, 'w', encoding='ISO-8859-1') as f:
            f.write(md)
        data, html = self.converter.convert(mdpath)
        self.assertEqual(data['title'], 'Hello world')

    def tearDown(self):
        self.dir.cleanup()


class TestConvert(unittest.TestCase):
    def setUp(self):
        self.converter = thera.Converter()
        self.converter.config = config
        self.dir = tempfile.TemporaryDirectory()
        self.converter.build_dir = os.path.join(self.dir.name, 'dist')

    def test_without_template(self):
        md = '''#Hello world'''
        mdpath = os.path.join(self.dir.name, 'test.md')
        with io.open(mdpath, 'w', encoding='ISO-8859-1') as f:
            f.write(md)
        data, content = self.converter.convert(mdpath)
        html = '<h1 id="hello-world">Hello world</h1>'
        self.assertEqual(content, html)
        self.assertEqual(data['title'], 'Hello world')

    def test_with_template(self):
        md = '''#Hello world'''
        mdpath = os.path.join(self.dir.name, 'test.md')
        with io.open(mdpath, 'w', encoding='ISO-8859-1') as f:
            f.write(md)
        template = '''
            <html>
            ${data["content"]}
            </html>
            '''
        temppath = os.path.join(self.dir.name, 'test.html')
        with io.open(temppath, 'w', encoding='ISO-8859-1') as f:
            f.write(template)
        data, content = self.converter.convert(mdpath, temppath)
        html = '''
            <html>
            <h1 id="hello-world">Hello world</h1>
            </html>
            '''
        self.assertEqual(content, html)
        self.assertEqual(data['title'], 'Hello world')

    def test_metadata(self):
        md = '---\nTitle: Hello world\nDate: 09 Apr 2018 07:00 AM -0400\nSlug: hello\nSummary: A new blog.\n---\n# Goodbye'
        mdpath = os.path.join(self.dir.name, 'test.md')
        with io.open(mdpath, 'w', encoding='ISO-8859-1') as f:
            f.write(md)
        template = '<html>\n${data["content"]}\n</html>'
        temppath = os.path.join(self.dir.name, 'test.html')
        with io.open(temppath, 'w', encoding='ISO-8859-1') as f:
            f.write(template)
        data, content = self.converter.convert(mdpath, temppath)
        html = '<html>\n<h1 id="goodbye">Goodbye</h1>\n</html>'
        self.assertEqual(content, html)
        self.assertEqual(data['title'], 'Hello world')
        self.assertEqual(data['slug'], 'hello')
        self.assertEqual(data['summary'], 'A new blog.')

    def tearDown(self):
        self.dir.cleanup()


class TestTimeStamp(unittest.TestCase):
    def setUp(self):
        self.converter = thera.Converter()
        self.converter.config = config

    def test_now(self):
        t = self.converter.now()
        self.assertTrue(t.endswith(' UTC'))

    def test_convert_format(self):
        s = '2018-07-01 08:30'
        old_format = '%Y-%m-%d %H:%M'
        new_format = '%a, %d %b %Y %H:%M'
        t = self.converter.convert_datetime(s, old_format, new_format)
        self.assertEqual(t, 'Sun, 01 Jul 2018 08:30')

    def test_utc(self):
        s = '2018-07-01 08:30 -0400'
        old_format = '%Y-%m-%d %H:%M %z'
        new_format = '%a, %d %b %Y %H:%M %Z'
        t = self.converter.convert_utc(s, old_format, new_format)
        self.assertEqual(t, 'Sun, 01 Jul 2018 12:30 UTC')


class TestSlug(unittest.TestCase):
    def setUp(self):
        self.converter = thera.Converter()
        self.dir = tempfile.TemporaryDirectory()
        self.converter.build_dir = os.path.join(self.dir.name, 'dist')

    def test_use_metadata(self):
        md = '---\nSlug: hello\n---\n# My title'
        mdpath = os.path.join(self.dir.name, 'test.md')
        with io.open(mdpath, 'w', encoding='ISO-8859-1') as f:
            f.write(md)
        data, content = self.converter.convert(mdpath)
        self.assertEqual(data['slug'], 'hello')

    def test_use_filename(self):
        md = '# My title'
        mdpath = os.path.join(self.dir.name, 'howdy.md')
        with io.open(mdpath, 'w', encoding='ISO-8859-1') as f:
            f.write(md)
        data, content = self.converter.convert(mdpath)
        self.assertEqual(data['slug'], 'howdy')

    def tearDown(self):
        self.dir.cleanup()


class TestConfig(unittest.TestCase):
    def setUp(self):
        class MockArgs:
            pass
        self.converter = thera.Converter()
        self.converter.args = MockArgs()
        self.dir = tempfile.TemporaryDirectory()

    def test_config(self):
        d = dict(RSS_ARTICLE_COUNT=42)
        cfg_path = os.path.join(self.dir.name, 'test.js')
        with io.open(cfg_path, 'w', encoding='ISO-8859-1') as f:
            json.dump(d, f)
        self.converter.args.config = cfg_path
        self.converter.read_config()
        self.assertEqual(self.converter.config['RSS_ARTICLE_COUNT'], 42)

    def tearDown(self):
        self.dir.cleanup()


if __name__ == '__main__':
    unittest.main()

