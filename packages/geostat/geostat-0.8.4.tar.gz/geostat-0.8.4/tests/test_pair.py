import numpy as np
import tensorflow as tf
from geostat import Featurizer, GP, Model, NormalizingFeaturizer, Trend
import geostat.kernel as krn

def test_pairwise_prediction():
    np.random.seed(2)
    tf.random.set_seed(2)

    # Create random locations in a square centered on the origin.
    locs1 = np.random.normal(size=[1000, 2])

    # Initialize featurizer of location for trends.
    def trend_terms(x, y): return x, y, x*y
    featurizer = NormalizingFeaturizer(trend_terms, locs1)
    kernel = krn.TrendPrior(featurizer) + krn.SquaredExponential(sill=1.) + krn.Noise()

    # Generate data.
    vals1 = Model(
        GP(0, kernel),
        parameters = dict(alpha=1., range=0.33, nugget=1.),
        verbose=True).generate(locs1).vals

    # Fit GP.
    model = Model(
        GP(0, kernel),
        parameters = dict(alpha=2., range=1., nugget=0.5),
        verbose=True).fit(locs1, vals1, iters=100, step_size=1e-1)

    assert np.allclose(
        [model.parameters[p] for p in ['range', 'nugget']],
        [0.33, 1.],
        rtol=0.3)

    # Interpolate using GP.
    N = 40
    xx, yy = np.meshgrid(np.linspace(-1, 1, N), np.linspace(-1, 1, N))
    locs2 = np.stack([xx, yy], axis=-1).reshape([-1, 2, 2])

    mean, var = model.predict(locs2, pair=True)
