#Step 1: From your project repository, check out a new branch and test the changes.

git checkout -b revence27-master master && 
git pull https://github.com/revence27/iminsi-gihumbi.git master && 

git checkout master &&
git merge --no-ff revence27-master && 

git checkout -b watshisface  master &&
git pull https://github.com/watshisface/iminsi-gihumbi.git master && 

git checkout master &&
git merge --no-ff watshisface 

#Step 2: Merge the changes and update on GitHub.


git push origin master

### AS this merge has a commit sha, you revert it and go back previous status before merge
### example

git revert -m 1 b3db4a22c142c4e322fe7e58688c525930b0baa4 / 016b47e933263823e53cc4512d70e3ad9542fdc7


