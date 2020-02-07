# Dynamic query in application

### Potential String Injection

"select * from users where name = '" + userName + "'";

###  

### Potential Numeric Injection

"select * from users where employee_id = " + userID;

##  

## Attacker supplies unexpected text

- userName = **Smith' or     '1'='1**
- userName =**' or 1=1 --**
- userID = **1234567 or     1=1**
- UserName = **Smith’;drop     table users; truncate audit_log;--**

##  

## Application executes query

- select * from users where     name = **'Smith' or '1' = '1'**

- - select * from users where      name = **'Smith' or TRUE**

- select * from users where     employee_id = 1234567 or 1=1

 

**All records are returned from database**

 

 

## Special Characters

/* */     are inline comments
 -- , #      are line comments

Example: Select * from users where name = 'admin' --and pass = 'pass'

 

;    allows query chaining

Example: Select * from users; drop table users;

 

',+,||     allows string concatenation
 Char()     strings without quotes

Example: Select * from users where name = '+char(27) or 1=1

##  

## Special Statements

Unions allows overlapping of database tables 'Select id, text from news union all select name, pass from users'

Joins allows connecting to other tables

 

 

 

# Defences against SQL injection

- Parameterized Queries
- Stored Procedures
- Use Encoders (owasp esAPI)

 

For non-SQL injections, encoding is required.