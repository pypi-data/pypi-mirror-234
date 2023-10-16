import setuptools
from setuptools import setup

using_setuptools = True

setup_args = {
    'name': 'basecolors',
    'version': '0.1.2',
    'url': 'https://github.com/ga1008/basecolors',
    'description': '在终端显示基本的文本颜色',
    'long_description': open('README.md', encoding="utf-8").read(),
    'author': 'Guardian',
    'author_email': 'zhling2012@live.com',
    'maintainer': 'Guardian',
    'maintainer_email': 'zhling2012@live.com',
    'long_description_content_type': "text/markdown",
    'LICENSE': 'MIT',
    'packages': setuptools.find_packages(),
    'include_package_data': True,
    'zip_safe': False,
    'entry_points': {
        'console_scripts': [
            'colorit = BaseColor.base_colors:color_it',
        ]
    },

    'classifiers': [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    'install_requires': [
    ],
}

setup(**setup_args)
