import unittest
from gpforecaster.model.gpf import GPF
import tsaugmentation as tsag
import timeit


class TestModel(unittest.TestCase):
    def setUp(self):
        self.data = tsag.preprocessing.PreprocessDatasets(
            "prison", freq="Q"
        ).apply_preprocess()
        self.n = self.data["predict"]["n"]
        self.s = self.data["train"]["s"]
        self.gpf = GPF("prison", self.data, log_dir="..")

    def test_early_stopping_fn(self):
        self.gpf.val_losses = [5.1, 5.2, 4.9, 5.0, 5.1, 5.2]
        res, non_decrease = self.gpf.early_stopping(self.gpf.val_losses, 2)
        print(non_decrease)
        self.assertTrue(non_decrease == 3)
        self.assertTrue(res)
