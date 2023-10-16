# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tvpy']

package_data = \
{'': ['*']}

install_requires = \
['1337x>=1.2.3,<2.0.0',
 'Pillow>=9.2.0,<10.0.0',
 'cssselect>=1.2.0,<2.0.0',
 'fire>=0.4.0,<0.5.0',
 'humanize>=4.4.0,<5.0.0',
 'libtorrent>=2.0.7,<3.0.0',
 'lxml>=4.9.1,<5.0.0',
 'parse-torrent-title>=2.4,<3.0',
 'pyright>=1.1.273,<2.0.0',
 'rich>=12.5.1,<13.0.0',
 'simple-term-menu>=1.5.2,<2.0.0',
 'toml>=0.10.2,<0.11.0',
 'tqdm>=4.64.0,<5.0.0']

entry_points = \
{'console_scripts': ['tv-clean = tvpy.main:tv_clean',
                     'tv-download = tvpy.main:tv_download',
                     'tv-follow = tvpy.main:tv_follow',
                     'tv-info = tvpy.main:tv_info',
                     'tv-rename = tvpy.main:tv_rename',
                     'tv-subs = tvpy.main:tv_subs',
                     'tv-tmdb = tvpy.main:tv_tmdb',
                     'tvpy = tvpy.main:tvpy']}

setup_kwargs = {
    'name': 'tvpy',
    'version': '0.0.46',
    'description': '📺 TvPy',
    'long_description': '# 📺📺 TvPy 🥧🥧\n\nManage TV shows from the terminal.\n\n![demo](https://github.com/gkutiel/tvpy/raw/1a6686c863a74e1c8dd66b4f9087de2f8a349c61/demo.gif)\n\n## Installation\n```shell\n> pip install tvpy\n```\n\n## Usage\n```shell\n> mkdir The.Peripheral \n> tvpy The.Peripheral \n```\n\n## Other commands\nDownload information from TMDB:\n```shell\n> mkdir The.Peripheral \n> tv-json The.Peripheral\n```\n\nDisplay information about a tv show:\n```shell\n> mkdir The.Peripheral \n> tv-info The.Peripheral\n```\n\nDownload a tv show:\n```shell\n> mkdir The.Peripheral \n> tv-download The.Peripheral\n```\n\nDownload subtitles for a tv show:\n```shell\n> mkdir The.Peripheral \n> tv-subs The.Peripheral\n```\n\nRename files to match the pattern `<title>.S<season>E<episode>.<ext>`\n```shell\n> mkdir The.Peripheral \n> tv-rename The.Peripheral\n```\n\n| ⚠️ Danger |\n|----------|\nRemove unused files\n```shell\n> mkdir The.Peripheral \n> tv-clean The.Peripheral\n```\n\n## Configuration\nA small `.tvpy.toml` configuration file is located at your home directory.\nIts content looks like that:\n```toml\nlang = "English"\nfollow = []\n```\n`lang` determines the subtitle language.\n`follow` is a list of TV shows you are watching.',
    'author': 'Gilad Kutiel',
    'author_email': 'gilad.kutiel@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/gkutiel/tvpy/tree/master',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
