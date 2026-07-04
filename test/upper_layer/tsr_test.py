import unittest
from pathlib import Path

import cv2

from table.table import Table
from tsr import Tsr

REPO_ROOT = Path(__file__).resolve().parents[2]


class TsrTest(unittest.TestCase):

    output_path = None

    @classmethod
    def setUpClass(cls):
        cls.output_path = REPO_ROOT / "test" / "results" / "tsr"
        cls.output_path.mkdir(parents=True, exist_ok=True)

    def test_tsr_form1(self):
        # given
        form = REPO_ROOT / "resources" / "LHI-final" / "form_contrasted_31_clean.png"

        # when
        tsr = Tsr(form, 40, 20, out_dir=self.output_path)
        grid = tsr.extract()
        form_img = cv2.imread(form.as_posix())
        form_img = grid.render(form_img, True, True)
        cv2.imwrite((self.output_path / "grid_ref.png").as_posix(), form_img)

        # test
        self.assertEqual(type(grid), Table)
        self.assertEqual(grid.shape, (13, 40))


if __name__ == '__main__':
    unittest.main()
    print('Done!')
