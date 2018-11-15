from sqlalchemy import create_engine
import pandas as pd
import numpy as np

engine = create_engine('postgresql://continube:ContiNube1234@staging.continube.co:5432/continube')
dfcontrols = pd.read_sql('select * from controls',con=engine)
dfframeworks = pd.read_sql('select * from frameworks',con=engine)

hieararchyLevel=5
muxer={}
for i in range(0,hieararchyLevel):
    muxer[i]=10**(hieararchyLevel-1-i)

selectcols = ['id','name','version']
frameworksslice = dfframeworks.loc[:,selectcols]
frameworksslice = frameworksslice.rename(columns={'id':'framework_id', 'version':'framework_version'})
selectcols = ['framework_id','name','displayable']
controlsslice = dfcontrols.loc[:,selectcols]
joindf = pd.merge(frameworksslice,controlsslice,on='framework_id')
joindf = joindf.rename(columns={'name_x':'framework_name', 'name_y':'control_name', 'displayable':'number'})

del dfcontrols, dfframeworks, controlsslice, frameworksslice

selectedframeworks=['FedRamp']
selectedversions=['1.0']
subdf=joindf.loc[joindf.loc[:,'framework_name'].isin(selectedframeworks)]
subdf=subdf.loc[subdf.loc[:,'framework_version'].isin(selectedversions)]
numdf=pd.DataFrame(columns=['idx','number','level','cumnum'])

for recindex, record in subdf.iterrows():
    numschemeslice = record['number'].split('.')
    cumnum = 0
    for numindex in range(len(numschemeslice)):
        cumnum += muxer.get(numindex) * int(numschemeslice[numindex])
    numdf = numdf.append({'idx':recindex,'number':record['number'], 'level':len(numschemeslice),'cumnum':cumnum},ignore_index=True) 
sorteddf=pd.merge(subdf,numdf,on='number',how='inner').sort_values(by='cumnum')

del subdf, numdf

#Assign Random Compliance% to all leaf controls
#1. Identify leaf controls
#2. Randomly assign 'Pass' and 100% to a certain % of Controls
#3. For the unassigned leaf controls, assign a random compliance value between 0 to 100%

# default assign root and leaf attributes as False
sorteddf['leaf']=-1
# sorteddf.loc[:,'root']=sorteddf.loc[sorteddf.loc[:,'cumnum']%10**5==0]
def checkIfRoot(row):
    return row['cumnum']%10**(hieararchyLevel-1)==0
sorteddf['root']=sorteddf.apply(checkIfRoot, axis=1)

# Build a recursive function to check for the leaf node        
def checkIfLeaf(row):
    if row['root']==True:
        return 0
    # let us take a sample number: 101100 (assuming hieararchy level = 5)
    # If we have 101110 - 101190; then 101100 should have leaf='false'
    # however if, 101100 does not have any other value below it, until the next hierarchy level 101200, then it should have leaf=true
    rowscumnum= row['cumnum']
    rowslevel=row['level']
    nextInHiearGT=rowscumnum #Greater Than
    nextInHiearLT=int(((rowscumnum/10**(hieararchyLevel - rowslevel  ))+1)*10**(hieararchyLevel - rowslevel))
    #print(row, nextInHiearGT, nextInHiearLT)

    childNodes=sorteddf.loc[(sorteddf.loc[:,'cumnum']>nextInHiearGT) & (sorteddf.loc[:,'cumnum']<nextInHiearLT)]
    noOfChildren=len(childNodes)
    if noOfChildren==0:
        return 1
    else:
        return 0
sorteddf.loc[:,'leaf']=sorteddf.apply(checkIfLeaf,axis=1)

def changeControlName(row):
    return row['control_name'].lower()
sorteddf.loc[:,'control_name']=sorteddf.apply(changeControlName,axis=1) 

sorteddf.to_csv('out.csv')