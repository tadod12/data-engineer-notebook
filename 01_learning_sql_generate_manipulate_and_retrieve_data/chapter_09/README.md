# Chapter 9. Subqueries

## What is a Subquery?

A _subquery_ is a query contained within another SQL statement (_containing statement_)

Like any query, a subquery returns a result set that may consist of:

- A single row with a single column
- Multiple rows with a single column
- Multiple rows having multiple columns
    ```
    SELECT customer_id, first_name, last_name
    FROM customer
    WHERE customer_id = (SELECT MAX(customer_id) FROM customer);  -- noncorrelated subquery
    ```

## Subquery Types

- Noncorrelated Subqueries - Subqueries are completely self-contained
- Correlated Subqueries - Subqueries reference columns from the containing statement

## Noncorrelated Subqueries

Most subqueries that you encounter will be of this type unless you are writing `update` or `delete` statements

    SELECT city_id, city
    FROM city
    WHERE country_id <> (SELECT country_id FROM country WHERE country = 'India');

### Multiple-Row, Single-Column Subqueries

#### The IN and NOT IN Operators

    SELECT city_id, city
    FROM city
    WHERE country_id NOT IN (
      SELECT country_id
      FROM country
      WHERE country IN ('Canada', 'Mexico')
    );

#### The ALL Operators

The `all` operator allows you to make comparisons between a single value and every value in a set

    SELECT first_name, last_name
    FROM customer
    WHERE customer_id <> ALL (
      SELECT customer_id
      FROM payment
      WHERE amount = 0
    );


    SELECT customer_id, count(*)
    FROM rental
    GROUP BY customer_id
    HAVING count(*) > ALL (
      SELECT count(*)
      FROM rental
        INNER JOIN customer c
        ON r.customer_id = c.customer_id
        INNER JOIN address a
        ON c.address_id = a.address_id
        INNER JOIN city ct
        ON a.city_id = ct.city_id
        INNER JOIN country co
        ON ct.country_id = co.country_id
      WHERE co.country IN ('United States', 'Mexico', 'Canada')
      GROUP BY r.customer_id
    );

#### The ANY Operator

Like the `all` operator, the `any` operator allows a value to be compared to the members of a set of values;
unlike `all`, however, a condition using the `any` operator evaluates to true as soon as a single comparison is
favorable

    SELECT customer_id, sum(amount)
    FROM payment
    GROUP BY customer_id
    HAVING sum(amount) > ANY (
      SELECT sum(p.amount)
      FROM payment p
        INNER JOIN customer c
        ON p.customer_id = c.customer_id
        INNER JOIN address a
        ON c.address_id = a.address_id
        INNER JOIN city ct
        ON a.city_id = ct.city_id
        INNER JOIN country co
        ON ct.country_id = co.country_id
      WHERE co.country IN ('Bolivia', 'Paraguay', 'Chile')
      GROUP BY co.country
    );

### Multicolumn Subqueries

    SELECT actor_id, film_id
    FROM film_actor
    WHERE (actor_id, film_id) IN (
      SELECT a.actor_id, f.film_id
      FROM actor a
        CROSS JOIN film f
      WHERE a.last_name = 'MONROE'
        AND f.rating = 'PG'
    );

## Correlated Subqueries

A _correlated subquery_, on the other hand, is _dependent_ on its containing statement from which it references one or
more columns

    SELECT c.first_name, c.last_name
    FROM customer c
    WHERE 20 = (
      SELECT count(*)
      FROM rental r
      WHERE r.customer_id = c.customer_id
    );

Along with equality conditions, you can use correlated subqueries in other types of conditions, such as the range
condition

    SELECT c.first_name, c.last_name
    FROM customer c
    WHERE (
      SELECT sum(p.amount)
      FROM payment p
      WHERE p.customer_id = c.customer_id
    ) BETWEEN 180 AND 240;

### The exists Operator

You use the `exists` operator when you want to identify that a relationship exists without regard for the quantity

    SELECT c.first_name, c.last_name
    FROM customer c
    WHERE EXISTS (
      SELECT 1  # Query only needs to know how many rows have been returned
      FROM rental r
      WHERE r.customer_id = c.customer_id
        AND date(r.rental_date) < '2005-05-25'
    );

> The convention is to specify either `select 1` or `select *` when using exists

    SELECT a.first_name, a.last_name
    FROM actor a
    WHERE NOT EXISTS (
      SELECT 1
      FROM film_actor fa
        INNER JOIN film f ON f.film_id = fa.film_id
      WHERE fa.actor_id = a.actor_id
        AND f.rating = 'R'
    );

### Data Manipulation Using Correlated Subqueries

Subqueries are used heavily in `update`, `delete`, and `insert` statements as well, with correlated subqueries appearing
frequently in `update` and `delete` statements

    UPDATE customer c
    SET c.last_update = (
      SELECT max(r.rental_date) FROM rental r
      WHERE r.customer_id = c.customer_id
    ); -- finding the latest rental date for each customer

Employing a `where` clause with a second correlated subquery

    UPDATE customer c
    SET c.last_update = (
      SELECT max(r.rental_date) 
      FROM rental r
      WHERE r.customer_id = c.customer_id
    )
    WHERE EXISTS (  -- protecting the data in the last_update column from being overwritten with a null
      SELECT 1 
      FROM rental r
      WHERE r.customer_id = c.customer_id
    );

> Table aliases are not allowed when using `delete` in MySQL

    DELETE FROM customer
    WHERE 365 < ALL (
      SELECT datediff(now(), r.rental_date) days_since_last_rental
      FROM rental r
      WHERE r.customer_id = customer.customer_id
    );

## When to Use Subqueries

### Subqueries as Data Sources

    SELECT c.first_name, c.last_name,
      pymnt.num_rentals, pymnt.tot_payments
    FROM customer c
      INNER JOIN (
        SELECT customer_id, count(*) num_rentals, sum(amount) tot_payments
        FROM payment
        GROUP By customer_id
      ) pymnt
    ON c.customer_id = pymnt.customer_id;

> Subqueries used in the `from` clause must be noncorrelated (They are executed first, and the data is held in memory
> until the containing query finishes execution)

#### Data Fabrication

    SELECT pymnt_grps.name, count(*) num_customers
    FROM (
      SELECT customer_id, count(*) num_rentals, sum(amount) tot_payments
      FROM payment
      GROUP BY customer_id
    ) pymnt
      INNER JOIN (
        SELECT 'Small Fry' name, 0 low_limit, 74.99 high_limit
        UNION ALL
        SELECT 'Average Joes' name, 75 low_limit, 149.99 high_limit
        UNION ALL
        SELECT 'Heavy Hitters' name, 150 low_limit, 9999999.99 high_limit
      ) pymnt_grps
      ON pymnt.tot_payments BETWEEN pymnt_grps.low_limit AND pymnt_grps.high_limit
    GROUP BY pymnt_grps.name;

The `from` clause contains two subqueries; the first subquery, named `pymnt`, returns the total number of film rentals
and total payments for each customer, while the second subquery, named `pymnt_grps`, generates the three customer
groupings. The two subqueries are joined by finding which of the three groups each customer belongs to, and the rows are
then grouped by the group name in order to count the number of customers in each group.

#### Task-Oriented Subqueries

    SELECT c.first_name, c.last_name, ct.city,
      pymnt.tot_payments, pymnt.tot_rentals
    FROM (
      SELECT customer_id, count(*) tot_rentals, sum(amount) tot_payments
      FROM payment
      GROUP BY customer_id
    ) pymnt
      INNER JOIN customer c
      ON pymnt.customer_id = c.customer_id
      INNER JOIN address a
      ON c.address_id = a.address_id
      INNER JOIn city ct
      ON a.city_id = ct.city_id;

#### Common Table Expressions (CTEs)

A CTE is a named subquery that appears at the top of a query in a `with` clause, which can contain multiple CTEs
separated by commas. Along with making queries more understandable, this feature also allows each CTE to refer to any
other CTE defined above it in the same `with` clause.

    WITH actor_s AS (
      SELECT actor_id, first_name, last_name
      FROM actor
      WHERE last_name LIKE 'S%'
    ),
    actors_s_pg AS (
      SELECT s.actor_id, s.first_name, s.last_name, f.film_id, f.title
      FROM actor_s s
        INNER JOIN film_actor fa
        ON s.actor_id = fa.actor_id
        INNER JOIN film f
        ON f.film_id = fa.film_id
      WHERE f.rating = 'PG'
    ),
    actors_s_pg_revenue AS (
      SELECT spg.first_name, spg.last_name, p.amount
      FROM actors_s_pg spg
        INNER JOIN inventory i
        ON i.film_id = spg.film_id
        INNER JOIN rental r
        ON i.inventory_id = r.inventory_id
        INNER JOIN payment p
        ON r.rental_id = p.rental_id
    ) -- end of WITH-AS clause
    SELECT spg_rev.first_name, spg_rev.last_name, sum(spg_rev.amount) tot_revenue
    FROM actors_s_pg_revenue spg_rev
    GROUP BY spg_rev.first_name, spg_rev.last_name
    ORDER BY 3 desc;

#### Subqueries as Expression Generators

    SELECT
      ( SELECT c.first_name
        FROM customer c
        WHERE c.customer_id = p.customer_id
      ) first_name,
      ( SELECT c.last_name
        FROM customer c
        WHERE c.customer_id = p.customer_id
      ) last_name,
      ( SELECT ct.city
        FROM customer c
          INNER JOIN address a
            ON c.address_id = a.address_id
          INNER JOIN city ct
            ON a.city_id = ct.city_id
        WHERE c.customer_id = p.customer_id
      ) city,
      sum(p.amount) tot_payments,
      count(*) tot_rentals
    FROM payment p
    GROUP BY p.customer_id;

There are two main differences between this query and the earlier version using a subquery in the `from` clause:

- Instead of joining the `customer`, `address`, and `city` tables to the payment data, correlated scalar subqueries are
  used in the `select` clause to look up the customer’s first/last names and city.

- The `customer` table is accessed three times (once in each of the three subqueries) rather than just once.

Along with using correlated scalar subqueries in `select` statements, you can use noncorrelated scalar subqueries to
generate values for an `insert` statement

    INSERT INTO film_actor (actor_id, film_id, last_update)
    VALUES (
      ( SELECT actor_id 
        FROM actor
        WHERE first_name = 'JENNIFER' AND last_name = 'DAVIS'
      ),
      ( SELECT film_id 
        FROM film
        WHERE title = 'ACE GOLDFINGER'
      ),
      now()
    );
