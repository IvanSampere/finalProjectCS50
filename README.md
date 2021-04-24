# Special Activities Repository
#### Video Demo:  https://youtu.be/FIwrKOKF9ds
#### Description:
This project is my CS50 final project.It´s a web-based application to share activities with other people who work with people with disabilities.
On the web you can read the activities that wrote other people, without an account, but if you want to write your own activities you must register.
On the web there are four sections, and you can filter by those, by the ages and the time that there is writen.
When you register you can access to write activities and consult your activities, you can even delete them if you want.

#### app.py
This file gets all the logic of the project. First connect with flask, after that there is the configuration of the application to use the library
Session instead the coockies. After config the Session, the application connects with the database, using the sc50 library because, to me, it is more
confortable at the time to execute the queries later.

The first function is for the default routing, where execute a query to get all the activities from the database, and render the index template
with that information. After that is the logic function, that clear the session and, if the request method is GET render the template login but if the
request method is POST get the information of the formulary, execute a query to get the users from the database and check if the user exist
and the password is correct, after that keep the user id and their username with the library Session, and finally redirect to the index.

The function register in first place render the template register. If the request method is POST, get the data from the formulary. For the password generates
a hash password to save in the database. Check if the username or the email exist, if they already exist redirect to the register template, if there is all okay
execute a query to insert the data to the database, after call the login function to login directly and redirect to the index.

The function log_out, only clear the session and redirect to the index.

The content function the first time get the arguments of the url and execute the query to get all the activities of the section and return the template
with the data. When the method is POST, get the data from the formulary, if there is no data gives default values, and executes a queries to get the activities,
and finally render the template with the data.

The activity function takes de arguments of the url, that is the activity id, execute a query to get all the information of the activity. To preserve
the original text (with their paragraphs) loops the text and every \r gives and tag br, finally render the template with the data. This logic is
the same to the function my_activities.

The new activity function in firat place render the template new_activity.html. When the request method is POST, get the data from the formulary,
execute a query to insert the activity in their table, and alsowith the tags and the ages. Finally redirect to the same page.

The delete activity function get the activity id from the arguments on the url, and execute a query to delete this activity, and redirect to the
my_activities template.