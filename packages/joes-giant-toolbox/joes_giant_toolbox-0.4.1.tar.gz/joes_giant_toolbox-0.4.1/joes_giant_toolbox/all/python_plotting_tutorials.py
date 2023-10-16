class PythonPlottingTutorials:
    """Example code snippets for creating common data visualisations in python

    Example Usage
    -------------
    >>> import joes_giant_toolbox.dataviz
    >>> plot_ref = joes_giant_toolbox.dataviz.PythonPlottingTutorials()
    >>> print(plot_ref.available_plots)
    >>> print( plot_ref.tutorials.get("heatmap") )
    >>> exec( plot_ref.tutorials.get("heatmap") )
    """

    def __init__(self):
        self.tutorials: dict = {
            "grid_of_matplotlib_plots": """
# https://matplotlib.org/stable/gallery/subplots_axes_and_figures/subplots_demo.html
from matplotlib import pyplot as plt
import numpy as np

n_rows = 3
n_cols = 5

shared_x = list(range(100))

fig, axs = plt.subplots(nrows=n_rows, ncols=n_cols, figsize=(12,8))    # note: figsize is the size of the global plot   
for row_idx in range(n_rows):
    for col_idx in range(n_cols):
        axs[row_idx,col_idx].plot(
                shared_x
            ,   np.random.normal(size=100).cumsum()   # a random normal walk
        )
        axs[row_idx,col_idx].set_xlabel("x axis label")
        axs[row_idx,col_idx].set_ylabel("y axis label")
        axs[row_idx,col_idx].set_title(f"Axis [{row_idx},{col_idx}]")
for ax in axs.flat:    # only keep the axis labels and axis ticks on the outer plots
    ax.label_outer()
fig.suptitle("Global Plot Title")      
fig.tight_layout()

plt.show()
            """,
            "heatmap": """
# https://seaborn.pydata.org/generated/seaborn.heatmap.html
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns

sns.set_theme()

data_for_heatmap = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])

ax = sns.heatmap(data_for_heatmap, annot=True)
ax.set_xticklabels(["a", "b", "c", "d"])
ax.set_yticklabels(["x", "y", "z"])

plt.show()

# same heatmap as above, but with data provided as pandas dataframe:
pandas_df_data_for_heatmap = pd.DataFrame(
    {"a": [1, 5, 9], "b": [2, 6, 10], "c": [3, 7, 11], "d": [4, 8, 12]},
    index=["x", "y", "z"],
)

ax = sns.heatmap(pandas_df_data_for_heatmap, annot=True)

plt.show()
            """,
        }
        self.available_plots: list = list(self.tutorials.keys())
