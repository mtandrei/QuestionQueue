Flask Question Queue App

To get set up on the project:

1. Set up virtualenv
    - run "virtualenv venv"
    - to activate run "source venv/bin/activate"
    - to deactivate run "deactivate"
2. Use pip to install dependencies (in the virtualenv)
    - run "pip install -r pip.req". Try skipping next two commands.
3. Run "python run.py"

Database stuff:

Ubuntu: sudo apt-get install mysql-server libmysqlclient-dev python-dev
Fedora: yum install python-migrate

Run the following commands:
- "sudo mysql"
- "create database queue;"
- "create user 'queue'@'localhost' identified by 'queue';"
- "grant all privileges on queue.* to 'queue'@'localhost';"
- "flush privileges;"
Quit out of mysql with "quit". Then run:
- "./migrate.py db init"
- "./migrate.py db migrate"
- "./migrate.py db upgrade"

To check the database subsequently, run "mysql -uqueue -pqueue"
To change database structure, edit queue/models.py, then run migrate and upgrade again.
If you happen to remove the migrations folder, then run init, migrate, then upgrade.

NOTE: To run this app in full, you need to set up an account with Twilio
