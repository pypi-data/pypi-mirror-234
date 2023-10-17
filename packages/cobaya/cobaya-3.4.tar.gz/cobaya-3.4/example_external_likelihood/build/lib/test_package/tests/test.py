import unittest


class LikeTest(unittest.TestCase):

    def test_cobaya(self):
        from cobaya.yaml import yaml_load
        from cobaya.model import get_model
        last_bib = None
        for name in ['test_package.TestLike',
                     'test_package.test_like.TestLike',
                     'test_package.sub_module.test_like2.TestLike2',
                     'test_package.sub_module.test_like2']:
            info_yaml = r"""
            likelihood:
              %s:
            params:
              H0: 72
            """ % name
            info = yaml_load(info_yaml)
            model = get_model(info)
            self.assertAlmostEqual(-2 * model.loglikes({})[0][0], 3.614504, 4)
            bib = model.likelihood[name].get_bibtex()
            self.assertTrue('Lewis' in bib if last_bib is None else bib == last_bib)
