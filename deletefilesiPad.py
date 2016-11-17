import glob,os, shutil

outputName = ''
CurrDir = os.getcwd()
print "You're in " + CurrDir

print "__________________"
folders = glob.glob('[0-9][0-9][0-9]') + glob.glob('SP[0-9][0-9][0-9]')


for participant in folders:
    os.chdir(CurrDir)
    print "Moving and Deleting files for participant " + participant
    path = CurrDir + "\\" + participant
    os.chdir(path)
    print "Changing to: " + os.getcwd()
    fn = glob.glob('clean')
    print "deleted "
    for x in fn:
        shutil.rmtree(x)
    filesToDel = glob.glob('*.csv')
    for x in filesToDel:
        os.remove(x)
