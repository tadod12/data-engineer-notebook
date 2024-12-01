# Chapter 10. Joins Revisited

## Outer Joins

    SELECT f.film_id, f.title, count(i.inventory_id) num_copies
    FROM film f
        LEFT OUTER JOIN inventory i -- full film
        ON f.film_id = i.film_id
    GROUP BY f.film_id, f.title;

The join definition was changed from `inner` to `left outer`, which instructs the server to include all rows from the
table on the left side of the join (`film`, in this case) and then include columns from the table on the right side of
the join (`inventory`) if the join is successful.

The `num_copies` column definition was changed from `count(*)` to `count(i.inventory_id)`, which will count the number
of non-null values of the `inventory.inventory_id` column.

### Left Versus Right Outer Joins

The `outer` keyword is optional, so you may opt for `A left join B` instead, but I recommend including outer for the
sake of clarity.

### Three-Way Outer Joins

    SELECT f.film_id, f.title, i.inventory_id, r.rental_date
    FROM film r
        LEFT OUTER JOIN inventory i
        ON f.film_id = i.film_id
        LEFT OUTER JOIN rental r
        ON i.inventory_id = r.inventory_id
    WHERE f.film_id BETWEEN 13 AND 15;

## Cross Joins (Cartesian Product)

    SELECT c.name category_name, l.name language_name
    FROM category c
        CROSS JOIN language l;

Situation in which the cross join be quite helpful

    -- Generate all dates in a year
    SELECT DATE_ADD('2020-01-01', INTERVAL (ones.num + tens.num + hundreds.num) DAY) dt
    FROM (
        SELECT 0 num UNION ALL
        SELECT 1 num UNION ALL
        SELECT 2 num UNION ALL
        SELECT 3 num UNION ALL
        SELECT 4 num UNION ALL
        SELECT 5 num UNION ALL
        SELECT 6 num UNION ALL
        SELECT 7 num UNION ALL
        SELECT 8 num UNION ALL
        SELECT 9 num UNION ALL
        SELECT 10 num
    ) ones CROSS JOIN (
        SELECT 0 num UNION ALL
        SELECT 10 num UNION ALL
        SELECT 20 num UNION ALL
        SELECT 30 num UNION ALL
        SELECT 40 num UNION ALL
        SELECT 50 num UNION ALL
        SELECT 60 num UNION ALL
        SELECT 70 num UNION ALL
        SELECT 80 num UNION ALL
        SELECT 90 num
    ) tens CROSS JOIN (
        SELECT 0 num UNION ALL
        SELECT 100 num UNION ALL
        SELECT 200 num UNION ALL
        SELECT 300 num
    ) hundreds
    WHERE DATE_ADD('2020-01-01', INTERVAL (ones.num + tens.num + hundreds.num) DAY) < '2021-01-01'
    ORDER BY 1;

Create report shows every day in 2020 along with the number of film rentals on that day

    SELECT days.dt, count(r.rental_id) num_rentals
    FROM rental r
        RIGHT OUTER JOIN (
            SELECT DATE_ADD('2005-01-01', INTERVAL (ones.num + tens.num + hundreds.num) DAY) dt
            FROM (
                SELECT 0 num UNION ALL
                SELECT 1 num UNION ALL
                SELECT 2 num UNION ALL
                SELECT 3 num UNION ALL
                SELECT 4 num UNION ALL
                SELECT 5 num UNION ALL
                SELECT 6 num UNION ALL
                SELECT 7 num UNION ALL
                SELECT 8 num UNION ALL
                SELECT 9 num UNION ALL
                SELECT 10 num
            ) ones CROSS JOIN (
                SELECT 0 num UNION ALL
                SELECT 10 num UNION ALL
                SELECT 20 num UNION ALL
                SELECT 30 num UNION ALL
                SELECT 40 num UNION ALL
                SELECT 50 num UNION ALL
                SELECT 60 num UNION ALL
                SELECT 70 num UNION ALL
                SELECT 80 num UNION ALL
                SELECT 90 num
            ) tens CROSS JOIN (
                SELECT 0 num UNION ALL
                SELECT 100 num UNION ALL
                SELECT 200 num UNION ALL
                SELECT 300 num
            ) hundreds
            WHERE DATE_ADD('2025-01-01', INTERVAL (ones.num + tens.num + hundreds.num) DAY) < '2006-01-01'
        ) days
        ON days.dt = date(r.rental_date)
    GROUP BY days.dt
    ORDER BY 1;

## Natural Joins

This join type relies on identical column names across multiple tables to infer the proper join conditions

    SELECT c.first_name, c.last_name, date(r.rental_date)
    FROM customer c
        NATURAL JOIN rental r; -- both have column `customer_id`

Because you specified a natural join, the server inspected the table definitions and added the join condition
`r.customer_id = c.customer_id` to join the two tables. This would have worked fine, but in the Sakila schema all the
tables include the column `last_update` to show when each row was last modified, so the server is also adding the join
condition `r.last_update = c.last_update`, which causes the query to return no data

    SELECT cust.first_name, cust.last_name, date(r.rental_date)
    FROM (
        SELECT customer_id, first_name, last_name
        FROM customer
    ) cust
        NATURAL JOIN rental r;

