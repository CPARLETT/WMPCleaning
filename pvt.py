import re, csv,os, os.path
import glob

name = 'NewHorizonScores.csv'
filenames = glob.glob('*.csv')
for f in filenames:
    pid = ''
    pacc = []
    rta = []
    print f#for checking purposes, prints file it's processing into terminal
    reader = csv.reader(open(f, 'rb'))
    if os.path.exists(name):
        writer = csv.writer(open( name ,'ab'))
    else:
        writer = csv.writer(open( name ,'wb'))
        writer.writerow(['pid','session', 'age', 'acc', 'rtavge','basal', 'ceiling', 'bilingual'])

    for row in reader:
        if row[0] == 'task':
            continue
        if len(row) < 4:
            if row[0]== 'basal:':
                basal = row[1]
            elif row[0]== 'ceiling:':
                ceiling = row[1]
            elif row[0] == 'bilingual score:':
                bilingual = row[1]
        else:
            pid = int(row[1])
            session = int(row[2])
            age = int(row[3])
            if row[6] == 'TRUE':
                continue
            else:
                if row[11] == '':
                    continue
                else:
                    acc = int(row[11])
                    if acc == -1:
                        continue
                    else:
                        pacc.append(acc)
                        rt = float(row[12])
                        rta.append(rt)
    if pid == '':
        continue
    s = sum(pacc)
    try:
        reactiontimeaverage = (sum(rta)/len(rta))
    except:
        reactiontimeaverage = 'something is wrong with this file'
    writer.writerow([pid, session, age, s, reactiontimeaverage, basal, ceiling, bilingual])
