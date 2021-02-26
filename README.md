# Distro_Auto_Update

This is a program to automatically update local git repos and also push updates to the remote master. I created this to solve several problems at once. First, the folder that I use to store all of my working code is not the same folder I use to store my repos. Second, some of the code in my working folder also exists in repos but will never be updated there because I'm lazy and I don't need them to be udpated currently. Third, my github update rate is abysmal because it's unnecessarily effortful to do pushes on a git by git basis. 

To run, you'll need to do 2 things first: 

First, run `git config --global credential.helper store` from cmd/ gitbash to store your username and password. 

Second, on lines 105 and 106 of the project, update with the filepath of your working folder and the top level directory all of your repos are stored in. 

Afterwords, you can run from cmd like `python githubupdater.py`

This program runs in phases. They are as follows. 

Phase 1) Collect data from main programming folder, including filename and date last modified. 

#Subset that data based on date last modified to only keep recents.  - Deprecated

Phase 2) iterate over the folders and files from some root directory, if the file is on the list, overwrite local copy with version from programming folder if and only if it isn't a later version. 

Phase 3) Go over each repo, commit with a procedurally generated comment and push. 

#check for updates - Deprecated in favor of passing the directories as var

Frequency for this running will be once daily. You can put this on a clock with the standard `time`/ `datetime` wrapper. 
