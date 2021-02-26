import os
import pathlib
from datetime import datetime as dt2
import shutil
from git import Repo


def last_modified(fname):   #getting the date last modified
    fname=pathlib.Path(fname)
    mtime = dt2.fromtimestamp(fname.stat().st_mtime)
    return(mtime)
    
def package(folder,file):  #to create dict obj
    x=os.fsdecode(file)
    #list including full path,filename, and last modified datetime
    y=[os.path.join(folder,os.fsdecode(file)),os.fsdecode(file),last_modified(os.path.join(folder,os.fsdecode(file)))]
    return(x,y)
    
def get_data(folder):   #create a hash table with all of the names and times
    files=os.listdir(os.fsencode(folder))
    timedict={}
    for file in files:
        #base filename as primary key in table
        x,y=package(folder,file)
        if 'main' not in x.lower():
            timedict.update({x:y})
    return(timedict)

def phase1(infolder):   #grabbing data
    timedict=get_data(infolder)
    return(timedict)    #spitting out result
    
def compare_files(source, satellite): #checking the work file against stored
    if source[2]>satellite[2]:  #if source is newer...
        print(f'{satellite[1]} overwritten!')
        return(replace_files(satellite[0],source[0]))   #overwrite the satellite

def pathparent(filepath):   #takes filepath as str and returns parent path
    pathobj=pathlib.Path(filepath)
    return(pathobj.parent)
        

def replace_files(replacement,original):    #a function for replacing files
    #moving and replacing the original with the replacement
    shutil.copy(original, pathparent(replacement))
    return(True)
    
def replacer(folder,fname,timedict):
    x,y=package(folder,fname)
    if x in timedict.keys():
        try:
            z=timedict[x]
            return(compare_files(z,y))
        except Exception as e:
            print(fname,e)
            

def mass_swap(start,replacer,timedict): #gathering data from each subdirectory
    replacelist=[]
    for root, dirs, files in os.walk(start):
        for file in files:
            if replacer(root,file,timedict):
                replacelist.append((os.path.join(root,file),os.fsdecode(file)))
                #trying to get this thing to save the file location to a list so we can update from there
    replacelist=[(pathparent(x[0]),x[1]) for x in replacelist]
    return(replacelist)
    
def phase2(infolder,outfolder):   
    timedict=phase1(infolder)
    replacelist=mass_swap(outfolder,replacer,timedict)
    return(replacelist)
    
def gitverify(folder):  #if we update an src file, I want it to know to update the main
    if '.git' in os.listdir(folder):
        return(folder)
    elif '.git' in os.listdir(folder.parent):
        return(folder.parent)
    elif '.git' in os.listdir(folder.parent.parent):
        return(folder.parent.parent)
    else:
        print(f'Somehow you used an unreasonable amount of nesting in {folder} boss.')

def git_push(PATH_OF_GIT_REPO,COMMIT_MESSAGE ):
    try:
        repo = Repo(PATH_OF_GIT_REPO)
        repo.git.add(update=True)
        repo.index.commit(COMMIT_MESSAGE)
        origin = repo.remote(name='origin')
        origin.push()
    except Exception as e:
        print('Some error occured while pushing the code')    
        print(e)

def phase3(infolder,outfolder):
    #feeding the upstream functions and generating the list for git pushes. 
    replacelist=phase2(infolder,outfolder)   
    #ensuring that the folders in the list are top level repos
    replacelist=[(gitverify(i[0]),i[1]) for i in replacelist] 
    #pushing
    for i in replacelist:
        message=f'updated {i[1]}'
        git_push(i[0],message)
    
    
def main():
    infolder=r'C:\Users\shane\Desktop\Projects\Programs'   #this is the folder containing the working code
    outfolder=r'C:\Users\shane\Desktop\Programming'  #this is the project folder to be updated and pushed
    phase3(infolder,outfolder)
    
if __name__=="__main__":
    main()