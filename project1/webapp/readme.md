**YOUR PROJECT TITLE**

**Video Demo of the webapplication:**  https://youtu.be/R6jUsanKhL0

**Description:**
Launch with command: flask run in the webapp directory.
I made a blog website with a frontpage, where users can post about their latest adventures and discoveries. This app is meant to create community, with the old internet feel. Users can leave comments on each others blogs and create a bio for themselves. Admins can keep an eye out and delete users and posts if the need arises. There is also a profanityfilter active to keep it all civil. 
I've used a website called coolor.co to find some matching colours, but to be honest: esthetics is not my strongsuit. 

## app.py

Flash messages:
The website will let you know if an action succeeded or failed through flash messages. They will be blue or red respective to their meaning. 

Navbar:
To register, login or access other pages than the index and the links on there I loaded a Navbar from bootstrap. The options will differ according to the cookiestatus. If not logged in, there will be login or register options, if logged in you can also navigate to your dashboard. If you're logged in as an admin user there will also appear an admin dashboard, but separate from the rest.  

Index:
The index page will show a list of all the blogs, with the newest one first. The authors of the blog are hyperlinked with their bios and below every blog there is a button that links to the blogpage with comments. Important to note is that you don't have to be logged in for this page or their links. 

Blog including comments:
I've made a page where you can see individual blogs, you don't have to be logged in, but to add to the comment section you have to be logged in. You can still read the comments without logging in, so have fun. The comments are saved in the database that references the user ID and the post ID. 

Register:
A new user who wants to post or comment will have to make an account. It checks the database for duplicates and will create a username and a hash if succesfull, which it will upload into the server.  

logging in:
After succesfully inserting username and password cookies will be created for user_id, username and for admin status. The login function checks if everything's there and will check the hash through a program from werkzeug security which I have imported. 

Change password: 
Combination of register and logging in, checks the hash, creates a new hash if succesfull. 

Check_admin: 
There's a hidden function that refreshes the admin status when needed, because I was experiencing some problems.  

Dashboard:
When you've logged in you'll have access to your dashboard, where you can delete posts and you'll find buttons to creating a new post and to view your bio. Important to add, javascript is listening and will send a warning message on the frontend before you're able to actually delete anything. 

Create post:
I've downloaded and imported an open source markdown editer called Markdown2 with which you can add styles and fonts into the blogposts you create. Blog posts receive a timestamp and are saved in the database connected to the user who wrote them. 

Bio and edit bio:
The bio uses the username in the url, and it's a personal page where you can upload a profile picture. If you haven't upoaded a profile picture yet, you will see a placeholder default profile picture. 

Admin Dashboard:
The admin dashboard is the powerhouse where the one ring rules the world. Basically just a place that loads all the users and posts and gives you a button to delete or promote users (to wield the same power), or to delete a post. 

## helpers.py

There's also a program called helpers.py in which I have added the function that checks if you're logged in, the function that checks if you're an administrator and functions that open and close the database. It saves a lot of space to have those ready and prepared, because almost every route opens the database in one way or another. 

## blog.db 

Is the database that holds tables on users, bios, posts, and comments.
I've used following programs to reset and populate them. 

## reset_schema.sql & test_populate.sql

Behind the scenes I've also made a .sql file that resets the database and a .sql file that populates the server so I can see what I looks like when it's being used. 

## Requirements.txt

Requirements.txt holds all the dependencies and will tell the server to install the different programs i've used to run this website. 

## 




