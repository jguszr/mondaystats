## charts for performance

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import mpld3

fname = "complete.csv"

## preparing Data
ds = pd.read_csv(fname)

bySprint = ds.groupby(ds.group_id)["Estimado"].sum()
byDev  = ds.groupby(ds.group_id)["Estimado","Realizado"].sum()
bySprint_dev= ds.groupby([ds.group_id,ds.Assignee])["Estimado","Realizado"].sum()


## charting the shit out of it !
plt.figure()
bySprint.plot.bar()
plt.title("Estimativas por Sprint")
plt.grid()
bySprint_dev.plot(kind="bar")
plt.show() 
