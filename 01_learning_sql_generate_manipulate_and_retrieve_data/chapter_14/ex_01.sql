DROP VIEW IF EXISTS film_ctgry_actor;

CREATE VIEW film_ctgry_actor (title, category_name, first_name, last_name)
AS
SELECT f.title, c.name, a.first_name, a.last_name
FROM actor a
    INNER JOIN film_actor fa ON a.actor_id = fa.actor_id
    INNER JOIN film f ON fa.film_id = f.film_id
    INNER JOIN film_category ON f.film_id = film_category.film_id
    INNER JOIN category c ON film_category.category_id = c.category_id;

SELECT title, category_name, first_name, last_name
FROM film_ctgry_actor
WHERE last_name = 'FAWCETT';
