import unittest
from pathlib import Path

from table.table import Table
from tsr import GridExtraction


class IdentificationTest(unittest.TestCase):

    def test_tsr_form1(self):
        # given ... change result path
        form = Path('../data/form1/form1-manual-clean.png')
        output_path = Path('./results/7/')
        output_path.mkdir(parents=True, exist_ok=True)

        # when
        tsr = GridExtraction(form, output_path, 20, 15)
        grid = tsr.extract(True)

        # test
        self.assertEqual(type(grid), Table)
        self.assertEqual(grid.shape, (20, 15))
        print(grid)


if __name__ == '__main__':
    unittest.main()
    print('Done!')
