import unittest
from pathlib import Path
from shutil import rmtree
from gfagraphs.gfagraphs import Graph


class TestLoadingGFA(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestLoadingGFA, self).__init__(*args, **kwargs)

    def test_notexists(self):
        with self.assertRaises(OSError):
            Graph('.tests/doesnotexists.gfa')

    def test_emptyfile(self):
        with open(gfa_path := '.tests/emptyfile.gfa', "w") as writer:
            writer.write("")
        with self.assertRaises(IOError):
            Graph(gfa_path)

    def test_baddescriptorfile(self):
        with open(gfa_path := '.tests/badfile.txt', "w") as writer:
            writer.write("")
        with self.assertRaises(IOError):
            Graph(gfa_path)

    def test_badgfa(self):
        with open(gfa_path := '.tests/bad.gfa', "w") as writer:
            writer.write("hello world")
        with self.assertRaises(ValueError):
            Graph(gfa_path)

    def test_minimalgfa(self):
        with open(gfa_path := '.tests/minimalgfa.gfa', "w") as writer:
            writer.write("H	VN:Z:1.1")
        self.assertEqual(1, len(Graph(gfa_path).headers))


if __name__ == '__main__':
    Path('.tests').mkdir(parents=True, exist_ok=True)
    unittest.main()
    rmtree('.tests')
