from setuptools import setup

version = '0.7.dev0'

long_description = '\n\n'.join([
    open('README.rst').read(),
    open('TODO.txt').read(),
    open('CREDITS.txt').read(),
    open('CHANGES.txt').read(),
    ])

install_requires = [
    'Django >= 1.4, < 1.7',
    'lizard-map',
    'sorl-thumbnail',
    'lizard-ui',
    'django-nose',
    'tweetstream',
    'twitter',
    ],

tests_require = [
    ]

setup(name='lizard-sticky-twitterized',
      version=version,
      description="A Twitter enabled version of the sticky app.",
      long_description=long_description,
      # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=['Programming Language :: Python',
                   'Framework :: Django',
                   ],
      keywords=[],
      author='Gijs Nijholt',
      author_email='gijs.nijholt@nelen-schuurmans.nl',
      url='',
      license='GPL',
      packages=['lizard_sticky_twitterized'],
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      tests_require=tests_require,
      extras_require = {'test': tests_require},
      entry_points={
          'console_scripts': [
          ],
          'lizard_map.adapter_class': [
            'adapter_sticky_twitterized = lizard_sticky_twitterized.layers:AdapterStickyTwitterized',
          ],
          },

      )
