# WMPCleaning
Data Processing and Cleaning for WMP Lab (developed by CMParlett)

## DDAuto.py
Cleans Delayed Discounting Data to return Overall and by block k-scores
### Options
participantidtype='[0-9][0-9][0-9]'

## SNBAutoComputer
Add's n-back and luretype to E-Prime Merged file for Spatial N-back (computer version)
###Options
test = False #print out and create csv with iterations for checking
KeepEmptyRows = False #delete rows with no nback information
rawFile = 'New.csv' #raw datafile name
codeTargetsAs = 'O' #What should targets be coded as, lure type wise? usually O or 0
csvNbackColName = 'nbacklevel' #What column is n-back level info in?


## Split Condition Curves.ipynb
Jupyter Notebook that outputs and saves training curves for MatchQuest Data
###Options
ref.csv # conditions of participants, saved as csv filename

## awa.py
Grades data for Auditory Word Attack

## baselineAuto.py
Grades and Summarizes n-back baseline (Spatial)

## deletefiles.py
Deletes excess files for baselineAuto.py

## mmScore.py
Scores MetaMemory Task

## pvt.py
Scores PVT Task

## spelling.py
Scores MillHill Vocabulary Task
