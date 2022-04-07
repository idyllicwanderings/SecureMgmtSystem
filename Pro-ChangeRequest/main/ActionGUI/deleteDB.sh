PROJECTNAME="${1}"

mysqladmin -uroot -pactiongui -h mysql -P 3306 drop ${PROJECTNAME}