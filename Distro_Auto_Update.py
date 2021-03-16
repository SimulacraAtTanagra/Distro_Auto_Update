import os
import pathlib
from datetime import datetime as dt2
import shutil
from git import Repo
from repo_helper import repo_update


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
def update_main(foldername,filename):
    with open(os.path.join(foldername,filename),'r') as f:
        lines=f.readlines()
    files=os.listdir(os.path.join(foldername,"src"))
    files=[file[:-3] for file in files if '.py' in file]
    for ix, line in enumerate(lines):
        if ix<40:
            for x in [segment for segment in line.split() if segment in files]:
                line=line.replace(f'import {x}',f'import src.{x}')
                line=line.replace(f'from {x}',f'from src.{x}')
                lines[ix]=line
    with open(os.path.join(foldername,filename),'w') as f:
        f.writelines(lines)               
#TODO build anonymizer function to strip out sensitive information, call here
def mass_swap(start,replacer,timedict): #gathering data from each subdirectory
    replacelist=[]
    for root, dirs, files in os.walk(start):
        for file in files:
            if replacer(root,file,timedict):
                replacelist.append((os.path.join(root,file),os.fsdecode(file)))
                filename=os.fsdecode(file)[:-3]
                if filename in dirs:
                     update_main(os.path.join(root,filename),os.fsdecode(file))
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
    
def general_update(repofolder):                                                                                                      
    subdirs = [x[0] for x in os.walk(repofolder) if "src" not in x[0] and "git" not in x[0]]          
    msg="Daily automated update"
    for foldername in subdirs:
        repo_update(os.path.abspath(foldername),message=msg)
        
        #TODO something in this step needs to account for removal of files
        #not just addition. Removal from src based on absence in the code
        
def readme_correct(repofolder): #single use function to repair readmes written previously
    subdirs = [x[0] for x in os.walk(repofolder) if "src" not in x[0] and "git" not in x[0]]          
    #msg="Daily automated update"
    for foldername in subdirs:
        if 'README.md' in os.listdir(foldername):
            filename=os.path.join(foldername,'README.md')
            with open(filename,'r') as f:
                xyz=f.readlines()
            xyz=[x.replace("##",'## ').replace('##  ','## ') for x in xyz]
            with open(filename,'w') as f:
                f.writelines(xyz)
        
#TODO create audit tool to fix src if code drops a local file call + delete src if empty
def main():
    infolder=r'C:\Users\shane\Desktop\Projects\Programs'   #this is the folder containing the working code
    outfolder=r'C:\Users\shane\Desktop\Programming'  #this is the project folder to be updated and pushed
    phase3(infolder,outfolder)
    general_update(outfolder)
    
    
if __name__=="__main__":
    main()