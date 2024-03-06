import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.neighbors import LocalOutlierFactor
from random import randint
from matplotlib.legend_handler import HandlerPathCollection

# Local Outlier Factor?
# High/Low Pass Frequency?
# Test both

df = pd.read_csv('resources/sample_data.csv')
x = df['x']
y = df['y']

values = [[num] for num in y]

ground_truth = np.ones(len(values), dtype=int)

clf = LocalOutlierFactor(n_neighbors=5, contamination=0.1)
y_pred = clf.fit_predict(values)
n_errors = (y_pred != ground_truth).sum()
X_scores = clf.negative_outlier_factor_

def update_legend_marker_size(handle, orig):
    "Customize size of the legend marker"
    handle.update_from(orig)    
    handle.set_sizes([20])


plt.scatter(x, y, color="k", s=3.0, label="Data points")
# plot circles with radius proportional to the outlier scores
radius = (X_scores.max() - X_scores) / (X_scores.max() - X_scores.min())
scatter = plt.scatter(
    x,
    y,
    s=1000 * radius,
    edgecolors="r",
    facecolors="none",
    label="Outlier scores",
)
plt.axis("tight")
plt.xlabel("prediction errors: %d" % (n_errors))
plt.legend(handler_map={scatter: HandlerPathCollection(update_func=update_legend_marker_size)})
plt.title("Local Outlier Factor (LOF)")
plt.show()