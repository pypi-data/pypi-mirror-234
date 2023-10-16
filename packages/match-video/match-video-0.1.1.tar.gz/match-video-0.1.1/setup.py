# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['match_video']

package_data = \
{'': ['*']}

install_requires = \
['typer[all]>=0.4.0,<0.5.0']

extras_require = \
{'examples': ['streamlit>=1.12.0,<2.0.0',
              'jupyterlab>=3.6.1,<4.0.0',
              'xmltodict>=0.13.0,<0.14.0',
              'numpy==1.23.4',
              'pyarrow==10.0.0'],
 'lint': ['pre-commit>=2.19.0,<3.0.0',
          'black>=22.3.0,<23.0.0',
          'flake8>=4.0.1,<5.0.0',
          'isort>=5.6.4,<6.0.0'],
 'test': ['pytest>=7.1.2,<8.0.0',
          'coverage[toml]>=6.4,<7.0',
          'pytest-cov>=3.0.0,<4.0.0',
          'pytest-mock>=3.2.0,<4.0.0',
          'pytest-sugar>=0.9.4,<0.10.0']}

entry_points = \
{'console_scripts': ['match-video = match_video.cli:app']}

setup_kwargs = {
    'name': 'match-video',
    'version': '0.1.1',
    'description': 'A Python library that simplifies working with video from soccer matches.',
    'long_description': '# Match Video\n\nThis is a Python library that simplifies working with video from soccer matches. It allows match video to be selected intuitively by period number and clock, instead of absolute video time.\n\nTo accomplish this the start of each period is set as a chapter in the match video\'s metadata. Clips from the video can then be selected by period number and clock. ffmpeg handles both reading and writing the video chapter metadata and clip selection.\n\n## Installation\n\n### Requirements\n- Python 3.6 or newer\n- [ffmpeg](https://ffmpeg.org)\n\n```shell\npip install match-video\n```\n\n## Usage\n\nBefore the video can be used, the start time of each half needs to be set.\n\n```shell\nmatch-video set-half-starts path/to/video.mp4 0:04 63:20\n```\n\nThen it is easy to select match video by period and clock!\n\n```python\nimport match_video as mv\n\n# get the third minute of the match\nclip = mv.get_clip("path/to/video.mp4", period=1, start_clock=180, end_clock=240)\n\n# get the start of each half and concatenate them\nclip_clocks = [\n    {"period": 1, "start_clock": 0, "end_clock": 30},\n    {"period": 2, "start_clock": 0, "end_clock": 30},\n]\nclips = mv.get_clips("path/to/video.mp4", clip_clocks)\n```\n\nSee the [examples](https://gitlab.com/grantwenzinger/match-video/-/tree/main/examples) to see how to save or display video clips.\n\n## Support\n\n<grantwenzinger@gmail.com>\n\n## License\n\n[MIT](https://choosealicense.com/licenses/mit/)\n',
    'author': 'Grant Wenzinger',
    'author_email': 'grantwenzinger@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/grantwenzinger/match-video',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9.0,<4.0.0',
}


setup(**setup_kwargs)
