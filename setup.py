from setuptools import setup

setup(
   name='sc2spreadsheet',
   version='0.1',
   license="MIT",
   description="""Small Python package that decodes 
                    starcraft 2 replays using s2protocol, logs relevant 
                    information(mmr, matchup etc. ) to the google spreadsheet
                    and lastly renames them to something alot more informative.""",
   author='Krzosa Karol',
   author_email='https://github.com/krzosa/sc2spreadsheet',
   url="http://www.foopackage.com/",
   packages=['sc2spreadsheet'], 
   install_requires=['s2protocol', 'gspread', 'oauth2client'],
)