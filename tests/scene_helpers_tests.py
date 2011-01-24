import unittest

import sys, os.path
sys.path.append(os.path.abspath('..'))

from sickbeard import sceneHelpers, common

class Show:
    def __init__(self, name, tvdbid, tvrname):
        self.name = name
        self.tvdbid = tvdbid
        self.tvrname = tvrname

class SceneTests(unittest.TestCase):
    
    def _test_sceneToNormalShowNames(self, name, expected):
        result = sceneHelpers.sceneToNormalShowNames(name)
        self.assertTrue(len(set(expected).intersection(set(result))) == len(expected))

        dot_result = sceneHelpers.sceneToNormalShowNames(name.replace(' ','.'))
        dot_expected = [x.replace(' ','.') for x in expected]
        self.assertTrue(len(set(dot_expected).intersection(set(dot_result))) == len(dot_expected))
        
    def _test_allPossibleShowNames(self, name, tvdbid=0, tvrname=None, expected=[]):
        
        result = sceneHelpers.allPossibleShowNames(Show(name, tvdbid, tvrname))
        self.assertTrue(len(set(expected).intersection(set(result))) == len(expected))

    def _test_filterBadReleases(self, name, lang, expected):
        result = sceneHelpers.filterBadReleases(name, lang)
        self.assertEqual(result, expected)

    def _test_isGoodName(self, name, show):
        self.assertTrue(sceneHelpers.isGoodResult(name, show))

    def test_isGoodName(self):
        self._test_isGoodName('Show.Name.S01E02.Test-Test', Show('Show/Name', 0, ''))
        self._test_isGoodName('Show.Name.S01E02.Test-Test', Show('Show. Name', 0, ''))
        self._test_isGoodName('Show.Name.S01E02.Test-Test', Show('Show- Name', 0, ''))
        self._test_isGoodName('Show.Name.Part.IV.Test-Test', Show('Show Name', 0, ''))
        self._test_isGoodName('Show.Name.1x02.Test-Test', Show('Show Name', 0, ''))
        self._test_isGoodName('Show.Name.S01.Test-Test', Show('Show Name', 0, ''))
        self._test_isGoodName('Show.Name.E02.Test-Test', Show('Show: Name', 0, ''))
        self._test_isGoodName('Show Name Season 2 Test', Show('Show: Name', 0, ''))

    def test_sceneToNormalShowNames(self):
        self._test_sceneToNormalShowNames('Show Name 2010', ['Show Name 2010', 'Show Name (2010)'])
        self._test_sceneToNormalShowNames('Show Name US', ['Show Name US', 'Show Name (US)'])
        self._test_sceneToNormalShowNames('Show Name AU', ['Show Name AU', 'Show Name (AU)'])
        self._test_sceneToNormalShowNames('Show Name CA', ['Show Name CA', 'Show Name (CA)'])
        self._test_sceneToNormalShowNames('Show and Name', ['Show and Name', 'Show & Name'])
        self._test_sceneToNormalShowNames('Show and Name 2010', ['Show and Name 2010', 'Show & Name 2010', 'Show and Name (2010)', 'Show & Name (2010)'])
        self._test_sceneToNormalShowNames('show name us', ['show name us', 'show name (us)'])
        self._test_sceneToNormalShowNames('Show And Name', ['Show And Name', 'Show & Name'])
        
        # failure cases
        self._test_sceneToNormalShowNames('Show Name 90210', ['Show Name 90210'])
        self._test_sceneToNormalShowNames('Show Name YA', ['Show Name YA'])

    def test_allPossibleShowNames(self):
        common.sceneExceptions[-1] = ['Exception Test']
        common.countryList['Full Country Name'] = 'FCN'
        
        self._test_allPossibleShowNames('Show Name', expected=['Show Name'])
        self._test_allPossibleShowNames('Show Name', -1, expected=['Show Name', 'Exception Test'])
        self._test_allPossibleShowNames('Show Name', tvrname='TVRage Name', expected=['Show Name', 'TVRage Name'])
        self._test_allPossibleShowNames('Show Name FCN', expected=['Show Name FCN', 'Show Name (Full Country Name)'])
        self._test_allPossibleShowNames('Show Name (FCN)', expected=['Show Name (FCN)', 'Show Name (Full Country Name)'])
        self._test_allPossibleShowNames('Show Name Full Country Name', expected=['Show Name Full Country Name', 'Show Name (FCN)'])
        self._test_allPossibleShowNames('Show Name (Full Country Name)', expected=['Show Name (Full Country Name)', 'Show Name (FCN)'])
        self._test_allPossibleShowNames('Show Name (FCN)', -1, 'TVRage Name', expected=['Show Name (FCN)', 'Show Name (Full Country Name)', 'Exception Test', 'TVRage Name'])

    def test_filterBadReleases(self):
        
        self._test_filterBadReleases('Show.S02.German.Stuff-Grp','en', False)
        self._test_filterBadReleases('Show.S02.French.Stuff-Grp','en', False)
        self._test_filterBadReleases('Show.S02.Some.German.Stuff-Grp','en', False)
        self._test_filterBadReleases('German.Show.S02.Some.Stuff-Grp','en', True)
        self._test_filterBadReleases('French.Show.S02.Some.Stuff-Grp','en', True)
        self._test_filterBadReleases('Show.S02.This.Is.German','en', False)

        self._test_filterBadReleases('Show.S02.German.Stuff-Grp','de', True)
        self._test_filterBadReleases('French.Show.S02.Some.Stuff-Grp','de', False)
        self._test_filterBadReleases('German.Show.S02.Some.Stuff-Grp','de', False)
        self._test_filterBadReleases('Show.S02.This.Is.German','de', True)
        self._test_filterBadReleases('Show.S02.This.Is.French','de', False)

        self._test_filterBadReleases('Show.S02.French.Stuff-Grp','fr', True)
        self._test_filterBadReleases('Show.S02.Some.German.Stuff-Grp','fr', False)
        self._test_filterBadReleases('Show.S02.Some.French.Stuff-Grp','fr', True)
        self._test_filterBadReleases('Show.S02.This.Is.French','fr', True)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        suite = unittest.TestLoader().loadTestsFromName('scene_helpers_tests.SceneTests.test_'+sys.argv[1])
    else:
        suite = unittest.TestLoader().loadTestsFromTestCase(SceneTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
