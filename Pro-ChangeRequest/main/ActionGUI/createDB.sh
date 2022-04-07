PROJECTNAME="${1}"

cat /usr/local/actiongui/${PROJECTNAME}/vm/target/generated-sources/sql/db.sql | mysql -u'root' -p'actiongui' -h mysql -P 3306