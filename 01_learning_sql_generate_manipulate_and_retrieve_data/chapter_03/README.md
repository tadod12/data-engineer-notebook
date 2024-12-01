# Chapter 3. Query Primer

## Query Mechanics

## Query Clauses

- `select` - Determines which columns to include in the query's result set
- `from` - Identifies the tables from which to retrieve data and how the tables should be joined
- `where` - Filters out unwanted data
- `group by` - Used to group rows together by common column values
- `having` - Filters out unwanted groups
- `order by` - Sorts the rows of the final result set by one or more columns

## The SELECT Clause

One of the last clauses that the database server evaluates. The SELECT clause determines which of all possible columns
should be included in the query's result set

    SELECT *
    FROM language;

Include things in SELECT clause:

- Literals, such as numbers or strings
- Expressions, such as `transaction.amount * -1`
- Build-in function calls, such as `ROUND(transaction.amount, 2)`
- User-defined function calls

    ```
    SELECT language_id,
        'COMMON' language_usage,  --Literal--
        language_id * 3.1415927 lang_pi_value,  --Expression--
        upper(name) language_name  --Build-in function- 
    FROM language;  
    ```

### Column Aliases

From previous: `upper(name) language_name`, `language_name` is column alias

Option: Using `as` before the alias name: `SELECT language_id * 3.1415927 AS lang_pi_value`

### Removing Duplicates

    SELECT DISTINCT actor_id FROM film_actor ORDER BY actor_id

## The FROM Clause

The `FROM` clause defines the tables used by a query, along with the means of linking the tables together

### Tables

Four different types of tables:

- Permanent tables (i.e., created using the `create table` statement)

- Derived (Subquery-Generated) tables (i.e., rows returned by a subquery and held in memory)

    ```
    SELECT concat(cust.last_name, ', ', cust.first_name) AS full_name
    FROM (
        SELECT first_name, last_name, email
        FROM customer
        WHERE first_name = 'JESSIE'
    ) AS cust;
    ```

- Temporary tables (i.e., volatile data held in memory): These tables look just like permanent tables, but any data
  inserted into a temporary table will disappear at some point (generally at the end of a transaction or when your
  database session is closed)

    ```
    CREATE TEMPORARY TABLE actor_j (
        actor_id smallint(5),
        first_name varchar(45),
        last_name varchar(45)
    );

    INSERT INTO actor_j
    SELECT actor_id , first_name, last_name
    FROM actor
    WHERE last_name LIKE 'J%';

    SELECT * FROM actor_j

    --Data will disappear after your session is closed--
    ```

- Virtual tables or Views (i.e., created using the `create view` statement): A view is a query that is stored in the
  data dictionary. When you issue a query against a view, your query is merged with the view definition to create a
  final query to be executed.

    ```
    CREATE VIEW curt_vw AS
    SELECT customer_id, first_name, last_name, active
    FROM customer;

    --When the view is created, no additional data is generated or stored--
    ```

### Table Links

    SELECT customer.first_name, customer.last_name, time(rental.rental_date) rental_time
    FROM customer
        INNER JOIN rental
        ON customer.customer_id = rental.customer_id
    WHERE date(rental.rental_date) = '2005-06-14';

### Defining Table Aliases

    SELECT c.first_name, c.last_name, 
        time(r.rental_date) rental_time
    FROM customer c
        INNER JOIN rental r
        ON c.customer_id = r.customer_id
    WHERE date(r.dental_date) = '2005-06-14';
    --time() function extracts the time part from a given datetime expression--

## The WHERE Clause
The `WHERE` clause is the mechanism for filtering out unwanted rows for your result set.
    
    SELECT title 
    FROM film
    WHERE rating = 'G' AND rental_duration >= 7;
    --Individual conditions are separated using operators such as AND, OR, NOT--

## The GROUP BY and HAVING Clauses
    SELECT c.first_name, c.last_name, count(*)
    FROM customer c
        INNER JOIN rental r
        ON c.custom_id = r.custom_id
    GROUP BY c.first_name, c.last_name
    HAVING count(*) >= 40;

## The ORDER BY Clause
The `ORDER BY` clause is the mechanism for sorting your result set using either raw column data or expressions based on column data.

    SELECT c.first_name, c.last_name,
        time(r.rental_date) rental_time
    FROM customer c
        INNER JOIN rental r
        ON c.customer_id = r.customer_id
    WHERE date(r.rental_date) = '2005-06-14'
    ORDER BY c.last_name, c.first_name;
    --date() function extracts the date part from a datetime expression--

### Ascending Versus Descending Sort Order
The default is ascending, so you will need to add the `desc` keyword if you want to use a descending sort.
    
    ORDER BY time(r.rental_date) desc;

### Sorting via Numeric Placeholder
If you are sorting using the columns in your select clause, you can opt to reference the columns by their position in the select clause rather than by name.

    SELECT c.first_name, c.last_name, 
        time(r.rental_date) rental_time
    FROM customer c
        INNER JOIN rental r
        ON c.customer_id = r.customer_id
    WHERE date(r.rantel_date) = '2005-06-14'
    ORDER BY 3 desc; /* column 3 - rental_time */
