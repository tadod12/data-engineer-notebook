# Chapter 14. Views

## What Are Views?

A view is simply a mechanism for querying data. Unlike tables, views do not involve data storage; you won’t need to
worry about views filling up your disk space. You create a view by assigning a name to a `select` statement and then
storing the query for others to use

View definition

    CREATE VIEW customer_vw (customer_id, first_name, last_name, email) -- list of view column names
    AS
    SELECT customer_id, first_name, last_name, concat(substr(email,1,2), '*****', substr(email, -4)) email
    FROM customer;

> When the create view statement is executed, the database server simply stores the view definition for future use; the
> query is not executed, and no data is retrieved or stored

Query view just like table

    SELECT first_name
    FROM customer_vw;

You can join views to other tables (or even to other views) within a query

    SELECT cv.first_name, cv.last_name, p.amount
    FROM customer_vw cv
        INNER JOIN payment p
        ON cv.customer_id = p.customer_id
    WHERE p.amount >= 11;

## Why Use Views?

### Data Security

The best approach for these situations is to keep the table private (i.e., don’t grant select permission to any users)
and then to create one or more views that either omit or obscure (such as the '*****' approach taken with the
customer_vw.email column) the sensitive columns. You may also constrain which rows a set of users may access by adding a
where clause to your view definition

### Data Aggregation

    CREATE VIEW sales_by_film_category
    AS
    SELECT
        c.name category,
        SUM(p.amount) total_sales
    FROM payment p
        INNER JOIN rental r ON p.rental_id = r.rental_id
        INNER JOIN inventory i ON r.inventory_id = i.inventory_id
        INNER JOIN film f ON i.film_id = f.film_id
        INNER JOIN film_category fc ON f.film_id = fc.film_id
        INNER JOIN category c ON fc.category_id = c.category_id
    GROUP BY c.name
    ORDER BY total_sales DESC;

### Hiding Complexity

    CREATE VIEW film_stats
    AS
    SELECT f.film_id, f.title, f.description, f.rating, (
        SELECT c.name
        FROM category c
            INNER JOIN film_category fc ON c.category_id = fc.category_id
        WHERE fc.film_id = f.film_id
    ) category_name, (
        SELECT count(*)
        FROM film_actor fa
        WHERE fa.film_id = f.film_id
    ) num_actors, (
        SELECT count(*)
        FROM inventory i
        WHERE i.film_id = f.film_id
    ) inventory_cnt, (
        SELECT count(*)
        FROM inventory i
            INNER JOIN rental r ON i.inventory_id = r.inventory_id
        WHERE i.film_id = f.film_id
    ) num_rentals
    FROM film f;

> Data from the other five tables is generated using scalar subqueries

### Joining Partitioned Data

Some database designs break large tables into multiple pieces in order to improve performance

    CREATE VIEW payment_all (payment_id, customer_id, staff_id, rental_id, 
        amount, payment_date, last_update)
    AS
    SELECT payment_id, customer_id, staff_id, rental_id,
        amount, payment_date, last_update
    FROM payment_history
    UNION ALL
    SELECT payment_id, customer_id, staff_id, rental_id,
        amount, payment_date, last_update
    FROM payment_current;

Using a view in this case is a good idea because it allows the designers to change the structure of the underlying data
without the need to force all database users to modify their queries

## Updatable Views

If you provide users with a set of views to use for data retrieval, what should you do if the users also need to modify
the same data? MySQL, Oracle Database, and SQL Server all allow you to modify data through a view, as long as you abide
by certain restrictions

- No aggregate function are used (`max()`, `min()`, `avg()`, etc.)

- The view does not employ `group by` or `having` clauses

- No subqueries exist in the `select` or `from` clause, and any subqueries in the `where` clause do not refer to tables
  in the `from` clause

- The view does not utilize `union`, `union all`, or `distinct`

- The `from` clause includes at least one table or updatable view

- The `from` clause uses only inner joins if there is more than one table or view

### Updating Simple Views

    CREATE VIEW customer_vw (customer_id, first_name, last_name, email)
    AS
    SELECT customer_id, first_name, last_name, 
        concat(substr(email, 1, 2), '*****', substr(email, -4)) email
    FROM customer;

This view definition doesn't violate any of the restrictions listed earlier, so you can use it to modify data in
the `customer` table

    UPDATE customer_vw
    SET last_name = 'SMITH-ALLEN'
    WHERE customer_id = 1;

Check the underlying `customer` table

    SELECT first_name, last_name, email
    FROM customer
    WHERE customer_id = 1;
    +------------+-------------+-------------------------------+
    | first_name | last_name | email |
    +------------+-------------+-------------------------------+
    | MARY | SMITH-ALLEN | MARY.SMITH@sakilacustomer.org |
    +------------+-------------+-------------------------------+
    1 row in set (0.00 sec)

You will not able to modify the `email` column, since it is delivered from an expression

    mysql> UPDATE customer_vw
        -> SET email = 'MARY.SMITH-ALLEN@sakilacustomer.org'
        -> WHERE customer_id = 1;
    ERROR 1348 (HY000): Column 'email' is not updatable

> views that contain derived columns cannot be used for inserting data, even if the derived columns are not included in
> the statement

### Updating Complex Views

    CREATE VIEW customer_details
    AS
    SELECT c.customer_id, c.store_id, c.first_name, c.last_name, c.address_id,
      c.active, c.create_date, a.address, ct.city, cn.country, a.postal_code
    FROM customer c
      INNER JOIN address a ON c.address_id = a.address_id
      INNER JOIN city c ON a.city_id = ct.city_id
      INNER JOIN country ct ON ct.country_id = cn.country_id;

Update `customer`, `address` table through view

    UPDATE customer_details
    SET address = '999 Mockingbird Lane'
    WHERE customer_id = 1;

    UPDATE customer_details
    SET last_name = 'SMITH-ALLEN', active = 0
    WHERE customer_id = 1;

> Can not update columns from both tables in a single statement

    UPDATE customer_details
    SET last_name = 'SMITH-ALLEN',
      active = 0,
      address = '999 Mockingbird Lane'
    WHERE customer_id = 1;
    ERROR 1393 (HY000): Can not modify more than one base table
      through a join view 'sakila.customer_details'

Same with insert data
    
    INSERT INTO customer_details
    (customer_id, store_id, first_name, last_name, address_id, active, create_date)
    VALUES (9998, 1, 'BRIAN', 'SALAZAR', 5, 1, now());
    Query OK, 1 row affected -- cuz this statement only populates columns from customer table

    INSERT INTO customer_details
    (customer_id, store_id, first_name, last_name, address_id, active, creat_date, address)
    VALUES (9999, 2, 'THOMAS', 'BISHOP', 7, 1, now()), '999 Mockingbird Lane');
    ERROR 1393 (HY000): Can not modify more than one base table 
      through a join view 'sakila.customer_details'

    