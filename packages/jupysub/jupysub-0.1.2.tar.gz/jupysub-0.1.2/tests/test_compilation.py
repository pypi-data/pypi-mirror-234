import os
import unittest
import subprocess
import numpy as np
import re

class TestJuPySub(unittest.TestCase):

    def test_compilation(self):
        cwd = os.path.dirname(__file__)
        print("Performing compilation, please wait...")
        subprocess.check_output('jupysub -i data/example.ipynb -o example_out.ipynb -ra -rb', shell=True, cwd=cwd) 

        f = open(os.path.join(cwd, 'example_out.ipynb'), 'r')
        result = f.readlines()
        f.close()

        f = open(os.path.join(cwd, 'data', 'example_out.ipynb'), 'r')
        expected = f.readlines()
        f.close()

        # regex pattern for timestamp
        ptn = r'^.*"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{6}Z",?$'

        for i in range(len(result)):

            # skip lines that contain a timestamp
            # or that contain specific versioning data
            if re.match(ptn, result[i]) or '"version"' in result[i]:
                continue

            np.testing.assert_equal(result[i], expected[i])

if __name__ == '__main__':
    unittest.main()