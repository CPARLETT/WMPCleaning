from __future__ import division
try:
    import re, csv, os, os.path
    import numpy as np
except:
    print "ERROR: Install numpy  using pip"
try:
    import glob
except:
    print "ERROR: Install glob using pip"
try:
    import shutil
except:
    print "ERROR: Install shutil using pip"

#TODO
# RT Correct
#add Hits to Data File (H-eoc)
def NBackWithLures(numBlocks = 6, test = False, Block = True, Level = True, Session = True ):

    CurrDir = os.getcwd()
    print "You're in " + CurrDir
    print "__________________"
    print "STARTED"

    filenames = glob.glob('[0-9][0-9][0-9]_[0-9]_20[0-9][0-9]_*.csv')
    if test:
        print "FILENAME: ", filenames
    for name in filenames: #each session
        reader = csv.DictReader(open(name, 'rU'))  # open reader
        date = re.findall('(20[0-9][0-9]_[0-9][0-9]_[0-9][0-9])', name)
        if test:
            print "DATE: ",date
        outputName = "clean.csv"



        acc = {3:{},2:{}} #{3:{1:{L:[], NL:[], All: []},2:{L:[], NL:[], All: []}...}, 2:{1:{L:[], NL:[], All: []},2:{L:[], NL:[], All: []}...}}
        for i in range(1, numBlocks+1):
            acc[3][i] = acc[3].get(i,{'L': [], 'NL': [], 'All': []})
            acc[2][i] = acc[2].get(i,{'L': [], 'NL': [], 'All': []})
        rts = {3:{},2:{}}
        for i in range(1, numBlocks+1):
            rts[3][i] = rts[3].get(i,{'L': [], 'NL': [], 'All': []})
            rts[2][i] = rts[2].get(i,{'L': [], 'NL': [], 'All': []})
        rtsCorrect = {3:{},2:{}}
        for i in range(1, numBlocks+1):
            rtsCorrect[3][i] = rts[3].get(i,{'L': [], 'NL': [], 'All': []})
            rtsCorrect[2][i] = rts[2].get(i,{'L': [], 'NL': [], 'All': []})
        eoo = {3:{},2:{}}
        for i in range(1, numBlocks+1):
            eoo[3][i] = eoo[3].get(i,[])
            eoo[2][i] = eoo[2].get(i,[])
        eoc = {3:{},2:{}}
        for i in range(1, numBlocks+1):
            eoc[3][i] = eoc[3].get(i,[])
            eoc[2][i] = eoc[2].get(i,[])
        lureRound = {3:{},2:{}}
        for i in range(1, numBlocks+1):
            lureRound[3][i] = lureRound[3].get(i,[])
            lureRound[2][i] = lureRound[2].get(i,[])
        hits = {3:{},2:{}}
        for i in range(1, numBlocks+1):
            hits[3][i] = hits[3].get(i,[])
            hits[2][i] = hits[2].get(i,[])

        if os.path.exists(outputName):
            writer = csv.writer(open(outputName, 'ab'))  # open filewriter
        else:
            writer = csv.writer(open(outputName, 'wb'))
            writer.writerow(
                ['PID', 'Date', 'Session', 'Level', 'Block', 'Lure Condition',

                'AccBlock', 'RTBlock', 'eooBlock', 'eocBlock', 'Acc Lure Block', 'RT Lure Block', 'Acc NLure Block', 'RT NLure Block', 'RT Correct Block','PR Block',

                'AccLev', 'RTLev', 'eooLev', 'eocLev','Acc Lure Lev', 'RT Lure Lev', 'Acc NLure Lev', 'RT NLure Lev','RT Correct Lev', 'PR Lev',

                'ACCSess', 'RT All Sess', 'eoo Sess', 'eoc Sess', 'Acc Lure Sess', 'RT Lure Sess','Acc NLure Sess', 'RT NLure Sess','RT Correct Sess', 'PR Sess'])  # write headers


        for row in reader: #get info from each file
            if row['practice'].lower() == 'true': #don't count practice
                continue
            pid = row['subject']
            if pid[0:2] == 'SP':
                pid = pid[2:]
            rnd = int(row["block number"])
            session = row['session']
            lev = int(row['level'])
            luretype = row['lure condition (0=no lures;1=1x n+1 lure and 1x n-1 lure;3=3x n+1 lures and 3x n-1 lures)']
            itemLure = row['presented stimulus type (0=nontarget;1=lure_minus;2=target;3=lure_plus)']

            #Check if Item is a Lure Item
            if itemLure == '1' or itemLure == '3':
                lureItem = True
            else:
                lureItem = False

            #get Dict of LureRounds
            if test:
                print lureRound[lev][rnd]
                print luretype
            lureRound[lev][rnd].append(luretype)
            #Don't count practice and skip unfinished data
            if len(row) <5 or row['practice'] == 'TRUE':
                print "short row or practice"
                continue

            #Find Where the RT is
            try:
                rt = int(row['RT left key'])
                rts[lev][rnd]['All'].append(rt)
                if lureItem:
                    rts[lev][rnd]['L'].append(rt)
                else:
                    rts[lev][rnd]['NL'].append(rt)
            except:
                pass
            try:
                rt = int(row['RT right key'])
                # rts[lev][rnd] = rts[lev].get(rnd, [])
                rts[lev][rnd]['All'].append(rt) # {1:[566,896,772,634], 2: [], 3: []}
                if lureItem:
                    rts[lev][rnd]['L'].append(rt)
                else:
                    rts[lev][rnd]['NL'].append(rt)
            except:
                pass

            #Get Accuracy, but also deal with old files that don't have the pressed Key row
            #What happens to Nulls? Ignore
            if row['accuracy'] =='0':
                try:
                    xyz = row['pressed key']
                except:
                    if row['RT left key'] == '0' or row['RT left key'] == '':
                        xyz = 'l'
                    elif row['RT right key'] == '0' or row['RT right key'] == '':
                        xyz = 'a'
                    else:
                        xyz = 'na' #don't count Non Responses

                if xyz == 'l':
                    x = 'o'
                    acc[lev][rnd]['All'].append(0)
                    if lureItem:
                        acc[lev][rnd]['L'].append(0)
                    else:
                        acc[lev][rnd]['NL'].append(0)
                    eoo[lev][rnd].append(1)
                elif xyz == "a":
                    x = 'c'
                    acc[lev][rnd]['All'].append(0)
                    if lureItem:
                        acc[lev][rnd]['L'].append(0)
                    else:
                        acc[lev][rnd]['NL'].append(0)
                    eoc[lev][rnd].append(1)
                else:
                    continue
            elif row['accuracy'] == '1':
                try:
                    rt = int(row['RT left key'])
                    rtsCorrect[lev][rnd]['All'].append(rt)
                    if lureItem:
                        rtsCorrect[lev][rnd]['L'].append(rt)
                    else:
                        rtsCorrect[lev][rnd]['NL'].append(rt)
                except:
                    pass
                try:
                    rt = int(row['RT right key'])
                    # rts[lev][rnd] = rts[lev].get(rnd, [])
                    rtsCorrect[lev][rnd]['All'].append(rt) # {1:[566,896,772,634], 2: [], 3: []}
                    if lureItem:
                        rtsCorrect[lev][rnd]['L'].append(rt)
                    else:
                        rtsCorrect[lev][rnd]['NL'].append(rt)
                except:
                    pass
                try:
                    xyz = row['pressed key']
                except:
                    if row['RT left key'] == '0' or row['RT left key'] == '':
                        xyz = 'l'
                    elif row['RT right key'] == '0' or row['RT right key'] == '':
                        xyz = 'a'
                    else:
                        xyz = 'na' #don't count Non Responses
                acc[lev][rnd]['All'].append(1)
                if lureItem:
                    acc[lev][rnd]['L'].append(1)
                else:
                    acc[lev][rnd]['NL'].append(1)
                if xyz == 'a':
                    hits[lev][rnd] = hits[lev].get(rnd, [])
                    hits[lev][rnd].append(1)
        if test:
            print " ACC:  ", acc
            print "RTS:   ", rts
            print "EOO:   ", eoo
            print "EOC:   ", eoc
            print "LURE:   ", lureRound
            print "HITS:   ", hits

        #MAke ALL lists
        #------------------------------------------------------------------------------
        #{3:{1:{L:[], NL:[], All: []},2:{L:[], NL:[], All: []}...}, 2:{1:{L:[], NL:[], All: []},2:{L:[], NL:[], All: []}...}}
        acc2 = list(i for i in acc[2].values()) #{1:{L:[], NL:[], All: []},2:{L:[], NL:[], All: []}...}
        acc2 = list(x for x in acc2) #{L:[], NL:[], All: []}
        acc2All = [d['All'] for d in acc2 if 'All' in d]
        acc2L =  [d['L'] for d in acc2 if 'L' in d]
        acc2NL = [d['NL'] for d in acc2 if 'NL' in d]
        acc2All = [item for sublist in acc2All for item in sublist]
        acc2NL = [item for sublist in acc2NL for item in sublist]
        acc2L = [item for sublist in acc2L for item in sublist]

        acc3 = list(i for i in acc[3].values()) #{1:{L:[], NL:[], All: []},3:{L:[], NL:[], All: []}...}
        acc3 = list(x for x in acc3) #{L:[], NL:[], All: []}
        acc3All = [d['All'] for d in acc3 if 'All' in d]
        acc3L =  [d['L'] for d in acc3 if 'L' in d]
        acc3NL = [d['NL'] for d in acc3 if 'NL' in d]
        acc3All = [item for sublist in acc3All for item in sublist]
        acc3NL = [item for sublist in acc3NL for item in sublist]
        acc3L = [item for sublist in acc3L for item in sublist]

        accsbyLev = {2: acc2All, 3: acc3All}
        accsbyLevNL = {2: acc2NL, 3: acc3NL}
        accsbyLevL = {2: acc2L, 3: acc3L}
        accsAll = acc2All + acc3All
        accsAllL = acc2L + acc3L
        accsAllNL = acc2NL + acc3NL

        rts2 = list(i for i in rts[2].values()) #{1:{L:[], NL:[], All: []},2:{L:[], NL:[], All: []}...}
        rts2 = list(x for x in rts2) #{L:[], NL:[], All: []}
        rts2All = [d['All'] for d in rts2 if 'All' in d]
        rts2L = [d['L'] for d in rts2 if 'L' in d]
        rts2NL = [d['NL'] for d in rts2 if 'NL' in d]
        rts2All = [item for sublist in rts2All for item in sublist]
        rts2NL = [item for sublist in rts2NL for item in sublist]
        rts2L = [item for sublist in rts2L for item in sublist]

        rts3 = list(i for i in rts[3].values()) #{1:{L:[], NL:[], All: []},3:{L:[], NL:[], All: []}...}
        rts3 = list(x for x in rts3) #{L:[], NL:[], All: []}
        rts3All = [d['All'] for d in rts3 if 'All' in d]
        rts3L = [d['L'] for d in rts3 if 'L' in d]
        rts3NL = [d['NL'] for d in rts3 if 'NL' in d]
        rts3All = [item for sublist in rts3All for item in sublist]
        rts3NL = [item for sublist in rts3NL for item in sublist]
        rts3L = [item for sublist in rts3L for item in sublist]

        rtsbyLev = {2: rts2All, 3: rts3All}
        rtsbyLevNL = {2: rts2NL, 3: rts3NL}
        rtsbyLevL = {2: rts2L, 3: rts3L}
        rtsAll = rts2All + rts3All
        rtsAllL = rts2L + rts3L
        rtsAllNL = rts2NL + rts3NL

        if test:
            print "RTS BY LEV: ", rtsbyLev
            print "RTS BY LEV NL: ", rtsbyLevNL


        rtsCorrect2 = list(i for i in rtsCorrect[2].values()) #{1:{L:[], NL:[], All: []},2:{L:[], NL:[], All: []}...}
        rtsCorrect2 = list(x for x in rtsCorrect2) #{L:[], NL:[], All: []}
        rtsCorrect2All = [d['All'] for d in rtsCorrect2 if 'All' in d]
        rtsCorrect2L = [d['L'] for d in rtsCorrect2 if 'L' in d]
        rtsCorrect2NL = [d['NL'] for d in rtsCorrect2 if 'NL' in d]
        rtsCorrect2All = [item for sublist in rtsCorrect2All for item in sublist]
        rtsCorrect2NL = [item for sublist in rtsCorrect2NL for item in sublist]
        rtsCorrect2L = [item for sublist in rtsCorrect2L for item in sublist]

        rtsCorrect3 = list(i for i in rtsCorrect[3].values()) #{1:{L:[], NL:[], All: []},3:{L:[], NL:[], All: []}...}
        rtsCorrect3 = list(x for x in rtsCorrect3) #{L:[], NL:[], All: []}
        rtsCorrect3All = [d['All'] for d in rtsCorrect3 if 'All' in d]
        rtsCorrect3L = [d['L'] for d in rtsCorrect3 if 'L' in d]
        rtsCorrect3NL = [d['NL'] for d in rtsCorrect3 if 'NL' in d]
        rtsCorrect3All = [item for sublist in rtsCorrect3All for item in sublist]
        rtsCorrect3NL = [item for sublist in rtsCorrect3NL for item in sublist]
        rtsCorrect3L = [item for sublist in rtsCorrect3L for item in sublist]

        rtsCorrectbyLev = {2: rtsCorrect2All, 3: rtsCorrect3All}
        rtsCorrectbyLevNL = {2: rtsCorrect2NL, 3: rtsCorrect3NL}
        rtsCorrectbyLevL = {2: rtsCorrect2L, 3: rtsCorrect3L}
        rtsCorrectAll = rtsCorrect2All + rtsCorrect3All
        rtsCorrectAllL = rtsCorrect2L + rtsCorrect3L
        rtsCorrectAllNL = rtsCorrect2NL + rtsCorrect3NL

        hits2 = list(i for i in hits[2].values())
        hits2 = [item for sublist in hits2 for item in sublist]
        hits3 = list(i for i in hits[3].values())
        hits3 = [item for sublist in hits3 for item in sublist]
        hitsbyLev = {2: hits2, 3: hits3}
        hitsAll = hits2 + hits3


        eoo2 = list(i for i in eoo[2].values())
        eoo2 = [item for sublist in eoo2 for item in sublist]
        eoo3 = list(i for i in eoo[3].values())
        eoo3 = [item for sublist in eoo3 for item in sublist]
        eoosbyLev = {2: eoo2, 3: eoo3}
        eoosAll = eoo2 + eoo3

        eoc2 = list(i for i in eoc[2].values())
        eoc2 = [item for sublist in eoc2 for item in sublist]
        eoc3 = list(i for i in eoc[3].values())
        eoc3 = [item for sublist in eoc3 for item in sublist]
        eocsbyLev = {2: eoc2, 3: eoc3}
        eocsAll = eoc2 + eoc3

        lureRound2 = list(i for i in lureRound[2].values())
        lureRound2 = [item for sublist in lureRound2 for item in sublist]
        lureRound3 = list(i for i in lureRound[3].values())
        lureRound3 = [item for sublist in lureRound3 for item in sublist]
        luresbyLev = {2: lureRound2, 3: lureRound3}
        lureRoundAll = lureRound2 + lureRound3

        hits2 = list(i for i in hits[2].values())
        hits2 = [item for sublist in hits2 for item in sublist]
        hits3 = list(i for i in hits[3].values())
        hits3 = [item for sublist in hits3 for item in sublist]
        hitsbyLev = {2: hits2, 3: hits3}
        hitsAll = hits2 + hits3


    #------------------------------------------------------------------------------
        if Block and Level and Session:
            for thisLev in [2,3]:
                for thisBlock in acc[thisLev]:
                    if len(lureRound[thisLev][thisBlock])<1:
                        lureRound[thisLev][thisBlock].append('na')

        #            ['PID', 'Date', 'Session', 'Level', 'Block', 'Lure Condition',
        #
        #            'AccBlock', 'RTBlock', 'eooBlock', 'eocBlock', 'Acc Lure Block', 'RT Lure Block', 'Acc NLure Block', 'RT NLure Block',
        #
        #            'AccLev', 'RTLev', 'eooLev', 'eocLev','Acc Lure Lev', 'RT Lure Lev', 'Acc NLure Lev', 'RT NLure Lev',
        #
        #            'ACCSess', 'RT All Sess', 'eoo Sess', 'eoc Sess', 'Acc Lure Sess', 'RT Lure Sess','Acc NLure Sess', 'RT NLure Sess',])  # write headers
                    writer.writerow([pid, date[0], session, thisLev, thisBlock,
                    lureRound[thisLev][thisBlock][0],

                    np.mean(acc[thisLev][thisBlock]['All']), np.mean(rts[thisLev][thisBlock]['All']),
                    sum(eoo[thisLev][thisBlock]),sum(eoc[thisLev][thisBlock]),
                    np.mean(acc[thisLev][thisBlock]['L']), np.mean(rts[thisLev][thisBlock]['L']),
                    np.mean(acc[thisLev][thisBlock]['NL']), np.mean(rts[thisLev][thisBlock]['NL']),
                    np.mean(rtsCorrect[thisLev][thisBlock]['All']),(sum(hits[thisLev][thisBlock]) - sum(eoc[thisLev][thisBlock])),

                    np.mean(accsbyLev[thisLev]), np.mean(rtsbyLev[thisLev]),
                    sum(eoosbyLev[thisLev]), sum(eocsbyLev[thisLev]),
                    np.mean(accsbyLevL[thisLev]), np.mean(rtsbyLevL[thisLev]),
                    np.mean(accsbyLevNL[thisLev]), np.mean(rtsbyLevNL[thisLev]),
                    np.mean(rtsCorrectbyLev[thisLev]), (sum(hitsbyLev[thisLev])- sum(eocsbyLev[thisLev])),


                    np.mean(accsAll), np.mean(rtsAll), sum(eoosAll), sum(eocsAll),
                    np.mean(accsAllL),np.mean(rtsAllL),np.mean(accsAllNL),np.mean(rtsAllNL),
                    np.mean(rtsCorrectAll), (sum(hitsAll)- sum(eocsAll))
                    ])
        # elif Level and Session:
        #     for thisLev in [2,3]:
        #         for thisBlock in acc[thisLev]:
        #             if len(lureRound[thisLev][thisBlock])<1:
        #                 lureRound[thisLev][thisBlock].append('na')
        #
        # #            ['PID', 'Date', 'Session', 'Level', 'Block', 'Lure Condition',
        # #
        # #            'AccBlock', 'RTBlock', 'eooBlock', 'eocBlock', 'Acc Lure Block', 'RT Lure Block', 'Acc NLure Block', 'RT NLure Block',
        # #
        # #            'AccLev', 'RTLev', 'eooLev', 'eocLev','Acc Lure Lev', 'RT Lure Lev', 'Acc NLure Lev', 'RT NLure Lev',
        # #
        # #            'ACCSess', 'RT All Sess', 'eoo Sess', 'eoc Sess', 'Acc Lure Sess', 'RT Lure Sess','Acc NLure Sess', 'RT NLure Sess',])  # write headers
        #             writer.writerow([pid, date[0], session, thisLev, thisBlock,
        #             lureRound[thisLev][thisBlock][0],
        #
        #             np.mean(acc[thisLev][thisBlock]['All']), np.mean(rts[thisLev][thisBlock]['All']),
        #             sum(eoo[thisLev][thisBlock]),sum(eoc[thisLev][thisBlock]),
        #             np.mean(acc[thisLev][thisBlock]['L']), np.mean(rts[thisLev][thisBlock]['L']),
        #             np.mean(acc[thisLev][thisBlock]['NL']), np.mean(rts[thisLev][thisBlock]['NL']),
        #             np.mean(rtsCorrect[thisLev][thisBlock]['All']),(sum(hits[thisLev][thisBlock]) - sum(eoc[thisLev][thisBlock])),
        #
        #             np.mean(accsbyLev[thisLev]), np.mean(rtsbyLev[thisLev]),
        #             sum(eoosbyLev[thisLev]), sum(eocsbyLev[thisLev]),
        #             np.mean(accsbyLevL[thisLev]), np.mean(rtsbyLevL[thisLev]),
        #             np.mean(accsbyLevNL[thisLev]), np.mean(rtsbyLevNL[thisLev]),
        #             np.mean(rtsCorrectbyLev[thisLev]), (sum(hitsbyLev[thisLev])- sum(eocsbyLev[thisLev])),
        #
        #
        #             np.mean(accsAll), np.mean(rtsAll), sum(eoosAll), sum(eocsAll),
        #             np.mean(accsAllL),np.mean(rtsAllL),np.mean(accsAllNL),np.mean(rtsAllNL),
        #             np.mean(rtsCorrectAll), (sum(hitsAll)- sum(eocsAll))
        #             ])
NBackWithLures()
