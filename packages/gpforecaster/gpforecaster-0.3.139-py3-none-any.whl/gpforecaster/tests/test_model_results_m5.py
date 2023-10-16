import unittest
import tsaugmentation as tsag
from gpforecaster.model.gpf import GPF
import shutil


class TestModel(unittest.TestCase):

    def setUp(self):
        self.data = tsag.preprocessing.PreprocessDatasets('m5', test_size=10, freq='W').apply_preprocess()
        self.n = self.data['predict']['n']
        self.s = self.data['train']['s']
        self.gpf = GPF('m5', self.data, log_dir="..")

    def test_predict_shape_xvalidation(self):
        model, like = self.gpf.train(epochs=2, n_splits=2)
        preds, preds_scaled = self.gpf.predict(model, like)
        self.assertTrue(preds[0].shape == (self.n, self.s))

    def test_predict_shape(self):
        model, like = self.gpf.train(epochs=2, n_splits=2, cross_validation=False)
        preds, preds_scaled = self.gpf.predict(model, like)
        self.gpf.plot_losses()
        self.assertTrue(preds[0].shape == (self.n, self.s))
