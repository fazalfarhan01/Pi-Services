#!/bin/bash

Black='\033[0;30m'
Red='\033[0;31m'
Green='\033[0;32m'
Brown_Orange='\033[0;33m'
Blue='\033[0;34m'
Purple='\033[0;35m'
Cyan='\033[0;36m'
Light_Gray='\033[0;37m'
Dark_Gray='\033[1;30m'
Light_Red='\033[1;31m'
Light_Green='\033[1;32m'
Yellow='\033[1;33m'
Light_Blue='\033[1;34m'
Light_Purple='\033[1;35m'
Light_Cyan='\033[1;36m'
White='\033[1;37m'
NC='\033[0m' # No Color

web=/var/www/ftm.ddns.net/wp-content/uploads/static-html-output/
now="$(date +%B) $(date +%d) $(date +%Y) $(date +%T)"
commit_message="Adding Files on $now"

printf "\n${Yellow}INFO: ${Cyan}Static HTML Output Directory: ${Light_Purple}$web\n"
printf "${Yellow}INFO: ${Cyan}Starting Static Site Generation..!!\n${NC}"

# Generate Static Site
sudo wp statichtmloutput generate --path=/var/www/ftm.ddns.net --allow-root

printf "${Yellow}INFO: ${Cyan}Static Site Generation Completed..!!\n"
cd $web
printf "${Yellow}INFO: ${Cyan}Current Working Directory: ${Light_Purple}$web\n"

# Generating XML Sitemaps from website
./ExtractAndReplaceXML.py

# Show git status
git status >> /var/www/ftm.ddns.net/generate.log

printf "${Yellow}INFO: ${Cyan}Staging the changes..!!\n"
# Adding changes in directory to git
git add . >> /var/www/ftm.ddns.net/generate.log

printf "${Yellow}INFO: ${Cyan}Commiting changes to git repo..!!\n"
printf "${Yellow}INFO: ${Cyan}Commit Message: ${Light_Purple}'$commit_message'\n"
# Commit the newly generated files
git commit -m "$commit_message" >> /var/www/ftm.ddns.net/generate.log

printf "${Yellow}INFO: ${Cyan}Pulling from remote repo..!!\n"
# Pull from remote repo
git pull origin master >> /var/www/ftm.ddns.net/generate.log

printf "${Yellow}INFO: ${Cyan}Pushing to remote repo..!!\n"
# Push to remote repo
git push -u origin master >> /var/www/ftm.ddns.net/generate.log

printf "${Green}******************************EXPORTED******************************\n"