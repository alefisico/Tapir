import json, sys
import numpy as np
from collections import Counter

data = json.load(sys.stdin)

statuses = [d["State"] for d in data.values()]
print Counter(statuses)

finished = [d for d in data.values() if d["State"] == "finished"]
wt = np.array([int(d["WallDurations"][-1])/3600.0 for d in finished])
rss = np.array([int(d["ResidentSetSize"][-1])/1024.0/1024.0 for d in finished])
print "WallTime mean={0:.2f} std={1:.2f} p0.9={2:.2f}".format(np.mean(wt), np.std(wt), np.percentile(wt, 90))
print "RSS mean={0:.2f} std={1:.2f}".format(np.mean(rss), np.std(rss))
