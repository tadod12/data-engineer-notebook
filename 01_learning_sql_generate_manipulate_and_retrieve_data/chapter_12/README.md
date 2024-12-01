# Chapter 12. Transactions

This chapter explores _transactions_, which are the mechanism used to group a set of SQL statements together such that
either all or none of the statements succeed

## Multiuser Databases

### Locking

Locks are the mechanism the database server uses to control simultaneous use of data resources

> When some portion of the database is locked, any other users wishing to modify (or possibly read) that data must wait
> until the lock has been released

Most database servers use one of two locking strategies:

- Database writers must request and receive from the server a _write lock_ to modify data, and database readers must
  request and receive from the server a _read lock_ to query data. While multiple users can read data simultaneously,
  only one write lock is given out at a time for each table (or portion thereof), and read requests are blocked until
  the write lock is released

- Database writers must request and receive from the server a write lock to modify data, but readers do not need any
  type of lock to query data. Instead, the server ensures that a reader sees a consistent view of the data (the data
  seems the same even though other users may be making modifications) from the time her query begins until her query has
  finished. This approach is known as _versioning_

> Microsoft SQL Server uses first approach, Oracle Database uses the second approach, and MySQL uses both (depending on
> user's choice of _storage engine_)

### Lock Granularities

- Table locks: Keep multiple users from modifying data in the same table simultaneously

- Page locks: Keep multiple users from modifying data on the same page (a page is a segment of memory generally in
  the range of 2 KB to 16 KB) of a table simultaneously

- Row locks: Keep multiple users from modifying the same row in a table simultaneously

## What is a Transaction?

This extra piece of the concurrency puzzle is the _transaction_, which is a device for grouping together multiple SQL
statements such that either all or none of the statements succeed (a property known as _atomicity_)

    START TRANSACTION;
    /* withdraw money from first account, making sure balance is sufficient */
    
    UPDATE account 
    SET avail_balance = avail_balance - 500
    WHERE account_id = 9988 AND avail_balance > 500;
    
    IF <exactly one row was updated by the previous statement> THEN
      /* deposit money into second account */
      UPDATE account SET avail_balance = avail_balance + 500
      WHERE account_id = 9989;
    
      IF <exactly one row was updated by the previous statement> THEN
      /* everything worked, make the changes permanent */
        COMMIT;
      ELSE
      /* something went wrong, undo all changes in this transaction */
        ROLLBACK;
      END IF;
    ELSE
      /* insufficient funds, or error encountered during update */
      ROLLBACK;
    END IF;

#### Choosing a Storage Engine (MySQL)

Back to locking (now we know about transaction)

- _MyISAM_: A non-transactional engine employing table locking

- _MEMORY_: A non-transactional engine used for in-memory tables

- _CSV_: A transactional engine that stores data in comma-separated files

- _InnoDB_: A transactional engine employing row-level locking

- _Merge_: A specialty engine used to make multiple identical MyISAM tables appear as a single table (a.k.a. table
  partitioning)

- _Archive_: A specialty engine used to store large amounts of unindexed data, mainly for archival purposes
    ```
    mysql> show table status like 'customer' \G;
    *************************** 1. row ***************************
          Name: customer
        Engine: InnoDB -- storage engine 
       Version: 10

    mysql> ALTER TABLE customer ENGINE = INNODB;
    ```

### Starting a Transaction

Database servers handle transaction creation in one of two ways

- An active transaction is **always associated with a database session**, so there is no need or method to explicitly
  begin a transaction. When the current transaction ends, the server automatically begins a new transaction for your
  session

- Unless you explicitly begin a transaction, **individual SQL statements are automatically committed independently of
  one another**. To begin a transaction, you must first issue a command

> Oracle Database takes the first approach, while Microsoft SQL Server and MySQL take the second approach

One of the advantages of Oracle’s approach to transactions is that, even if you are issuing only a single SQL command,
you have the ability to roll back the changes if you don’t like the outcome or if you change your mind. With MySQL and
SQL Server, however, once you press the Enter key, the changes brought about by your SQL statement will be permanent (if
you don't explicitly begin a transaction, you are in what is known as _autocommit mode_)

MySQL allows you to disable autocommit mode

    SET AUTOCOMMIT=0
    -- all SQL commands take place within the scope of a transaction and must be explicitly committed or rolled back

Explicitly begin a transaction (MySQL)

    start transaction;

### Ending a Transaction

Once a transaction has begun (in both ways), you must explicitly end your transaction for your changes to become
permanent

    COMMIT;
    -- Instructs the server to mark the changes as permanent and release any resources (page/row locks) during transaction

Undo all the changes made since starting the transaction

    ROLLBACK;
    -- Instructs the server to return the data to its pre-transaction state

> After `rollback` has been completed, any resources used by your session are released

Scenarios:

- The server shuts down: Transaction will be rolled back automatically when the server is restarted

- Issue SQL schema statement (such as `alter table`): Commit the current transaction and start a new transaction

- Issue another `start transaction` command: The previous transaction will be commited

- Server detects a _deadlock_ (two different transactions are waiting for resources that the other transaction currently
  holds): The transaction will be rolled back, user receive an error message

> Scenario #2: Alternations to a database cannot be rolled back, so those commands must take place outside a
> transaction. Therefore, the server will commit your current transaction, execute the SQL schema statement command(s),
> and then automatically start a new transaction for your session

### Transaction Savepoints

Encountering an issue within a transaction that requires a rollback, but you may not want to undo _all_ the work. You
can establish one or more _savepoints_ within a transaction and use them to roll back to a particular location within
your transaction

Create a savepoint named `my_savepoint`

    SAVEPOINT my_savepoint;

Roll back to a particular savepoint

    ROLLBACK TO SAVEPOINT my_savepoint;

Example

    START TRANSACTION;
    
    UPDATE product
    SET date_retired = CURRENT_TIMESTAMP()
    WHERE product_cd = 'XYZ';

    SAVEPOINT before_close_accounts;

    UPDATE account
    SET status = 'CLOSED', close_date = CURRENT_TIMESTAMP(),
      last_activity_date = CURRENT_TIMESTAMP()
    WHERE product_cd = 'XYZ';

    ROLLBACK TO SAVEPOINT before_close_accounts;

    COMMIT;

> Despite the name, nothing is saved when you create a savepoint. You must eventually issue a `commit` if you want your
> transaction to be made permanent

> If you issue a `rollback` without naming a savepoint, all savepoints within the transaction will be ignored, and the
> entire transaction will be undone