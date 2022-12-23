# WEB APPLICATION For "Gym Managment System"

Everything that takes places Everything that takes place in the gym will be automated by the GYM MANAGEMENT SYSTEM. All people who work at the gym, train there, and who run the gym are doing it to help and make their jobs easier. The database includes every person's contact information, personal information, daily goals, metrics of their successes and growth, training plans the gym offers, equipment, etc.

## CONTRIBUTORS
@Shameem Mujawar: 10623068
@Akshay Shishupal: 10616829
@Sri Chandana: 10616015
@ Shivraj Baladi: 10617278

## TECHNOLOGIES USED

 - Front end
	- HTML
	- JavaScript 
	
 - Middleware
	- Python
		- flask
		- flask session 
 - Backend
	- My SQL DBMS

## TECHNICAL DESCRIPTION 
Below python libraries are used in this app. 

- flask 
- flask_mysqldb 
- wtforms 
- wtforms.fields
- passlib.hash 
- flask_script
- functools 
- datetime 

Below is the command to install a python library 

pip install [library_name]

## Requirements for running application:

my SQL database: we need to have mysql database. the database name is gym, if not then please create datebase with this given name.

This system needs one bootstrap admin user to be present. To add the admin user, use below command

INSERT INTO info(username, password, street, city, phone, name, prof) VALUES('shameem_23', '$5$rounds=535000$6gsmZKME5DrojTtI$8WcFkNyq0vGAh7M2splCCf6ZSVDcG3xOEDWP5XBRNL2', 'castle house', 'dublin 1', '0123456789', 'Shameem Mujawar', 1);

To run the app, navigate to root directory and enter below command. 

flask --app app run 

Once app opens (usually open run on 127.0.0.1:5000 given that user does not change port), user will land on login page. 

Enter below credentials to login as admin user. 

username - shameem_23
password - eswar@259522

Once logged in, first you need to add trainer user and plan. If not added, while adding member, you wont see any plan. 

This system provides dashboard for receptionist which has functionalities like add member ,delete member and view details of existing members using the below commands.

CREATE TABLE members(username VARCHAR(200), plan VARCHAR(100), trainor VARCHAR(200), PRIMARY KEY(username), FOREIGN KEY(username) references info(username), FOREIGN KEY(plan) references plans(name), FOREIGN KEY(trainor) references trainors(username));

INSERT INTO members(username, plan, trainor) VALUES(%s, %s, %s)", (username, plan, trainor)

DELETE FROM members WHERE username = %s", [username]

SELECT username FROM info WHERE username != %s", [session['username']]























}

### App.py
	========================================================================================================================================================
	| APIs                                                         | Navigations                | Action -Performed
	========================================================================================================================================================
	| /                                                            | home.html                  | this will open homepage of application
	--------------------------------------------------------------------------------------------------------------------------------------------------------
	| /login', methods = ['GET', 'POST']                           | login.html                 | This will navigate to login page of application
	--------------------------------------------------------------------------------------------------------------------------------------------------------
	| /update_password/<string:username>', methods = ['GET', 'POST'] | updatePassword.html      | it will update the password
	--------------------------------------------------------------------------------------------------------------------------------------------------------
	| /adminDash                                                   | adminDash.html             | this will show admin's dashboard will all details
	--------------------------------------------------------------------------------------------------------------------------------------------------------
	| /addTrainor', methods = ['GET', 'POST']                      | addTrainor.html            | this will add new trainor
	--------------------------------------------------------------------------------------------------------------------------------------------------------
	| /deleteTrainor', methods = ['GET', 'POST']                   | deleteTrainor.html         | this will remove existing trainor
	--------------------------------------------------------------------------------------------------------------------------------------------------------
	|/addRecep', methods = ['GET', 'POST']                         | addRecep.html		     | used to add receptionist
	--------------------------------------------------------------------------------------------------------------------------------------------------------
	| /deleteRecep', methods = ['GET', 'POST']                     | deleteRecep.html           | used to delete recep
	--------------------------------------------------------------------------------------------------------------------------------------------------------
	| /addEquip', methods = ['GET', 'POST']                        | addEquip.html              | Used to add equipments
	--------------------------------------------------------------------------------------------------------------------------------------------------------
	| /removeEquip', methods = ['GET', 'POST']                     | removeEquip.html           | Used to remove equipments
	--------------------------------------------------------------------------------------------------------------------------------------------------------
	| /addMember', methods = ['GET', 'POST']                       | addMember.html             | used to add new member
	--------------------------------------------------------------------------------------------------------------------------------------------------------
	| /deleteMember', methods = ['GET', 'POST']                    | deleteMember.html          | used to delet existing member
	--------------------------------------------------------------------------------------------------------------------------------------------------------
	| /viewDetails'                                                | viewDetails.html           | used to view details
	--------------------------------------------------------------------------------------------------------------------------------------------------------
	|/recepDash                                                    | recepDash.html             | used to view recep dashboard
	--------------------------------------------------------------------------------------------------------------------------------------------------------
	|/trainorDash', methods = ['GET', 'POST']                      | trainorDash.html           | used to view trainor dashboard
	--------------------------------------------------------------------------------------------------------------------------------------------------------
	|/updatePlans', methods = ['GET', 'POST']                      | updatePlans.html           | used to update plans by trainor
	--------------------------------------------------------------------------------------------------------------------------------------------------------
	|/memberDash/<string:username>                                 | memberDash.html            | used to view members dashboard
	--------------------------------------------------------------------------------------------------------------------------------------------------------
	|/profile/<string:username>                                    | profile.html               | used to view profile of any member
	--------------------------------------------------------------------------------------------------------------------------------------------------------
	|/edit_profile/<string:username>', methods = ['GET', 'POST']   | edit_profile.html          | used to edit any profile
	--------------------------------------------------------------------------------------------------------------------------------------------------------
	|/logout                                                       | logout.html                | used to logout from any dashboard
	=========================================================================================================================================================
 

 
## CONTRIBUTION REPORT :

@Shameem Mujawar: 
I reaserched about python framework and chose suitable python framework for web application which is python flask. Python flask is microframework and it is flexible.
we can add many functionality in it. so My contribution in it is develop python flask code. Also I focued on role of owner and develop all necesorry functions for owner of gym
in this project.


@Sri Chandana Melimi: 
In this project, Gym Management System I have taken the responsibility of creating and executing the functionalities that are handled by a receptionist of this particular system.
  I have mainly implemented three functionalities Adding ,Deleting and View Details of Member
I concentrated on the backend part i.e, the Data base design, tables creation and integrating the data base. 
I have learnt and used the concepts of Object Oriented Programing of Python in my functions and classes. Also learnt the concepts of Flask and MySQL and made use of them in our project development.
 Additionally, I was also in responsible of the report's structure, rewriting the content, and delivering the introduction while outlining the libraries we imported for our programming. 

@Akshay Shishupal: 
The base of the project is Python. The spotlight of the project was to produce an HTML webpage and design it using CSS. For doing this we had to research, develop and administer a database on SQL. The CSS helped us to make look the webpages more presentable and easy to format. For some development, we also used JavaScript. As HTML and CSS were not handson for me, practice was important for making it work. I had also made prototype webpages to make sure that the final webpage worked as per requirement.

@Shivraj Srinivas:
The module needed to be learned in order to connect to the database. It took a few days to establish the initial connection and the way commands were carried out. The most pressing issue following the successful connection was figuring out how to use Flask. Another challenging area of work has been the flask; During the development phase, a lot of examples and tutorials were referred to. The members' HTML pages had to communicate with Flask, and the required inputs and outputs had to be taken from the webpage and added to it. There were endeavors made to get the right configuration and sort of happy. The exploration of the flask session had been a beautiful journey, from misgivings about whether handling was taking place to making sure the right session was handled. Working with templates on HTML pages and executing the appropriate SQL commands took relatively little effort. XML layouts were utilized to deal with the certifications, for which some exploration must be finished.


 

 
