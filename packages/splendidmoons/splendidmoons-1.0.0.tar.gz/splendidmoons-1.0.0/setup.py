# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['splendidmoons']

package_data = \
{'': ['*']}

install_requires = \
['typer>=0.9.0,<0.10.0']

entry_points = \
{'console_scripts': ['splendidmoons = splendidmoons.runner:main']}

setup_kwargs = {
    'name': 'splendidmoons',
    'version': '1.0.0',
    'description': 'Calculates uposatha moonday calendar data for Mahanikaya',
    'long_description': '# Splendid Moons\n\n*calculates uposatha moonday calendar data for Mahanikaya*\n\nPython library\n\nGenerates the calendar data for <http://splendidmoons.github.io/>\n\n(This is a Python port and replacement of the older [suriya-go](https://github.com/splendidmoons/suriya-go) GoLang package.)\n\n``` shell\n$ pip install splendidmoons\n$ splendidmoons asalha-puja 2023\n2023-08-01\n$ splendidmoons year-events-csv 2020 2030 moondays.csv\n```\n\n``` python\nfrom splendidmoons.calendar_year import CalendarYear\nfor year in [2023, 2024, 2025]:\n    print(f"{year}: {CalendarYear(year).year_type()}")\n# 2023: YearType.Adhikamasa\n# 2024: YearType.Normal\n# 2025: YearType.Adhikavara\n```\n\n',
    'author': 'Gambhiro',
    'author_email': 'profound.labs@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
