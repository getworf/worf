# Worf - User & Revenue Management Framework!

Worf (which is short for **Web-based Open source Revenue Framework**) is a user management and revenue framework that makes it easy to manage the entire user journey for your digital product, software solution or software-as-a-service (SaaS) business. Worf can manage all your user data and handles authentication, subscriptions, billing, role-based access management, among other things. It can be easily extended with additional functionality and provides a single source of truth about your users. Worf is security-focused and provides privacy-friendly solutions for the most common problems you face when managing a userbase. It can also work with external services for things like social logins or payments.

**Please note that this is still a pre-alpha build of Worf, it's still a work in progress.**

## Installing

You can install Worf using pip:

    pip install .

When developing Worf, you can install the package in development mode,
which will not copy files but instead link them to your virtual environment
so that you can edit them and see changes immediately:

    pip install -e .

If you want to run tests, please also install test dependencies:

    pip install -r requirements-test.txt --no-index --find-links wheels

## Defining settings

Worf loads settings from the directory specified in the `WORF_SETTINGS_D`
environment variable. You can specify multiple directories separated by
a `:` character as well.

For development, you can point the variable to the `settings` directory in
the Worf repository:

    export WORF_SETTINGS_D=settings

Alterantively, you can use the `.dev-setup` file:

    source .dev-setup

## Setting Up The Database

Worf requires a Postgresql database. By default, it tries to access a
`worf_development` or `worf_test` database for the development or tests,
respectively. The default username and password is set as `worf` in the
settings (don't use this in production!). To create the databases:

    su postgres
    psql
    > CREATE DATABASE worf_development;
    > CREATE DATABASE worf_test;
    > CREATE USER worf WITH ENCRYPTED PASSWORD 'worf';
    > GRANT ALL PRIVILEGES ON DATABASE worf_development TO worf;
    > GRANT ALL PRIVILEGES ON DATABASE worf_test TO worf;

That's it! Now you can run tests and migrate the database for development.

## Migrations

Worf runs on Postgres (but can support SQLite too). The database schema is
managed using SQL migration files. To run the migrations simply execute

    worf db migrate

To add a new migration, create a pair of files in the `migrations` directory
and define your SQL commands for migrating up and down. Take a look at the
existing files to get a feeling for the format.

## Running Worf

To run Worf:

    worf api run

To run the background worker:

    worf worker run

## Creating a superuser

When using Worf for the first time, you will need to create a superuser, which
you can do with the following command:

    worf user create admin --superuser

## Upgrading packages

You can use the fabulous `pur` tool to upgrade packages in the requirements files:

    make update

## Building Wheels

We install all packages from local wheels if possible (for security reasons), to
generate these wheels simply use the following commands:


    make wheels
