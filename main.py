from random import randint
from math import sin
import numpy as np
from sklearn.neighbors import LocalOutlierFactor
import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerPathCollection

# Local Outlier Factor
# High/Low Pass Frequency

x = [i for i in range(100)]
y = []
values = []

for i in range(100):
    y.append(i + 5 * sin(i/2))

values = [[num] for num in y]

print(len(x))
print(len(values))

ground_truth = np.ones(len(values), dtype=int)

clf = LocalOutlierFactor(n_neighbors=10, contamination=0.1)
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
plt.xlim((-5, 105))
plt.ylim((-5, 105))
plt.xlabel("prediction errors: %d" % (n_errors))
plt.legend(
    handler_map={scatter: HandlerPathCollection(update_func=update_legend_marker_size)}
)
plt.title("Local Outlier Factor (LOF)")
plt.show()