import pandas as pd

# DataArr = {'Day':[1,2,3,4,5,6], 'Visitors':[100,200,500,10000,20,0], 'BounceRate':[0,0,1,1100,20,10]}
DataArr1 = {"HPI":[80,90,100,110], "People Names" : ["period1","period2","",""]}
dframe = pd.DataFrame(DataArr1)

#dframe = pd.DataFrame(DataArr)
print (dframe)