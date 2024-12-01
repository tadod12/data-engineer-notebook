# Chapter 6. Working with Sets

## Set Theory Primer

## Set Theory Practise

When perform set operations on two data sets, the following guidelines must apply:

- Both data sets must have the same number of columns
- The data types of each column across the two data sets must be the same (or the server must be able to convert one to
  the other)

  SELECT 1 num, 'abc' str
  UNION
  SELECT 9 num, 'xyz' str;
  +-----+-----+
  | num | str |
  +-----+-----+
  | 1 | abc |
  | 9 | xyz |
  +-----+-----+
  2 rows in set (0.02 sec)

## Set Operators

### The union Operator

The union and union all operators allow you to combine multiple data sets. The difference between the two is that union
sorts the combined set and removes duplicates, whereas union all does not.

    SELECT 'CUST' typ, c.first_name, c.last_name
    FROM customer c
    UNION ALL
    SELECT 'ACTR' typ, a.first_name, a.last_name
    FROM actor a;

### The intersect Operator

    SELECT c.first_name, c.last_name
    FROM customer c
    WHERE c.first_name LIKE 'J%' AND c.last_name LIKE 'D%'
    INTERSECT
    SELECT a.first_name, a.last_name
    FROM actor a
    WHERE a.first_name LIKE 'J%' AND a.last_name LIKE 'D%';

### The except Operator

    SELECT a.first_name, a.last_name
    FROM actor a
    WHERE a.first_name LIKE 'J%' AND a.last_name LIKE 'D%'
    EXCEPT
    SELECT c.first_name, c.last_name
    FROM customer c
    WHERE c.first_name LIKE 'J%' AND c.last_name LIKE 'D%';

#### Different between EXCEPT and EXCEPT ALL

Set A

    +----------+
    | actor_id |
    +----------+
    |       10 |
    |       11 |
    |       12 |
    |       10 |
    |       10 |
    +----------+

Set B

    +----------+
    | actor_id |
    +----------+
    |       10 |
    |       10 |
    +----------+

A `except` B

    +----------+
    | actor_id |
    +----------+
    |       11 |
    |       12 |
    +----------+

A `except all` B

    +----------+
    | actor_id |
    +----------+
    |       10 |
    |       11 |
    |       12 |
    +----------+

> `except` removes all occurrences of duplicate data from set A, whereas `except all` removes only one occurrence of
> duplicate data from set A for every occurrence in set B

## Set Operation Rules

### Sorting Compound Query Results

    SELECT a.first_name fname, a.last_name lname
    FROM actor a
    WHERE a.first_name LIKE 'J%' AND a.last_name LIKE 'D%'
    UNION ALL
    SELECT c.first_name, c.last_name
    FROM customer c
    WHERE c.first_name LIKE 'J%' AND c.last_name LIKE 'D%'
    ORDER BY lname, fname;



