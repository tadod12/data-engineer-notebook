# Chapter 13. Indexes and Constraints

## Indexes

Indexes are special tables that, unlike normal data tables, are kept in a specific order. Instead of containing all the
data about an entity, however, an index contains only the column (or columns) used to locate rows in the data table,
along with information describing where the rows are physically located

> The role of indexes is to facilitate the retrieval of a subset of a table’s rows and columns without the need to
> inspect every row in the table

### Index Creation

    AlTER TABLE customer
    ADD INDEX idx_email (email); -- create a B-tree index on the customer.email column

    CREATE INDEX idx_email
    ON customer (email);

    CREATE TABLE customer (
        customer_id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
        store_id TINYINT UNSIGNED NOT NULL,
        first_name VARCHAR(45) NOT NULL,
        last_name VARCHAR(45) NOT NULL,
        email VARCHAR(50) DEFAULT NULL,
        address_id SMALLINT UNSIGNED NOT NULL,
        active BOOLEAN NOT NULL DEFAULT TRUE,
        create_date DATETIME NOT NULL,
        last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (customer_id),
        KEY idx_fk_store_id (store_id),
        KEY idx_fk_address_id (address_id),
        KEY idx_last_name (last_name),
        ...

Show indexes on a specific table

    SHOW INDEX FROM customer \G;

Remove index

    ALTER TABLE customer
    DROP INDEX idx_email;

#### Unique Indexes

A `unique index` plays multiple roles; along with providing all the benefits of a regular index, it also serves as a
mechanism for disallowing duplicate values in the indexed column

    ALTER TABLE customer
    ADD UNIQUE idx_email (email);

> You should not build unique indexes on your primary key column(s), since the server already checks uniqueness for
> primary key values

#### Multicolumn Indexes

    ALTER TABLE customer
    ADD INDEX idx_full_name (last_name, first_name);
    /* 
    useful for queries that specify the first and last names or just the last name
    not be useful for queries that specify only the customer’s first name
    */

### Types of Indexes

#### B-tree Indexes

All the indexes shown thus far are _balanced-tree indexes_ or _B-tree indexes_. B-tree indexes are organized as trees,
with one or more levels of branch nodes leading to a single level of leaf nodes

#### Bitmap Indexes

For columns that contain only a small number of values across a large number of rows (known as _low-cardinality_ data),
a different indexing strategy is needed. To handle this situation more efficiently, Oracle Database includes _bitmap
indexes_, which generate a bitmap for each value stored in the column

    -- Oracle
    CREATE BITMAP INDEX idx_active ON customer (active);

> Bitmap indexes are commonly used in data warehousing environments, where large amounts of data are generally indexed
> on columns containing relatively few values (e.g., sales quarters, geographic regions, products, salespeople)

#### Text Indexes

If your database stores documents, you may need to allow users to search for words or phrases in the documents. MySQL,
SQL Server, and Oracle Database include specialized indexing and search mechanisms for documents; both SQL Server and
MySQL include what they call _full-text_ indexes, and Oracle Database includes a powerful set of tools known as Oracle
Text

### How Indexes Are Used

To see how MySQL's query optimizer decides to execute the query, we can use the `explain` statement to ask the server to
show the execution plan for the query rather than executing the query

    mysql> EXPLAIN
        -> SELECT customer_id, first_name, last_name
        -> FROM customer
        -> WHERE first_name LIKE 'S%' AND last_name LIKE 'P%' \G;
    *************************** 1. row ***************************
                id: 1
       select_type: SIMPLE
             table: customer
        partitions: NULL
              type: range
     possible_keys: idx_last_name,idx_full_name  -- option server can choose
               key: idx_full_name
           key_len: 274
               ref: NULL
              rows: 28
          filtered: 11.11
             Extra: Using where; Using index
    1 row in set, 1 warning (0.00 sec)

> This is an example of **query tuning**. Tuning involves looking at an SQL statement and determining the resources
> available to the server to execute the statement. You can decide to modify the SQL statement, to adjust the database
> resources, or to do both in order to make a statement run more efficiently. Tuning is a detailed topic, and I strongly
> urge you to either read your server’s tuning guide or pick up a good tuning book so that you can see all the different
> approaches available for your server.

### The Downside of Indexes

Every index is a table (special type). Therefore, every time a row is added to or removed from a table, all indexes on
that table must be modified.

> The more indexes you have, the more work the server needs to do to keep all schema objects up-to-date. Best strategy
> is to add an index when a clear need arises

In the case of data warehouses, where indexes are crucial during business hours as users run reports and ad hoc queries
but are problematic when data is being loaded into the warehouse overnight, it is a common practice to drop the indexes
before data is loaded and then re-create them before the warehouse opens for business

Indexing strategy

- Make sure all primary key columns are indexed (most servers automatically create)

- Build indexes on all columns that are referenced in foreign key constraints

- Index any columns that will frequently be used to retrieve data

## Constraints

A constraint is simply a restriction placed on one or more columns of a table

- _Primary key constraints_: Identify the column or columns that guarantee uniqueness within a table

- _Foreign key constraints_: Restrict one or more columns to contain only values found in another table's primary key
  column

- _Unique constraints_: Restrict one or more columns to contain unique values within a table

- _Check constraints_: Restrict the allowable values for a column

### Constraint Creation

    CREATE TABLE customer (
      customer_id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
      store_id TINYINT UNSIGNED NOT NULL,
      first_name VARCHAR(45) NOT NULL,
      last_name VARCHAR(45) NOT NULL,
      email VARCHAR(50) DEFAULT NULL,
      address_id SMALLINT UNSIGNED NOT NULL,
      active BOOLEAN NOT NULL DEFAULT TRUE,
      create_date DATETIME NOT NULL,
      last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
      PRIMARY KEY (customer_id),
        KEY idx_fk_store_id (store_id),
        KEY idx_fk_address_id (address_id),
        KEY idx_last_name (last_name),
      CONSTRAINT fk_customer_address FOREIGN KEY (address_id)
        REFERENCES address (address_id) ON DELETE RESTRICT ON UPDATE CASCADE,
      CONSTRAINT fk_customer_store FOREIGN KEY (store_id)
        REFERENCES store (store_id) ON DELETE RESTRICT ON UPDATE CASCADE
      )ENGINE=InnoDB DEFAULT CHARSET=utf8;

Alternative

    ALTER TABLE customer
    ADD CONSTRAINT fk_customer_address FOREIGN KEY (address_id)
    REFERENCES address (address_id) ON DELETE RESTRICT ON UPDATE CASCADE;

`on` clauses

- `on delete restrict` - cause the server to raise an error if a row is deleted in the parent table that is referenced
  in the child table

- `on update cascade` - cause the server to propagate a change to the primary key value of a parent table to the child
  table

- More options: `on delete set null`, `on update restrict`, `on update set null`


