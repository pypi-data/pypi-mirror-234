import unittest
import numpy as np
import os
import sys
from sklearn.metrics import mean_squared_error

from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
import logging

# Get the current directory of the test file
current_dir = os.path.dirname(__file__)

# Get the absolute path to the main directory (one level up)
main_dir = os.path.abspath(os.path.join(current_dir, ".."))

print(main_dir)

# Add the main directory to the Python path
sys.path.insert(0, main_dir)

from gradientcobra.gradientcobra import GradientCOBRA

from sklearn.utils.estimator_checks import check_estimator


class TestPrediction(unittest.TestCase):
    def setUp(self):
        rd_state = np.random.RandomState(11111)
        n_features = 20

        # D1 = train machines; D2 = create COBRA; D3 = calibrate epsilon, alpha; D4 = testing
        X, y = make_regression(
            n_samples=1000, 
            n_features=n_features, 
            noise=1,
            random_state=rd_state)

        # Train-test data splitting
        X_train, X_test, y_train, y_test = train_test_split(
            X, 
            y, 
            test_size=0.2, 
            random_state=rd_state)

        agg_model = GradientCOBRA(random_state=rd_state,
                                  show_progress = True)
        agg_model.fit(X_train, y_train)

        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test
        self.GradientCOBRA = agg_model

    def test_opt_bandwidth(self):
        expected = 0.5591282113123428 # 0.5581881403503334 # 0.5592629558714854
        self.assertAlmostEqual(expected, self.GradientCOBRA.optimization_outputs['opt_bandwidth'])
    
    def test_basic_estimators(self):
        expected = [1.2032133203682551, 1.2448736091320127, 1.2087950033295554, 4670.95417246458, 2578.4586697386835]
        res = [mean_squared_error(self.GradientCOBRA.pred_X_l[:,j] / self.GradientCOBRA.normalize_constant, self.y_train[self.GradientCOBRA.iloc_l]) for j in range(len(expected))]
        for i in range(5):
            self.assertAlmostEqual(expected[i], res[i])

    def test_predict(self):
        expected = 30.97875936419449 #30.976945691554874 # 30.979022169450154 
        result = mean_squared_error(self.GradientCOBRA.predict(self.X_test), self.y_test)
        self.assertAlmostEqual(expected, result)
        
if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)
    unittest.main()
