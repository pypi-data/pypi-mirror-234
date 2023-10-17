import pandas as pd

def findsth(a, var, wantval):
    varlist = list(a.loc[:, var])
    indexlist = []
    indexnum = 0
    finallist = pd.DataFrame()
    
    for i in varlist:
        if(i == wantval):
            indexlist.append(indexnum)
        indexnum += 1
    finallist = a.loc[indexlist]
    return finallist


def findsth_all(a, wantval):
    varlist = []
    indexlist = []
    indexnum = 0
    for temp in a:
        varlist.append(temp)
    for var in varlist:
        templist = list(a.loc[:, var])
        indexnum = 0
        for i in templist:
            if(i == wantval):
                indexlist.append(indexnum)
            indexnum += 1
    finallist = a.loc[indexlist]
      
    return finallist


