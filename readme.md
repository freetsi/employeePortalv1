# Employee Report Technical Specifications

# Contents

[Employee Report Technical Specifications 1](#_Toc53584345)

[Description 2](#_Toc53584346)

[Document Structure 2](#_Toc53584347)

[Architecture 2](#_Toc53584348)

[Requirements 2](#_Toc53584349)

[Requirements and how to run the application 2](#_Toc53584350)

[Testing + API Documentation 3](#_Toc53584351)

[Core Functionality 3](#_Toc53584352)

[Data Modelling 3](#_Toc53584353)

[Back Office 3](#_Toc53584354)

[Logging in 4](#_Toc53584355)

[Home Page 4](#_Toc53584356)

[Header (1) 4](#_Toc53584357)

[Api Tester 5](#_Toc53584358)

[Api Documentation 6](#_Toc53584359)

[Employees (2) 6](#_Toc53584360)

[Departments (3) 6](#_Toc53584361)

[Reports (4) 7](#_Toc53584362)

[Logs (5) 7](#_Toc53584363)

[Audit(6) 7](#_Toc53584364)

[Python Testing 8](#_Toc53584365)

# Description

This project acts as a reporting system of a company and provides simple REST APIs for handling simple information storage and retrieval requests for employees&#39; reports. In parallel, a back-office module is provided for handling employees, reports, employees&#39; departments, and log/ audit management.

# Document Structure

The first part outlines architecture and technology stack and the second part reveal the process and technical info.

# Architecture

![](RackMultipart20201014-4-1hp6pba_html_e98bdda42486bad5.png)

## Requirements

**Sqlite** : Since I had to implement only 3 simple endpoints no access to real database was needed. Additionally, sqlite has the power of a relation DB without the overhead of having a separate DB server.

**Python + Django Rest Framework** : Django is an open source web framework that helps you create a web app quickly as it takes care of additional web-development needs. Django Rest Framework&#39;s modular, flexible, and customizable architecture makes the development of both simple, turnkey API endpoints and complicated REST constructs possible.

## Requirements and how to run the application

1. A console emulator ([cmder](https://cmder.net/) was used during development)
2. **Python Set up** Python 3.7.4 was used
In your command line type python -m pip install -U pip
3. **Virtual environment** ([virtualenv 20.0.4](https://pypi.org/project/virtualenv/) was used during development)
 Please create a new environment for this project.
4. Git clone the project from git hub repository and navigate to that repository
5. workon \&lt;your\_env\&gt; to enter your environment
6. pip install requirements.txt to install all the required packages into your environment
7. DB (sqlite) will also come into the project with git pull. No migrations are needed.
8. python mange.py runserverto start server

## Testing + API Documentation

**drf-yasg** is a Swagger generation tool implemented without using the schema generation provided by Django Rest Framework. It aims to implement as much of the OpenAPI specification as possible - nested schemas, named models, response bodies, enum/pattern/min/max validators, form parameters, etc. - and to generate documents. This also translates into a very useful interactive documentation viewer in the form of swagger-ui.

# Core Functionality

## Data Modelling

Employees: Django&#39;s default user model was used to depict each employee. Profiles model acts as a one to one relationship model which provides additional employees info such as mobile, address, department, gender etc.

![](RackMultipart20201014-4-1hp6pba_html_35df5e758c98f474.png)

Reports: This model depicts report entries and has a foreign key relationship with usermodel

![](RackMultipart20201014-4-1hp6pba_html_6c1ed13f0884cc38.png)

Departments: This model describes department entries of the company. Each department has an autoincrement id and a description.

## Back Office

Business Admin Console Interface is an interface available to users that belong to the admin group. Through this interface one has access to data models entries and modification rights. This interface also supports logs presentation and audit.

### Logging in

Start by typing the url &#39;http//localhost:8000/&#39; on your browser

![](RackMultipart20201014-4-1hp6pba_html_823f6d3a584c8164.png)

Use admin/ man123qwe credentials. Admin user is already set up and member of the Admin Group.

### Home Page

This is the first page of the admin console. Navigate to this page from anywhere by clicking the Logo or the home menu option

![](RackMultipart20201014-4-1hp6pba_html_377a5489f656885c.png)

#### Header (1)

Header part is always visible from anywhere in the app. &#39;Data Modelling&#39; menu option consists of &#39;employees&#39;, &#39;departments&#39;, &#39;reports&#39; sub menus and &#39;system admin&#39; menu consist of &#39;logs&#39;, &#39;audit&#39; sub menus.

If you click on the &quot;log out&quot; action then you will be logged out from this app

##### Api Tester

By clicking this action, you will navigate to an interface where you can test each api separately

![](RackMultipart20201014-4-1hp6pba_html_a708a95723ae59df.png)

You may need to perform an authorization with the admin/ man123qwe (Basic authentication) to test the APIs. &quot;Fetch&quot; section contains the api for retrieving reports query (GET request). &quot;Post&quot; section contains the apis for initiating or updating employees and report records (POST requests)

![](RackMultipart20201014-4-1hp6pba_html_b254f71d68618a31.png)

You can try out each of these apis with the &quot;try it out button&quot;. The request and response payload are all set up and ready to use with your desired values. Form Validations are also active so you can test anything you wish.

![](RackMultipart20201014-4-1hp6pba_html_bb77da9983058883.png)

##### Api Documentation

By clicking this action, you will navigate to an interface where you can see the full documentation and request and response payloads for each api separately

#### Employees (2)

Page for viewing/ modifying employee records.

![](RackMultipart20201014-4-1hp6pba_html_e3d36b74ae00f1d8.png)

#### Departments (3)

Page for viewing/ modifying department records.

![](RackMultipart20201014-4-1hp6pba_html_453646eb5d1c2e69.png)

#### Reports (4)

Page for viewing/ modifying report records.

![](RackMultipart20201014-4-1hp6pba_html_9badc048707d64bd.png)

#### Logs (5)

Page for viewing full application log

![](RackMultipart20201014-4-1hp6pba_html_29ea89b6b50df4ee.png)

#### Audit(6)

Full stack trace of the web services and business admin console apps listed by month.

![](RackMultipart20201014-4-1hp6pba_html_28bc604f57977b29.png)

## Python Testing

Test file is located in test.py under &#39;rootapp&#39; app. You can run the test with the following command

Python manage.py test

![](RackMultipart20201014-4-1hp6pba_html_a8b5958a6d0bba38.png)

We can change payload to make the test fail or write more complicated tests.

#