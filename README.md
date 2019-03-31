# Gnosis

**Gnosis** is an online paper management and collaboration tool.


## Installation Instructions

These instructions are a brief overview of the steps required to run the **Gnosis** Django application on a development
server using Django's build in web server, the free version of Neo4j, and sqlite3.

**Gnosis** is a Python Django web application. You should install a suitable version of Python in 
order to proceed. We have tested **Gnosis** with Python version 3.6.5 but any 3.6.* version should
work. 

These installation instructions are for Mac OS. The instructions for any popular Linux distributions should be very
similar. We have not tested **Gnosis** on Windows 10.

### Install Neo4j

Download and install the free desktop version of the Neo3j Graph database from [here](https://neo4j.com/download/).

We have installed and tested Gnosis with the Neo4j community version 3.3.4 although newer version should
work just as well.

Let's assume that you have successfully installed Neo4j in the directory `/Neo4j/`. You can now start the neo4j server 
by executing the command

`/Neo4j/bin/neo4j start`

If the database server starts without errors you should see the following message printed in the terminal,

    Started neo4j (pid 23687). It is available at http://localhost:7474/
    There may be a short delay until the server is ready.

With your web browser, you can now access the Neo4j console by visiting http://localhost:7474/.

**Important** When you first install Neo4j, you can create a user account and set a password. Remember these as you
will need them later in the instructions.

### Install Gnosis

First, you need to either clone or download the code from GitHub.

To clone the **Gnosis** repo in the directory `/Projects`, change to the latter and then issue
the following command,

    git clone https://github.com/stellargraph/stellar-gnosis.git

This command will clone the **Gnosis** repo into the directory `/Projects/stellar-gnosis`.

Create a new Python virtual environment either using `virtualevn` or `conda` for a suitable version
of Python. Let's assume that the new environment is called `gnosis-env`.

Activate `gnosis-env` and install the library requirements using the following command,

    pip install -r requirements.txt

**Important:** As the next step you must apply a patch to the django-neomodel library. Locate
the file `/site-packages/django_neomodel/__init__.py` and the method `get_choices(self, include_blank=True)`.

Then replace the line,

    choices=list(self.choices)if self.choices else []

with the following,

    choices=[(k, v)for k, v in self.choices.items()] if self.choices else []

Locate the `settings.py` file in the directory `/Projects/stellar-gnosis/gnosis/gnosis/`. You need to set your
Neo4j database password so that Django can access it. Find the line,

    NEOMODEL_NEO4J_BOLT_URL = os.environ.get('NEO4J_BOLT_URL', 'bolt://neo4j:GnosisTest00@localhost:7687')

The string `bolt://neo4j:GnosisTest00@localhost:7687'` indicates that the default (for development) Neo4j user
name is *neo4j* and the password is `GnosisTest00`. Replace these with the username and password you created earlier
during the Neo4j installation. You do not need a strong password as this is only used for development. You can use the
values in `settings.py` if you want; in this case, you don't have to modify the above line.

#### Prepare the databases

Change to the directory `/Projects/stellar-gnosis/gnosis/` where you can find the file `manage.py`.

Prepare the Neo4j and sqlite3 databases by using the following commands,

    python manage.py install_labels
    python manage.py makemigrations
    python manage.py migrate
    
Create a **Gnosis** administrator account using the below command and following the prompts:

    python manage.py createsuperuser

You can now start the development server by issuing the command,

    python manage.py runserver
    
You can access **Gnosis** running on your local machine by pointing your web browser to `http://127.0.0.1:8000/`

## License

Copyright 2010-2019 Commonwealth Scientific and Industrial Research Organisation (CSIRO).

All Rights Reserved.

NOTICE: All information contained herein remains the property of the CSIRO. The intellectual and technical concepts 
contained herein are proprietary to the CSIRO and are protected by copyright law. Dissemination of this information 
or reproduction of this material is strictly forbidden unless prior written permission is obtained from the CSIRO.
