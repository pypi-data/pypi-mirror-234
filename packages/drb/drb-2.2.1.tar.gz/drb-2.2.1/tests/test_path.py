# import os
import unittest
import pathlib

from drb.exceptions.core import DrbException
from drb.core.path import parse_path, ParsedPath


class TestPath(unittest.TestCase):
    def test_parse_path_from_url_string(self):
        uris = [
            {
                'url': 'file:///my/path/to/my_file/',
                'type': ParsedPath,
                'path': "/my/path/to/my_file/",
                'path_without_scheme': "/my/path/to/my_file/",
                'scheme': 'file',
                'archive': None,
                'is_local': True,
                'is_remote': False
            },
            {
                'url': '/my/path/to/my_file/',
                'type': ParsedPath,
                'path': "/my/path/to/my_file/",
                'path_without_scheme': "/my/path/to/my_file/",
                'scheme': '',
                'archive': None,
                'is_local': True,
                'is_remote': False
            },
            {
                'url': 'http://avp.wikia.com/wiki/ht_file',
                'type': ParsedPath,
                'path': "/wiki/ht_file",
                'path_without_scheme': "avp.wikia.com/wiki/ht_file",
                'scheme': 'http',
                'archive': None,
                'is_local': False,
                'is_remote': True
            },
            {
                'url': 'http://avp.wikia.com/wiki/ht_file?q=*',
                'type': ParsedPath,
                'path': "/wiki/ht_file",
                'path_without_scheme': "avp.wikia.com/wiki/ht_file?q=*",
                'scheme': 'http',
                'archive': None,
                'is_local': False,
                'is_remote': True
            },
            {
                'url': 'ftp://ftp.fe.fr/ms/fp.cs.org/7.2.15/ft_file',
                'type': ParsedPath,
                'path': "/ms/fp.cs.org/7.2.15/ft_file",
                'path_without_scheme': "ftp.fe.fr/ms/fp.cs.org/7.2.15/ft_file",
                'scheme': 'ftp',
                'archive': None,
                'is_local': False,
                'is_remote': True
            },
            {
                'url': 'mailto:billg@microsoft.com',
                'type': ParsedPath,
                'path': "billg@microsoft.com",
                'path_without_scheme': "billg@microsoft.com",
                'scheme': 'mailto',
                'archive': None,
                'is_local': True,
                'is_remote': False
            }]

        for uri in uris:
            url = uri['url']
            path_name = uri['path']

            parsed_path = parse_path(url)
            self.assertIsInstance(parsed_path, ParsedPath)
            url_path = parsed_path.path
            self.assertEqual(url_path, path_name,
                             msg=f"Wrong path for URI={url}")
            self.assertEqual(parsed_path.name, url,
                             msg=f"Wrong name for URI={url}")
            if isinstance(parsed_path, ParsedPath):
                self.assertEqual(parsed_path.uri_with_netloc(),
                                 uri['path_without_scheme'],
                                 msg=f"Wrong uri_without_scheme for URI={url}")
                self.assertEqual(parsed_path.scheme, uri['scheme'],
                                 msg=f"Wrong scheme for URI={url}")
                self.assertEqual(parsed_path.archive, uri['archive'],
                                 msg=f"Wrong archive for URI={url}")
                self.assertEqual(parsed_path.is_local, uri['is_local'],
                                 msg=f"Wrong archive for URI={url}")
                self.assertEqual(parsed_path.is_remote, uri['is_remote'],
                                 msg=f"Wrong archive for URI={url}")

    def test_parse_path_from_vfs_string(self):
        vfss = [
            {
                'url': 'file+zip:///my/path/to/my_file/file.zip',
                'type': ParsedPath,
                'path': "/my/path/to/my_file/file.zip",
                'path_with_netloc': "/my/path/to/my_file/file.zip",
                'scheme': 'file+zip',
                'archive': None,
                'is_local': True
            },
            {
                'url': 'zip+https://avp.wikia.com/wiki/ht_file/file.zip',
                'type': ParsedPath,
                'path': "/wiki/ht_file/file.zip",
                'path_with_netloc': "avp.wikia.com/wiki/ht_file/file.zip",
                'scheme': 'zip+https',
                'archive': None,
                'is_local': False
            },
            {
                'url': 'https+zip://avp.wikia.com/wiki/ht_file/file.zip',
                'type': ParsedPath,
                'path': "/wiki/ht_file/file.zip",
                'path_with_netloc': "avp.wikia.com/wiki/ht_file/file.zip",
                'scheme': 'https+zip',
                'archive': None,
                'is_local': True
            },
            {
                'url': 'zip+https://avp.wikia.com/wiki/ht_file/file.zip!'
                       '/content/of/zip',
                'type': ParsedPath,
                'path': "/wiki/ht_file/file.zip!/content/of/zip",
                'path_with_netloc':
                    "avp.wikia.com/wiki/ht_file/file.zip!/content/of/zip",
                'scheme': 'zip+https',
                'archive': '/wiki/ht_file/file.zip',
                'is_local': False
            },
        ]

        for uri in vfss:
            url = uri['url']
            path_name = uri['path']
            path_with_netloc = uri['path_with_netloc']

            path = parse_path(url)
            self.assertIsInstance(path, uri['type'])
            if isinstance(path, ParsedPath):
                self.assertEqual(path.name, url,
                                 msg=f"Wrong name for URI={url}")
                self.assertEqual(path.path, path_name,
                                 msg=f"Wrong path for URI={url}")
                self.assertEqual(path.uri_with_netloc(), path_with_netloc,
                                 msg=f"Wrong uri_without_scheme for URI={url}")
                self.assertEqual(path.scheme, uri['scheme'],
                                 msg=f"Wrong scheme for URI={url}")
                self.assertEqual(path.archive, uri['archive'],
                                 msg=f"Wrong archive for URI={url}")
                self.assertEqual(path.is_local, uri['is_local'],
                                 msg=f"Wrong archive for URI={url}")
            elif isinstance(path, ParsedPath):
                self.assertEqual(path.name, url,
                                 msg=f"Wrong name for URI={url}")
                self.assertEqual(path.path, path_name,
                                 msg=f"Wrong path for URI={url}")
            else:
                self.fail(f"Wrong type {type(path).__name__}")

    def test_parse_path_from_path(self):
        my_path = ParsedPath(path='/path/value',
                             archive='www.gael.fr/archive/path.zip',
                             scheme='http')
        parsed_path = parse_path(my_path)
        self.assertEqual(my_path, parsed_path)

    def test_parse_path_from_pathlib(self):
        path = pathlib.Path.cwd()
        parsed_path = parse_path(path)
        self.assertEqual(parsed_path.name, path.as_posix())

    def test_path_filename(self):
        _pathes = [
            {
                'path': '/path/to/filename',
                'filename': 'filename'
            },
            {
                'path': '/path/to/filename/',
                'filename': ''
            },
            {
                'path': 'file:/path/to/filename',
                'filename': 'filename'
            },
            {
                'path': 's3+zip:/path/to/filename',
                'filename': 'filename'
            },
            {
                'path': 'https:/path/to/filename?query=*&row=5',
                'filename': 'filename'
            },
            {
                'path': 'https:/path/to/filename/?query=*&row=5',
                'filename': ''
            },
            {
                'path': 'https:/path/to/data.zip!/filename?query=*&row=5',
                'filename': 'filename'
            },
        ]
        for p in _pathes:
            pp = parse_path(p['path'])
            self.assertEqual(pp.filename, p['filename'])

    def test_path_child_str(self):
        pp = parse_path('file+zip:///my/path/to/my_file/file.zip')
        son = pp / 'root_node'

        self.assertEqual(pp.filename, 'file.zip')

        self.assertEqual(son.filename, 'root_node')
        self.assertEqual(son.path, '/my/path/to/my_file/file.zip/root_node')
        self.assertEqual(son.scheme, 'file+zip')
        self.assertEqual(son.uri_with_netloc(),
                         '/my/path/to/my_file/file.zip/root_node')
        self.assertEqual(son.name,
                         'file+zip:///my/path/to/my_file/file.zip/root_node')

    def test_path_child_empty(self):
        pp = parse_path('file+zip:///my/path/to/my_file/file.zip')
        son = pp / ''

        self.assertEqual(pp.filename, 'file.zip')

        self.assertEqual(son.filename, 'file.zip')
        self.assertEqual(son.path, '/my/path/to/my_file/file.zip')
        self.assertEqual(son.scheme, 'file+zip')
        self.assertEqual(son.uri_with_netloc(),
                         '/my/path/to/my_file/file.zip')
        self.assertEqual(son.name,
                         'file+zip:///my/path/to/my_file/file.zip')

    def test_path_child_sep(self):
        pp = parse_path('file+zip:///my/path/to/my_file/file.zip')
        son = pp / '/'

        self.assertEqual(pp.filename, 'file.zip')

        self.assertEqual(son.filename, '')
        self.assertEqual(son.path, '/my/path/to/my_file/file.zip/')
        self.assertEqual(son.scheme, 'file+zip')
        self.assertEqual(son.uri_with_netloc(),
                         '/my/path/to/my_file/file.zip/')
        self.assertEqual(son.name,
                         'file+zip:///my/path/to/my_file/file.zip/')

    def test_path_child_test_double_sep(self):
        pp = parse_path('file+zip:///my/path/to/my_file/file.zip')

        son = pp / '/root_node'

        self.assertEqual(pp.filename, 'file.zip')

        self.assertEqual(son.filename, 'root_node')
        self.assertEqual(son.path, '/my/path/to/my_file/file.zip/root_node')
        self.assertEqual(son.scheme, 'file+zip')
        self.assertEqual(son.uri_with_netloc(),
                         '/my/path/to/my_file/file.zip/root_node')
        self.assertEqual(son.name,
                         'file+zip:///my/path/to/my_file/file.zip/root_node')

    def test_path_child_test_tipple_sep(self):
        pp = parse_path('file+zip:///my/path/to/my_file/file.zip/')

        son = pp / '/root_node'

        self.assertEqual(pp.filename, '')

        self.assertEqual(son.filename, 'root_node')
        self.assertEqual(son.path, '/my/path/to/my_file/file.zip/root_node')
        self.assertEqual(son.scheme, 'file+zip')
        self.assertEqual(son.uri_with_netloc(),
                         '/my/path/to/my_file/file.zip/root_node')
        self.assertEqual(son.name,
                         'file+zip:///my/path/to/my_file/file.zip/root_node')

    def test_path_child_str_with_scheme(self):
        pp = parse_path('file+zip:///my/path/to/my_file/file.zip/')

        son = pp / 'tar:///root_node.tar'

        self.assertEqual(pp.filename, '')

        self.assertEqual(son.filename, 'root_node.tar')
        self.assertEqual(son.path, '/my/path/to/my_file/file.zip/'
                                   'root_node.tar')
        self.assertEqual(son.scheme, 'file+zip+tar')
        self.assertEqual(son.uri_with_netloc(),
                         '/my/path/to/my_file/file.zip/root_node.tar')
        self.assertEqual(son.name,
                         'file+zip+tar:///my/path/to/my_file/file.zip/'
                         'root_node.tar')

    def test_path_child_str_with_scheme_and_netloc(self):
        pp = parse_path('file+zip://localhost/my/path/to/my_file/file.zip/')

        son = pp / 'tar://other_host/root_node.tar'

        self.assertEqual(pp.filename, '')
        self.assertEqual(son.netloc, 'localhost')

        self.assertEqual(son.filename, 'root_node.tar')
        self.assertEqual(son.path, '/my/path/to/my_file/file.zip/'
                                   'root_node.tar')
        self.assertEqual(son.scheme, 'file+zip+tar')
        self.assertEqual(son.uri_with_netloc(),
                         'localhost/my/path/to/my_file/file.zip/root_node.tar')
        self.assertEqual(son.name,
                         'file+zip+tar://localhost/my/path/to/my_file/'
                         'file.zip/root_node.tar')

    def test_path_child_parsed_path(self):
        pp = parse_path('file+zip:///my/path/to/my_file/file.zip')

        son = parse_path('tar:root_node.tar')
        son = pp / son
        self.assertEqual(pp.filename, 'file.zip')

        self.assertEqual(son.filename, 'root_node.tar')
        self.assertEqual(son.path, '/my/path/to/my_file/file.zip/'
                                   'root_node.tar')
        self.assertEqual(son.scheme, 'file+zip+tar')
        self.assertEqual(son.uri_with_netloc(),
                         '/my/path/to/my_file/file.zip/root_node.tar')
        self.assertEqual(son.name,
                         'file+zip+tar:///my/path/to/my_file/file.zip/'
                         'root_node.tar')

    def test_path_child_with_query(self):

        pp = parse_path('file+zip:///my/path/to/my_file/file.zip?nodes=test')
        son = parse_path('IMG_DATA/BANDS?band=2')
        son = pp / son
        self.assertEqual(pp.filename, 'file.zip')

        self.assertEqual(son.filename, 'BANDS')
        self.assertEqual(son.path,
                         '/my/path/to/my_file/file.zip/IMG_DATA/BANDS')
        self.assertEqual(son.scheme, 'file+zip')
        self.assertEqual(son.uri_with_netloc(),
                         '/my/path/to/my_file/file.zip/IMG_DATA/BANDS?band=2')
        self.assertEqual(son.name,
                         'file+zip:///my/path/to/my_file/file.zip/IMG_DATA/'
                         'BANDS?band=2')

        pp = parse_path('file+zip:///my/path/to/my_file/file.zip?nodes=test')
        son = parse_path('IMG_DATA/BANDS')
        son = pp / son
        self.assertEqual(pp.filename, 'file.zip')

        self.assertEqual(son.filename, 'BANDS')
        self.assertEqual(son.path,
                         '/my/path/to/my_file/file.zip/IMG_DATA/BANDS')
        self.assertEqual(son.scheme, 'file+zip')
        self.assertEqual(son.uri_with_netloc(),
                         '/my/path/to/my_file/file.zip/IMG_DATA/BANDS')
        self.assertEqual(son.name,
                         'file+zip:///my/path/to/my_file/file.zip'
                         '/IMG_DATA/BANDS')

        with self.assertRaises(DrbException):
            pp / 1

    def test_path_child_duplicate_scheme(self):
        pp = parse_path('file+zip:///my/path/to/my_file/file.zip')

        son = parse_path('zip:root_node.zip')

        son = pp / son

        self.assertEqual(son.filename, 'root_node.zip')
        self.assertEqual(son.path, '/my/path/to/my_file/file.zip/'
                                   'root_node.zip')
        self.assertEqual(son.scheme, 'file+zip')
        self.assertEqual(son.uri_with_netloc(),
                         '/my/path/to/my_file/file.zip/root_node.zip')
        self.assertEqual(son.name,
                         'file+zip:///my/path/to/my_file/file.zip/'
                         'root_node.zip')

    def test_repr(self):
        path = ParsedPath('path/to/my_file')
        self.assertEqual('path/to/my_file', str(path))
