## charts for performance

from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
import bokeh
import pandas as pd

output_file("bar_colormapped.html")

fname = "complete.csv"

## preparing Data
ds = pd.read_csv(fname)

bySprint = ds.groupby(ds.group_id)["Estimado"].sum()
byDev  = ds.groupby(ds.group_id)["Estimado","Realizado"].sum()
bySprint_dev= ds.groupby([ds.Assignee,ds.group_id])["Estimado","Realizado"].sum()