
# Job Search Portal

This project is an example project to  job search platforms for jobseekers
and recruiters. In this Django app, recruiters can create jobs and jobseekers
can apply related to their interests.

## Features

- Registration and login
- Optional job postings
- Profile management


__Registration and login:__

A registration and login page is provided on both the admin and job seeker sides.
Admin can check user records while job seeker, job search on platform,
job application etc. may perform intended activities such as by registering
or logging in.

__Optional job postings:__

The user's preference can be collected through a filtering mechanism in the
application. For example, if someone just wants a Django projects developer
job, postings related to it can be viewed in the person's stream.


__Profile management:__

The user can update their profile by updating, deleting or adding data
according to their preferences.
should be able to manage. A password reset mechanism should also be implemented.


## Running the Project Locally

First, clone the repository to your local machine and prepare an environment

```bash
sedacaglar@debian:~$ git clone git@github.com:sdcaglar/jobsearchportal.git
sedacaglar@debian:~$ cd jobsearchportal
sedacaglar@debian:~/jobsearchportal$ python3 -m venv env
sedacaglar@debian:~/jobsearchportal$ . env/bin/activate
```

Install the requirements
```bash
(env) ➜ sedacaglar@debian:~/jobsearchportal$ pip3 install -r requirements.txt
```

#### Create Database

```bash
root@debian:~# su -l postgres
postgres@debian:~$ CREATE DATABASE jobportaldb;
postgres@debian:~$ psql -U sedacaglar jobportaldb ;
```

#### Create Tables From Model
Now, we have successfully written our table but the table is not being sent to
PostgreSQL yet.

__makemigrations:__ To update and see the history or transaction happened in
our table (We have to run this command everytime when something changes in
models.py e.g. adding new table, change a field name, etc

__migrate:__ The last step to submit or sent out our table into the database
```bash
(env) ➜ sedacaglar@debian:~/jobsearchportal$ python3 manage.py makemigrations app
(env) ➜ sedacaglar@debian:~/jobsearchportal$ python3 manage.py migrate app
(env) ➜ sedacaglar@debian:~/jobsearchportal$ python3 manage.py migrate
```

#### Create Superuser
```bash
(env) ➜ sedacaglar@debian:~/jobsearchportal$ python3 manage.py createsuperuser
```

Finally, run the development server:
```bash
(env) ➜ sedacaglar@debian:~/jobsearchportal$ python3 manage.py runserver
```
The project will be available at http://127.0.0.1:8000/

## Contributors

- [Seda Çağlar](https://github.com/sdcaglar)

## License

The source code is released under the [MIT License](https://choosealicense.com/licenses/mit/).




