#Written by Chelsea Parlett (2016) for the Working Memory and Plasticity lab and
#collaborators. For questions email cparlett@uci.edu


import re, csv,os, os.path
import glob
import shutil
import numpy as np

__all__ = ["addSession", "pullQuestions", "MQAuto", "KBAuto", "deletefiles"]
#This program will pull all the files from a folder that are .csv and it just sorts them and then adds a session number--CP
def addSession(Game='MQ', participantidtype='[0-9][0-9][0-9]'):
    CurrDir = os.getcwd()
    print "You're in " + CurrDir

    print "__________________"
    folders = glob.glob(participantidtype)

    for participant in folders:
        path = CurrDir + "\\" + participant
        os.chdir(path)
        print "Changing to: " + os.getcwd()
        lookFor = participantidtype + '---*.csv'
        filenames = glob.glob(lookFor)
        new = sorted(filenames)#will sort
        i=1
        for f in new:
            # print f#for checking purposes, prints file it's processing into terminal
            # print i
            if Game == 'KB':
                delim = ';'
            else:
                delim = ','
            reader = csv.reader(open(f, 'rU'), delimiter = delim)
            name = str(i)+ '_' + f
            writer = csv.writer(open( name ,'wb'))
            for row in reader:
                if len(row)<15:
                    writer.writerow([row[0],row[1],row[2],row[3],str(i)])#the last 4 rows, just put them back
                else:
                    if row[0]=="Participant ID":
                        if Game == 'KB':
                            writer.writerow([row[0],row[1],row[2],row[3],row[4],row[5],
                            row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],
                            row[14],row[15],row[16], "Session"])#header Row
                        else:
                            writer.writerow([row[0],row[1],row[2],row[3],row[4],row[5],
                            row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],
                            row[14],row[15],row[16],row[17],row[18],row[19],row[20],
                            row[21],row[22],row[23],row[24],row[25],row[26], row[27],
                            row[28], "Session"])#header Row
                    else:
                        if Game == 'KB':
                            writer.writerow([row[0],row[1], row[2],row[3],row[4],row[5],
                            row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],
                            row[14],row[15],row[16],str(i)])#add session number
                        else:
                            writer.writerow([row[0],row[1], row[2],row[3],row[4],row[5],
                            row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],
                            row[14],row[15],row[16],row[17],row[18],row[19],row[20],row[21],
                            row[22],row[23],row[24],row[25],row[26],row[27],row[28],str(i)])#add session number
            i += 1 #next session
        os.chdir(CurrDir)
def pullQuestions(participantidtype='[0-9][0-9][0-9]'):
    #this will pull their responses from the files and put them in one place--CP
    CurrDir = os.getcwd()
    print "You're in " + CurrDir

    print "__________________"

    folders = glob.glob('[0-9][0-9][0-9]')

    # print folders

    for participant in folders:
        path = CurrDir + "\\" + participant
        os.chdir(path)
        print "Changing to: " + os.getcwd()

        filenames = glob.glob('[0-9]_*.csv')
        print filenames

        for f in filenames:
            # print f#for checking purposes, prints file it's processing into terminal
            reader = csv.reader(open(f, 'rb'))
            pidsearch= '[0-9]_(' + participantidtype + ')---'
            pid = re.findall(pidsearch, f)
            if len(pid)>0:
                name = pid[0] + '_'+ 'questions.csv'
            else:
                break
            if os.path.exists(name):
                writer = csv.writer(open(name,'ab'),delimiter = ',')
            else:
                writer = csv.writer(open( name ,'wb'))
                writer.writerow(['PID', 'Question', 'Score','Date','Session'])
            for row in reader:
                getRidofSpaces = list(r for r in row if r != '')
                if len(getRidofSpaces)<6 and row[1]!= "Practice round for level: " and row[1]!="Round":
                    writer.writerow(getRidofSpaces)#the last 4 rows, just put them back
    os.chdir(CurrDir)
def MQAuto(): #works for all Match Quest Style files
    #REGEX to find PID
    CurrDir = os.getcwd()
    print "You're in " + CurrDir

    print "__________________"
    folders = glob.glob('[0-9][0-9][0-9]')

    for participant in folders:

        rtsAll = []
        path = CurrDir + "\\" + participant
        os.chdir(path)
        print "Changing to: " + os.getcwd()

        print "STARTED"
        fn = glob.glob('[0-9][0-9]_*.csv')
        filenames = fn + glob.glob('[0-9]_*.csv')
        for name in filenames: #each session

            reader = csv.reader(open(name, 'rU'))  # open reader
            pid = re.findall('[0-9]+_([a-zA-Z0-9]+)---', name)  # find PID
            session = re.findall('([0-9]+)_[a-zA-Z0-9]+---', name) #find Session number
            print "Doing Session: " + str(session)
            if len(pid) < 1:
                break
            outputName = pid[0] + "_" + "clean.csv"
            toWrite = []

            rtsAll = []
            accsAll = []
            rtsL = []
            rtsNL = []
            accsL= []
            accsNL = []
            levelsBySession = []


            reaction = {1:{0:[], 1:[], 2:[], 3:[], 13:[]}, 2:{0:[], 1:[], 2:[], 3:[], 13:[]},
            3:{0:[], 1:[], 2:[], 3:[] , 13:[]}, 4:{0:[], 1:[], 2:[], 3:[], 13:[]},
             5:{0:[], 1:[], 2:[], 3:[], 13:[]}, 6:{0:[], 1:[], 2:[], 3:[], 13:[]},
              7:{0:[], 1:[], 2:[], 3:[], 13:[]}, 8:{0:[], 1:[], 2:[], 3:[], 13:[]},
               9:{0:[], 1:[], 2:[], 3:[], 13:[]} , 10:{0:[], 1:[], 2:[], 3:[], 13:[]}}
            acc = {1:{0:[], 1:[], 2:[], 3:[], 13:[]}, 2:{0:[], 1:[], 2:[], 3:[], 13:[]},
            3:{0:[], 1:[], 2:[], 3:[] , 13:[]}, 4:{0:[], 1:[], 2:[], 3:[], 13:[]},
             5:{0:[], 1:[], 2:[], 3:[], 13:[]}, 6:{0:[], 1:[], 2:[], 3:[], 13:[]},
              7:{0:[], 1:[], 2:[], 3:[], 13:[]}, 8:{0:[], 1:[], 2:[], 3:[], 13:[]},
               9:{0:[], 1:[], 2:[], 3:[], 13:[]} , 10:{0:[], 1:[], 2:[], 3:[], 13:[]}}
            counts = {
            1:{'eoo': 0, 'eoc': 0, 'tresp': 0, 'level': [], 'tacc': [], 'trt': []},
            2:{'eoo': 0, 'eoc': 0, 'tresp': 0, 'level': [], 'tacc': [], 'trt': []},
            3:{'eoo': 0, 'eoc': 0, 'tresp': 0, 'level': [], 'tacc': [], 'trt': []},
            4:{'eoo': 0, 'eoc': 0, 'tresp': 0, 'level': [], 'tacc': [], 'trt': []},
            5:{'eoo': 0, 'eoc': 0, 'tresp': 0, 'level': [], 'tacc': [], 'trt': []},
            6:{'eoo': 0, 'eoc': 0, 'tresp': 0, 'level': [], 'tacc': [], 'trt': []},
            7:{'eoo': 0, 'eoc': 0, 'tresp': 0, 'level': [], 'tacc': [], 'trt': []},
            8:{'eoo': 0, 'eoc': 0, 'tresp': 0, 'level': [], 'tacc': [], 'trt': []},
            9:{'eoo': 0, 'eoc': 0, 'tresp': 0, 'level': [], 'tacc': [], 'trt': []},
            10:{'eoo': 0, 'eoc': 0, 'tresp': 0, 'level': [], 'tacc': [], 'trt': []}
            }

            if os.path.exists(outputName):
                writer = csv.writer(open(outputName, 'ab'))  # open filewriter
            else:
                writer = csv.writer(open(outputName, 'wb'))
                writer.writerow(
                    ['PID', 'Session', 'Round', 'Avg ACC', 'Avg RT', 'Avg Lvl', 'Total Responses', '#EOO', '#EOC', 'ACC Lure',
                     'ACC NLure', 'RT Lure', 'RT NLure', 'Overall Acc', 'Overall Lure Acc',
                      'Overall NLure Acc', 'Overall RT', 'Overall Lure RT', 'Overall NLure RT', 'Mean Level for Session'])  # write headers


            for row in reader: #get info from each file
                if row[0] == 'Game Name' or len([t for t in row if len(t) > 0]) < 10: #Check if header or if row is short (practice or Qs)
                    continue
                # print row[5]

                rnd = int(row[2])
                lvl = int(row[5])
                # print lvl
                luretype = int(row[7])
                # print luretype
                # print row[9]
                if row[9]!= '':
                    rt = int(row[9])
                accuracy = int(row[10])
                pr = row[8]
                # nbacktype = row[17]
                if row[9]!= '':
                    reaction[rnd][luretype].append(rt)  # {0: [0,0,0,1,0,1,1,0]}
                    rtsAll.append(rt)
                acc[rnd][luretype].append(accuracy) # {0: [0,0,0,1,0,1,1,0]}
                accsAll.append(accuracy)

                if accuracy == 0:
                    if pr == 'tapped screen':
                        counts[rnd]['eoc'] += 1
                    elif pr == 'no tap':
                        counts[rnd]['eoo'] += 1

                if pr == 'tapped screen':
                    counts[rnd]['tresp'] += 1

                counts[rnd]['level'].append(lvl)
                levelsBySession.append(lvl)
                counts[rnd]['tacc'].append(accuracy)
                if row[9]!= '':
                    counts[rnd]['trt'].append(rt)
            for x in range(1,11): #for each round
                if x == 0:
                    print "OH NO"


                fullListNLacc1 = list(item for item in acc[x][0])
                fullListNLacc2 = list(item for item in acc[x][1])
                fullListNLacc3 = list(item for item in acc[x][13])

                fullListNLacc = fullListNLacc1 + fullListNLacc2 + fullListNLacc3

                fullListLacc1 = list(item for item in acc[x][2])
                fullListLacc2 = list(item for item in acc[x][3])

                fullListLacc = fullListLacc1 + fullListLacc2

                accsAll = accsAll + fullListNLacc# add all ACCs
                accsAll += fullListLacc #add all ACCs
                accsL +=  fullListLacc#add L ACC to L
                accsNL += fullListNLacc #add NL ACCs to NL

                accl = np.mean(fullListLacc)
                accnl = np.mean(fullListNLacc)



                fullListNLrt1 = list(item for item in reaction[x][0])
                fullListNLrt2 = list(item for item in reaction[x][1])
                fullListNLrt3 = list(item for item in reaction[x][13])

                fullListNLrt = fullListNLrt1 + fullListNLrt2 + fullListNLrt3

                fullListLrt1 = list(item for item in reaction[x][2])
                fullListLrt2 = list(item for item in reaction[x][3])

                fullListLrt = fullListLrt1 + fullListLrt2

                rtsAll +=  fullListNLrt# add all ACCs
                rtsAll += fullListLrt #add all ACCs
                rtsL += fullListLrt#add L ACC to L
                rtsNL += fullListNLrt #add NL ACCs to NL

                rtl = np.mean(fullListLrt)
                rtnl = np.mean(fullListNLrt)


                toWrite.append([pid[0], session[0], x, np.mean(counts[x]['tacc']), np.mean(counts[x]['trt']),
                np.mean(counts[x]['level']),counts[x]['tresp'], counts[x]['eoo'], counts[x]['eoc'],
                accl, accnl, rtl, rtnl,])
            print "____________________________________"
            print "____________________________________"
            print levelsBySession
            for thing in toWrite:
                thing += [np.mean(accsAll), np.mean(accsL), np.mean(accsNL), np.mean(rtsAll), np.mean(rtsL), np.mean(rtsNL), np.mean(levelsBySession)]
                # print 'done adding'
            for row in toWrite:
                writer.writerow(row)
                # print 'done writing'
        os.chdir(CurrDir)
def KBAuto():
    #REGEX to find PID
    CurrDir = os.getcwd()
    print "You're in " + CurrDir

    print "__________________"
    folders = glob.glob('[0-9][0-9][0-9]')

    for participant in folders:

        toWrite = []

        rtsAll = []
        path = CurrDir + "\\" + participant
        os.chdir(path)
        print "Changing to: " + os.getcwd()

        print "STARTED"
        fn = glob.glob('[0-9][0-9]_*.csv')
        filenames = fn + glob.glob('[0-9]_*.csv')
        # print filenames
        print "______________________________________________" # find all the csv files
        for name in filenames: #session
            print "Working on " + name
            reader = csv.reader(open(name, 'rb'))  # open reader
            pid = re.findall('[0-9]*_([a-zA-Z0-9]+)---', name)  # find PID
            session = re.findall('([0-9]*)_[a-zA-Z0-9]+---', name) #find Session number

            outputName = pid[0] + "_" + "clean.csv"

            reactionALL = []
            accuracyALL = []
            reaction = {1:[],2:[],3:[],4:[],5:[],6:[],7:[], 8:[], 9:[], 10:[]}
            acc = {1:[],2:[],3:[],4:[],5:[],6:[],7:[], 8:[], 9:[], 10:[]}
            level = {1:[],2:[],3:[],4:[],5:[],6:[],7:[], 8:[], 9:[], 10:[]}
            if os.path.exists(outputName):
                writer = csv.writer(open(outputName, 'ab'))  # open filewriter
            else:
                writer = csv.writer(open(outputName, 'wb'))
                writer.writerow(
                    ['PID', 'Session', 'Round', 'Avg ACC', 'Avg RT', 'Avg Lvl', 'Session Avg RT', 'Session Avg Acc'])  # write headers


            for row in reader:
                if row[0] == 'Subject' or len([t for t in row if len(t) > 0]) < 10: #Check if header or if row is short (practice or Qs)
                    continue
                rnd = int(row[1])
                lvl = int(row[3])
                if row[8] != '':
                    if row[8] == 'x' or row[8] == 's' or row[8] == 'k' or row[8] == 'm':
                        rt = float(row[9])
                        accuracy = int(row[10])
                    else:
                        rt = float(row[8])
                        reaction[rnd].append(rt)
                        reactionALL.append(rt)
                        accuracy = int(row[9])
                acc[rnd].append(accuracy)
                accuracyALL.append(accuracy)
                level[rnd].append(lvl)


            for rnd in range(1,11):
                writer.writerow([pid[0], session[0], rnd, np.mean(acc[rnd]), np.mean(reaction[rnd]),
                np.mean(level[rnd]), np.mean(reactionALL), np.mean(accuracyALL)])
    os.chdir(CurrDir)
def deletefiles():
    outputName = ''
    CurrDir = os.getcwd()
    print "You're in " + CurrDir

    print "__________________"
    folders = glob.glob('[0-9][0-9][0-9]')

    for participant in folders:
        print "Moving and Deleting files for participant " + participant
        path = CurrDir + "\\" + participant
        os.chdir(path)
        print "Changing to: " + os.getcwd()
        fn = glob.glob('[0-9][0-9]_*.csv')
        filenames = fn + glob.glob('[0-9]_*.csv')  # find all the csv files
        for name in filenames:
            print "deleted " + name
            os.remove(name)
        cleanFolder = CurrDir + '\\Clean'
        cleanFile = participant + '_clean.csv'
        if os.path.exists(cleanFolder):
            if os.path.exists(cleanFolder + "\\" + cleanFile):
                print cleanFile + " exists"
                continue
            else:
                shutil.copy(cleanFile,cleanFolder)
                print "moved " + cleanFile
                os.remove(cleanFile)
        else:
            os.mkdir(cleanFolder)
            shutil.copy(cleanFile,cleanFolder)
            print "moved " + cleanFile
            os.remove(cleanFile)
        questionsFolder = CurrDir + '\\Questions'
        questionsFile = participant + '_questions.csv'
        if os.path.exists(questionsFolder):
            if os.path.exists(questionsFolder + "\\" + questionsFile):
                continue
            else:
                shutil.copy(questionsFile,questionsFolder)
                print "moved " + questionsFile
                os.remove(questionsFile)
        else:
            os.mkdir(questionsFolder)
            shutil.copy(questionsFile,questionsFolder)
            print "moved " + questionsFile
            os.remove(questionsFile)
    os.chdir(CurrDir)
