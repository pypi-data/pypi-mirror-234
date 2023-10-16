import qtc.ext.unittest as ut
from qtc.ext.enum import Enum


class TestEnum(ut.TestCase):
    def test_retrieve_by_name(self):
        class RiskRegionEnum(Enum):
            AP = 'Asia'
            EU = 'EU'
            US = 'US'
            WW = 'WW'
            ROW = 'ROW'

        self.assertEqual(RiskRegionEnum.retrieve_by_name('AP'), RiskRegionEnum.AP)
        self.assertEqual(RiskRegionEnum.retrieve_by_name('EU'), RiskRegionEnum.EU)
        self.assertEqual(RiskRegionEnum.retrieve_by_name('US'), RiskRegionEnum.US)

    def test_retrieve(self):
        class Symbology(Enum):
            BARRA_ID = 'BarraId'
            AXIOMA_ID = 'AxiomaId'
            FACTSET_ID = 'FactsetId'

        self.assertEqual(Symbology.retrieve('BarraId'), Symbology.BARRA_ID)
        self.assertEqual(Symbology.retrieve('AXIOMA_ID'), Symbology.AXIOMA_ID)
        self.assertEqual(Symbology.retrieve('FactsetId'), Symbology.FACTSET_ID)


if __name__ == '__main__':
    ut.main()
