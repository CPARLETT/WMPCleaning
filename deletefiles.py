import glob,os, shutil

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
    else:
        os.mkdir(cleanFolder)
        shutil.copy(cleanFile,cleanFolder)
        print "moved " + cleanFile
    questionsFolder = CurrDir + '\\Questions'
    questionsFile = participant + '_questions.csv'
    if os.path.exists(questionsFolder):
        if os.path.exists(questionsFolder + "\\" + questionsFile):
            continue
        else:
            shutil.copy(questionsFile,questionsFolder)
            print "moved " + questionsFile
    else:
        os.mkdir(questionsFolder)
        shutil.copy(questionsFile,questionsFolder)
        print "moved " + questionsFile
