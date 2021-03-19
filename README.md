## The purpose of this project is as follows:
This is a program to automatically update local git repos and also push updates to the remote master. I created this to solve several problems at once. First, the folder that I use to store all of my working code is not the same folder I use to store my repos. Second, some of the code in my working folder also exists in repos but will never be updated there because I'm lazy and I don't need them to be udpated currently. Third, my github update rate is abysmal because it's unnecessarily effortful to do pushes on a git by git basis. 
## Here's some back story on why I needed to build this:
This project came about as a result of needing to update multiple git repositories very frequently and easily. A fundamental character trait of programmers is laziness.
## This project uses only python built-in functions and data types.

## In order to use this, you'll first need do the following:
First, run `git config --global credential.helper store` from cmd/ gitbash to store your username and password. 
## The expected frequency for running this code is as follows:
As Needed