# Chapter 15. Metadata

Along with storing all the data that various users insert into a database, a database server also needs to store
information about all the database objects (tables, views, indexes, etc.) that were created to store this data. The
database server stores this information, not surprisingly, in a database. This chapter discusses how and where this
information, known as _metadata_, is stored, how you can access it, and how you can use it to build flexible systems.

## Data About Data

Metadata is essentially data about data. This data is collectively known as the _data dictionary_ or _system catalog_

The database server must safeguard this data so that it can be modified only via an appropriate mechanism,
such as the alter table statement.

Every database server uses a different mechanism to publish metadata

- A set of views: Oracle Database's `user_tables` and `all_constraints`views

- A set of system-stored procedure: SQL Server's `sp_tables` procedure; Oracle Database's `dbms_metadata` package

- A special database: MySQL's `information_schema` database

## information_schema

All the objects available within the `information_schema` database are views. The views within information_schema can be
queried and, thus, used programmatically

    -- Include both tables and views
    SELECT table_name, table_type
    FROM information_schema.tables
    WHERE table_schema = 'sakila'
    ORDER BY 1;

If you are only interested in information about views, you can query `information_schema.views`

    SELECT table_name, is_updatable
    FROM information_schema.views
    WHERE table_schema = 'sakila'
    ORDER BY 1;

Column information for both tables and views is available via the `columns` view

    SELECT column_name, 
        data_type,
        character_maximum_length char_max_len,
        numeric_precision num_prcsn, 
        numeric_scale num_scale
    FROM information_schema.columns
    WHERE table_schema = 'sakila' 
        AND table_name = 'film'
    ORDER BY ordinal_position; -- in the order in which they were added to the table

You can retrieve information about a table’s indexes via the `information_schema.statistics` view

    SELECT index_name, non_unique, seq_in_index, column_name
    FROM information_schema.statistics
    WHERE table_schema = 'sakila' AND table_name = 'rental'
    ORDER BY 1, 3;

> PRIMARY KEY is unique index

You can retrieve the different types of constraints (foreign key, primary key, unique) that have been created via the
`information_schema.table_constraints` view

    SELECT constraint_name, table_name, constraint_type
    FROM information_schema.table_constraints
    WHERE table_schema = 'sakila'
    ORDER BY 3,1;

## Working with Metadata

### Schema Generation Scripts

Although a variety of tools and utilities will generate these types of scripts for you, you can also query the
`information_schema` views and generate the script yourself.

### Deployment Verification

After the deployment scripts have been run, it’s a good idea to run a verification script to ensure that the new schema
objects are in place with the appropriate columns, indexes, primary keys, and so forth

    SELECT tbl.table_name, (
        SELECT count(*) FROM information_schema.columns clm
        WHERE clm.table_schema = tbl.table_schema
            AND clm.table_name = tbl.table_name) num_columns, (
        SELECT count(*) FROM information_schema.statistics sta
        WHERE sta.table_schema = tbl.table_schema
            AND sta.table_name = tbl.table_name) num_indexes, (
        SELECT count(*) FROM information_schema.table_constraints tc
        WHERE tc.table_schema = tbl.table_schema
            AND tc.table_name = tbl.table_name
            AND tc.constraint_type = 'PRIMARY KEY') num_primary_keys
    FROM information_schema.tables tbl
    WHERE tbl.table_schema = 'sakila'
        AND tbl.table_type = 'BASE TABLE'
    ORDER BY 1;

### Dynamic SQL Generation

SQL Server, Oracle Database, and MySQL, allow SQL statements to be submitted to the server as strings.Submitting strings
to a database engine rather than utilizing its SQL interface is generally known as _dynamic SQL execution_

MySQL provides the statements `prepare`, `execute`, and `deallocate` to allow for dynamic SQL execution

    SET @qry = 'SELECT customer_id, first_name, last_name FROM customer';

    PREPARE dynsql1 FROM @qry;
    -- Statement prepared

    EXECUTE dynsql1;
    -- run query

    DEALLOCATE PREPARE dynsql1;
    -- free database resources utilized during execution

Query that includes placeholders

    SET @qry = 'SELECT customer_id, first_name, last_name
        FROM customer WHERE customer_id = ?';

    PREPARE dynsql2 FROM @qry;

    SET @custid = 9;

    EXECUTING dynsql2 USING @custid;

    DEALLOCATE PREPARE dynsql2;

