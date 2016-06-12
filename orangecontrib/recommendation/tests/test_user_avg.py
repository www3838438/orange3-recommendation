import unittest

import numpy as np
from orangecontrib.recommendation import UserAvgLearner
from sklearn.metrics import mean_squared_error
import math
import Orange

class TestUserAvg(unittest.TestCase):

    # def test_UserAvg_swap_columns(self):
    #     # Recommender
    #     learner = UserAvgLearner(verbose=False)
    #
    #     # Dataset 1
    #     filename = '../datasets/users-movies-toy.tab'
    #     data = Orange.data.Table(filename)
    #     recommender = learner(data)
    #     prediction = recommender.predict_items()
    #     y_pred1 = prediction[data.X[:, recommender.order[0]],
    #                          data.X[:, recommender.order[1]]]
    #
    #     # Dataset 2
    #     filename = '../datasets/users-movies-toy2.tab'
    #     data = Orange.data.Table(filename)
    #     recommender = learner(data)
    #     prediction = recommender.predict_items()
    #     y_pred2 = prediction[data.X[:, recommender.order[0]],
    #                          data.X[:, recommender.order[1]]]
    #
    #     # Compare results
    #     np.testing.assert_array_equal(y_pred1, y_pred2)


    def test_UserAvg_correctness(self):
        filename = '../datasets/users-movies-toy.tab'
        data = Orange.data.Table(filename)

        # Train recommender
        learner = UserAvgLearner(verbose=False)
        recommender = learner(data)

        # Set ground truth
        ground_truth = np.asarray([3.25, 3.6666, 3.25, 3.3333, 3.3333, 2.6666,
                                   2.6, 3.6666])

        # Compare results
        np.testing.assert_array_almost_equal(recommender.users_average,
                                             ground_truth,
                                             decimal=2)


    def test_UserAvg_predict_items(self):
        # Load data
        filename = '../datasets/users-movies-toy.tab'
        data = Orange.data.Table(filename)

        # Train recommender
        learner = UserAvgLearner(verbose=False)
        recommender = learner(data)

        # Compute predictions
        prediction = recommender.predict_items()
        y_pred = prediction[data.X[:, recommender.order[0]],
                            data.X[:, recommender.order[1]]]

        # Compute RMSE
        rmse = math.sqrt(mean_squared_error(data.Y, y_pred))
        print('-> RMSE (predict items): %.3f' % rmse)

        # Check correctness
        self.assertGreaterEqual(rmse, 0)


    def test_UserAvg_input_data(self):
        # Load data
        filename = '../datasets/users-movies-toy.tab'
        data = Orange.data.Table(filename)

        # Train recommender
        learner = UserAvgLearner(verbose=False)
        recommender = learner(data)

        # Compute predictions
        y_pred = recommender(data)

        # Compute RMSE
        rmse = math.sqrt(mean_squared_error(data.Y, y_pred))
        print('-> RMSE (input data): %.3f' % rmse)

        # Check correctness
        self.assertGreaterEqual(rmse, 0)


    def test_UserAvg_pairs(self):
        # Load data
        filename = '../datasets/users-movies-toy.tab'
        data = Orange.data.Table(filename)

        # Train recommender
        learner = UserAvgLearner(verbose=False)
        recommender = learner(data)

        # Create indices to test
        sample_size = 10
        num_users, num_items = recommender.shape
        idx_users = np.random.randint(0, num_users, size=sample_size)
        idx_items = np.random.randint(0, num_items, size=sample_size)
        indices = np.column_stack((idx_users, idx_items))

        # Compute predictions
        y_pred = recommender(indices)
        print('-> Same number? (pairs): %r' % (len(y_pred) == sample_size))

        # Check correctness
        self.assertEqual(len(y_pred), sample_size)


    def test_ItemAvg_CV(self):
        from Orange.evaluation.testing import CrossValidation

        # Load data
        filename = '../datasets/users-movies-toy.tab'
        data = Orange.data.Table(filename)

        users_avg = UserAvgLearner(verbose=False)
        learners = [users_avg]

        res = CrossValidation(data, learners, k=5)
        rmse = Orange.evaluation.RMSE(res)
        r2 = Orange.evaluation.R2(res)

        print("Learner  RMSE  R2")
        for i in range(len(learners)):
            print(
                "{:8s} {:.2f} {:5.2f}".format(learners[i].name, rmse[i], r2[i]))

        self.assertIsInstance(rmse, np.ndarray)


if __name__ == "__main__":
    unittest.main()
