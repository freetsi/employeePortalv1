# Employee Report Technical Specifications

# Description

This project acts as a reporting system of a company and provides simple REST APIs for handling simple information storage and retrieval requests for employees&#39; reports. In parallel, a back-office module is provided for handling employees, reports, employees&#39; departments, and log/ audit management.

# Document Structure

The first part outlines architecture and technology stack and the second part reveal the process and technical info.

# Architecture

![alt text](https://i.imgur.com/Lzyl5BW.png)

## Requirements

**Sqlite** : Since I had to implement only 3 simple endpoints no access to real database was needed. Additionally, sqlite has the power of a relation DB without the overhead of having a separate DB server.

**Python + Django Rest Framework** : Django is an open source web framework that helps you create a web app quickly as it takes care of additional web-development needs. Django Rest Framework&#39;s modular, flexible, and customizable architecture makes the development of both simple, turnkey API endpoints and complicated REST constructs possible.

## Requirements and how to run the application

1. A console emulator ([cmder](https://cmder.net/) was used during development)
2. **Python Set up** Python 3.7.4 was used
In your command line type 'python -m pip install -U pip'
3. **Virtual environment** ([virtualenv 20.0.4](https://pypi.org/project/virtualenv/) was used during development)
 Please create a new environment for this project.
4. Git clone the project from git hub repository and navigate to that repository
5. workon <your_env> to enter your environment
6. 'pip install -r requirements.txt' to install all the required packages into your environment
7. DB (sqlite) will also come into the project with git pull. No migrations are needed.
8. Please set and ensure that LOG_PATH from settings.py exist in your machine.
9. 'python manage.py runserver' to start server

## Testing + API Documentation

**drf-yasg** is a Swagger generation tool implemented without using the schema generation provided by Django Rest Framework. It aims to implement as much of the OpenAPI specification as possible - nested schemas, named models, response bodies, enum/pattern/min/max validators, form parameters, etc. - and to generate documents. This also translates into a very useful interactive documentation viewer in the form of swagger-ui.

# Core Functionality

## Data Modelling

### Employees
Django&#39;s default user model was used to depict each employee. Profiles model acts as a one to one relationship model which provides additional employees info such as mobile, address, department, gender etc.
![alt text](https://i.imgur.com/9NgRFA7.png)

### Reports
This model depicts report entries and has a foreign key relationship with usermodel
![alt text](https://i.imgur.com/frT0l4d.png)

### Departments
This model describes department entries of the company. Each department has an autoincrement id and a description.
![alt text](https://i.imgur.com/frT0l4d.png)


## Back Office

Business Admin Console Interface is an interface available to users that belong to the admin group. Through this interface one has access to data models entries and modification rights. This interface also supports logs presentation and audit.

### Logging in

Start by typing the url &#39;http//localhost:8000/&#39; on your browser

![alt text](https://i.imgur.com/DfMhO3l.png)

Use admin/ man123qwe credentials. Admin user is already set up and member of the Admin Group.

### Home Page

This is the first page of the admin console. Navigate to this page from anywhere by clicking the Logo or the home menu option

![alt text](https://i.imgur.com/QNWXi56.png)

#### Header (1)

Header part is always visible from anywhere in the app. &#39;Data Modelling&#39; menu option consists of &#39;employees&#39;, &#39;departments&#39;, &#39;reports&#39; sub menus and &#39;system admin&#39; menu consist of &#39;logs&#39;, &#39;audit&#39; sub menus.

If you click on the &quot;log out&quot; action then you will be logged out from this app

##### Api Tester

By clicking this action, you will navigate to an interface where you can test each api separately

![alt text](https://i.imgur.com/f0Iu0Om.png)

You may need to perform an authorization with the admin/ man123qwe (Basic authentication) to test the APIs. &quot;Fetch&quot; section contains the api for retrieving reports query (GET request). &quot;Post&quot; section contains the apis for initiating or updating employees and report records (POST requests)

![alt text](https://i.imgur.com/p51eVue.png)

You can try out each of these apis with the &quot;try it out button&quot;. The request and response payload are all set up and ready to use with your desired values. Form Validations are also active so you can test anything you wish.

![alt text](https://i.imgur.com/yDFj8fT.png)

##### Api Documentation

By clicking this action, you will navigate to an interface where you can see the full documentation as well as request and response payloads for each api separately

#### Employees (2)

Page for viewing/ modifying employee records.

![alt text](https://i.imgur.com/fAiZ7mh.png)

#### Departments (3)

Page for viewing/ modifying department records.

![alt text](https://i.imgur.com/p4a8YqM.png)

#### Reports (4)

Page for viewing/ modifying report records.

![alt text](https://i.imgur.com/cskUXS2.png)

#### Logs (5)

Page for viewing full application log

![alt text](https://i.imgur.com/dLqim9y.png)

#### Audit(6)

Full stack trace of the web services and business admin console apps listed by month.

!![alt text](https://i.imgur.com/OjOWzaz.png)

## Python Testing

Test file is located in test.py under &#39;rootapp&#39; app. You can run the test with the following command

'python manage.py test'

![alt text](https://i.imgur.com/qKXmf0A.png)

We can change payload to make the test fail or write more complicated tests.

## Ιmprovements
We could configure Django settings for multiple enviroments with different '.env' files with the desired settings.py variables.
We could read the values of these variables from the configuration file insead of directrly declaring them in settings.py. 
This is very useful in deploying the app in UAT and production, where I need different settings for each server.