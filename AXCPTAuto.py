from __future__ import division
import re, csv, os, os.path
import numpy as np
import glob
import shutil

#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
WhatTrialType = 'AY'
test = False
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------


#REGEX to find PID
CurrDir = os.getcwd()
if test:
    print "You're in " + CurrDir
    print "__________________"
    print "STARTED"
filenames = glob.glob('AXCPT.csv')
if test:
    print "FILENAME: ", filenames

ACC = {}
RT = {}
SIDS = []
ACCAX = {WhatTrialType:{}, 'NOT':{}}
RTAX = {WhatTrialType:{}, 'NOT':{}}

for name in filenames: #each session
    reader = csv.DictReader(open(name, 'rU'))  # open reader

    outputName = "AXCPTclean.csv"

    if os.path.exists(outputName):
        writer = csv.writer(open(outputName, 'ab'))  # open filewriter
    else:
        writer = csv.writer(open(outputName, 'wb'))
        writer.writerow(
            ['PID', 'Session', 'RT1', 'RT2', 'RT All','ACC1', 'ACC2', 'ACC All',
             WhatTrialType.lower() +'RT1', WhatTrialType.lower() +'RT2',
              WhatTrialType.lower() +'RT All',WhatTrialType.lower() +'ACC1',
              WhatTrialType.lower() +'ACC2', WhatTrialType.lower() +'ACC All'])  # write headers

    for row in reader: #get info from each file
        if row['ProcedureBlock'] == 'Break':
            continue
        elif row['ProcedureBlock'] == 'PracticeProc':
            continue

        Subject = row['Subject']
        Session = row['Session']
        ACC1 = int(row['ShowStimulus1.ACC'])
        ACC2 = int(row['ShowStimulus2.ACC'])
        RT1 = int(row['ShowStimulus1.RT'])
        RT2 = int(row['ShowStimulus2.RT'])
        TrialType = row['TrialType']

        ACC[Subject] = ACC.get(Subject, {}) #add Subject entry to Dict
        ACC[Subject][Session] = ACC[Subject].get(Session,{})
        ACC[Subject][Session]['ACC1'] = ACC[Subject][Session].get('ACC1', [])
        ACC[Subject][Session]['ACC1'].append(ACC1)
        ACC[Subject][Session]['ACC2'] = ACC[Subject][Session].get('ACC2', [])
        ACC[Subject][Session]['ACC2'].append(ACC2)

        RT[Subject] = RT.get(Subject, {}) #add Subject entry to Dict
        RT[Subject][Session] = RT[Subject].get(Session,{})
        RT[Subject][Session]['RT1'] = RT[Subject][Session].get('RT1', [])
        RT[Subject][Session]['RT1'].append(RT1)
        RT[Subject][Session]['RT2'] = RT[Subject][Session].get('RT2', [])
        RT[Subject][Session]['RT2'].append(RT2)

        if TrialType == WhatTrialType:
            ACCAX[WhatTrialType][Subject] = ACCAX[WhatTrialType].get(Subject,{'1':{'ACCAX1':[], 'ACCAX2':[]}, '2':{'ACCAX1':[], 'ACCAX2':[]}}) #add Subject entry to Dict
            ACCAX[WhatTrialType][Subject][Session]['ACCAX1'].append(ACC1)
            ACCAX[WhatTrialType][Subject][Session]['ACCAX2'].append(ACC2)

            RTAX[WhatTrialType][Subject] = RTAX[WhatTrialType].get(Subject, {'1':{'RTAX1':[], 'RTAX2':[]}, '2':{'RTAX1':[], 'RTAX2':[]}}) #add Subject entry to Dict
            RTAX[WhatTrialType][Subject][Session]['RTAX1'].append(RT1)
            RTAX[WhatTrialType][Subject][Session]['RTAX2'].append(RT2)
        else:
            ACCAX['NOT'][Subject] = ACCAX['NOT'].get(Subject, {'1':{'ACCAX1':[], 'ACCAX2':[]}, '2':{'ACCAX1':[], 'ACCAX2':[]}}) #add Subject entry to Dict
            ACCAX['NOT'][Subject][Session]['ACCAX1'].append(ACC1)
            ACCAX['NOT'][Subject][Session]['ACCAX2'].append(ACC2)

            RTAX['NOT'][Subject] = RTAX['NOT'].get(Subject, {'1':{'RTAX1':[], 'RTAX2':[]}, '2':{'RTAX1':[], 'RTAX2':[]}}) #add Subject entry to Dict
            RTAX['NOT'][Subject][Session]['RTAX1'].append(RT1)
            RTAX['NOT'][Subject][Session]['RTAX2'].append(RT2)


print "RTAX:    ", RTAX[WhatTrialType]['289']
print "ACCAX:    ", ACCAX[WhatTrialType]['289']
print "RTAX:    ", RTAX[WhatTrialType]['223']
print "ACCAX:    ", ACCAX[WhatTrialType]['223']
for sid in ACC:
    for sess in ACC[sid]:
        # ['PID', 'Session', 'RT1', 'RT2', 'RT All','ACC1', 'ACC2', 'ACC All',
        # 'axRT1', 'axRT2', 'axRT All','axACC1', 'axACC2', 'axACC All'])  # write headers
        writer.writerow([sid, sess, np.nanmean(RT[sid][sess]['RT1']), np.nanmean(RT[sid][sess]['RT2']),
        np.nanmean(RT[sid][sess]['RT1']+RT[sid][sess]['RT2']),np.nanmean(ACC[sid][sess]['ACC1']),
        np.nanmean(ACC[sid][sess]['ACC2']),np.nanmean(ACC[sid][sess]['ACC1']+ACC[sid][sess]['ACC2']),

        np.nanmean(RTAX[WhatTrialType][sid][sess]['RTAX1']),
        np.nanmean(RTAX[WhatTrialType][sid][sess]['RTAX2']),
        np.nanmean(RTAX[WhatTrialType][sid][sess]['RTAX1']+RTAX[WhatTrialType][sid][sess]['RTAX2']),
        np.nanmean(ACCAX[WhatTrialType][sid][sess]['ACCAX1']),
        np.nanmean(ACCAX[WhatTrialType][sid][sess]['ACCAX2']),
        np.nanmean(ACCAX[WhatTrialType][sid][sess]['ACCAX1']+ACCAX[WhatTrialType][sid][sess]['ACCAX2'])
        ])
