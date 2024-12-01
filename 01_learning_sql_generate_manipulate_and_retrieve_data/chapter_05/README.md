# Chapter 5. Querying Multiple Tables

## Join

> A foreign key constraint can optionally be created to verify that the values in one table exist in another table

### Cartesian Product

    SELECT c.first_name, c.last_name, a.address
    FROM customer c JOIN address a

The query didn't specify how the two tables should be joined, the database server generated the _Cartesian product_,
which is _every_ permutation of the two tables
> This type of join is known as _cross join_, and it is rarely used

### Inner Joins

    SELECT c.first_name, c.last_name, a.address
    FROM customer c JOIN address a
        ON c.address_id = a.address_id;

The server joins the `customer` and `address` tables by using the `address_id` column to traverse from one table to the
other
> This type of join is known as an _inner join_, and it is the most commonly used type of join

With the addition of the join type:

    SELECT c.first_name, c.last_name, a.address
    FROM customer c INNER JOIN address a
        ON c.address_id = a.address_id;

If the names of the columns used to join the two tables are identical, you can use the `using` subclause instead of
the `on` clause:

    SELECT c.first_name, c.last_name, a.address
    FROM customer c INNER JOIN address a
        USING(address_id);

### The ANSI Join Syntax

    SELECT c.first_name, c.last_name, a.address
    FROM customer c, address a
    WHERE c.address_id = a.address_id;

The ANSI join syntax has the following advantages:

- Join conditions and filter conditions are separated into two different clauses (the on subclause and the where clause,
  respectively), making a query easier to understand.
- The join conditions for each pair of tables are contained in their own on clause, making it less likely that part of a
  join will be mistakenly omitted.

The benefits of the SQL92 join syntax are easier to identify for complex queries that include both join and filter
conditions

    SELECT c.first_name, c.last_name, a.address
    FROM customer c INNER JOIN address a
      ON c.addres_id = a.address_id
    WHERE a.postal_code = 52137;

## Joining Three or More Tables

    SELECT c.first_name, c.last_name, ct.city
    FROM customer c
      INNER JOIN address a
      ON c.address_id = a.address_id
      INNER JOIN city ct
      ON a.city_id = ct.city_id

### Using Subqueries as Tables

    SELECT c.first_name, c.last_name, addr.address, addr.city
    FROM customer c
      INNER JOIN (
        SELECT a.address_id, a.address, ct.city
        FROM address a
          INNER JOIN city ct
          ON a.city_id = ct.city_id
        WHERE a.district = 'California'
      ) addr
      ON c.address_id = addr.address_id;

### Using the same table twice

    SELECT f.title
    FROM film f
      INNER JOIN film_actor fa1
      ON f.film_id = fa1.film_id
      INNER JOIN actor a1
      ON fa1.actor_id = a1.actor_id
      INNER JOIN film_actor fa2
      ON f.film_id = fa2.film_id
      INNER JOIN actor a2
      ON f.actor_id = a2.actor_id
    WHERE (a1.first_name = 'CATE' AND a1.last_name = 'MCQUEEN')
      AND (a1.first_name = 'CUBA' AND a1.last_name = 'BIRCH');

## Self-Joins

Some tables include a _self-referencing foreign key_, which means that it includes a column that points to the primary
key within the same table

Example: The `film` table includes the column `prequel_film_id`, which points to the film’s parent (e.g., the film _Fiddler Lost II_ would use this column to point to the parent film _Fiddler Lost_)

    SELECT f.title, f_prnt.title prequel
    FROM film f
      INNER JOIN film f_prnt
      ON f_prnt.film_id = f.prequel_film_id
    WHERE f.prequel_film_id IS NOT NULL;
