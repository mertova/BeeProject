import unittest
from pathlib import Path

import execute_extraction


class IdentificationTest(unittest.TestCase):

    def test_analysis(self):
        # given
        data_samples = Path('./scans/Niedersach_examples_10/').as_posix()
        reference = Path('./scans/Niedersach_examples_10/Sample_Niedersachsen-2-1.png').as_posix()
        output_path = Path('./results/7/')
        output_path.mkdir(parents=True, exist_ok=True)

        # when
        template, grid = execute_extraction.main(path_t_output=output_path.as_posix(), path_reference=reference,
                                                 eps_h=20, eps_v=15, template_extraction=True,
                                                 path_data_sample=data_samples, data_limit=15, transform=True,
                                                 debug=True)
        self.assertIsNotNone(template)
        self.assertIsNotNone(grid)
        print(template)
        print(grid)

    def test_no_table_extraction(self):
        reference = Path('../data/form1/mask.png').as_posix()
        output_path = Path('./results/9/')
        output_path.mkdir(parents=True, exist_ok=True)
        grid = execute_extraction.main(path_t_output=output_path.as_posix(), path_reference=reference,
                                       eps_h=10, eps_v=20, template_extraction=False,
                                       debug=True)
        self.assertIsNotNone(grid)
        print(grid)


if __name__ == '__main__':
    unittest.main()
    print('Done!')
