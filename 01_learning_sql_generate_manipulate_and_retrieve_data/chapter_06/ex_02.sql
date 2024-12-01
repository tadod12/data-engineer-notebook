SELECT a.first_name fname, a.last_name lname
FROM actor a
WHERE a.last_name LIKE 'L%'
UNION
SELECT c.first_name, c.last_name
FROM customer c
WHERE c.last_name LIKE 'L%'
ORDER BY lname; /* include ex_03 */