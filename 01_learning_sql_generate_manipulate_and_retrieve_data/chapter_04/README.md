# Chapter 4. Filtering

## Condition Evaluation

A `WHERE` clause may contain one or more _conditions_, separated by the operators `AND` and `OR`

    WHERE first_name = 'STEVEN' AND create_date > '2006-01-01'

### Using Parentheses

    WHERE (first_name = 'STEVEN' OR last_name = 'YOUNG')
        AND create_date > '2006-01-01'

### Using the not Operator

    WHERE NOT (first_name = 'STEVEN' OR last_name = 'YOUNG') --NOT for this line--
        AND create_date > '2006-01-01'

- You can use the `not` operator:

    ```    
    WHERE first_name <> 'STEVEN' AND last_name <> 'YOUNG'
        AND create_date > '2006-01-01'
  
    /* first_name not equal 'STEVEN' */
    ```

## Building a Condition
A condition is made up of one or more expressions combined with one or more operators

An expression can be any of the following:
- A number
- A column in a table or view
- A string literal, such as `'Maple Street'`
- A build-in function, such as `concat('Learning', ' ', 'SQL')`
- A subquery
- A list of expressions, such as `('Boston', 'New York', 'Chicago')`

The operators used within conditions include:
- Comparison operators, such as `=`, `!=`, `<`, `>`, `<>`, `like`, `in`, and `between`
- Arithmetic operators, such as `+`, `-`, `*`, and `\`

## Condition Types

### Equality Conditions

    title = 'RIVER OUTLAW'
    fed_id = '111-11-1111'
    amount = 375.25
    film_id = (SELECT film_id FROM film WHERE title = 'RIVER OUTLAW')

#### Inequality Conditions

    WHERE date(r.rental_date) <> '2005-06-14'
    --or--
    WHERE date(r.rental_date) != '2005-06-24'

#### Data Modification Using Equality Conditions

    DELETE FROM rental
    WHERE year(rental_date) = 2004;

### Range Conditions

    rental_date < '2005-05-25'

#### The Between Operator

    WHERE rental_date BETWEEN '2005-06-14' AND '2005-06-16'

#### String Ranges

    WHERE last_name BETWEEN 'FA' AND 'FR'
    /* Result set
    FARNSWORTH
    FENNEL
    FERGUSON
    */

### Membership Conditions

    SELECT title, rating
    FROM film
    WHERE rating IN ('G', 'PG');

#### Using Subquery
    
    SELECT title, rating
    FROM film
    WHERE rating IN (SELECT rating FROM film WHERE title LIKE '%PET%';

#### Using NOT IN
    
    SELECT title, rating
    FROM film
    WHERE rating NOT IN ('PG-13', 'R', 'NC-17');

### Matching Conditions

    WHERE left(last_name, 1) = 'Q';

> `left(..., n)` - strips off the first n letters of the column ...

#### Using Wildcards

- The percent sign `%` represents zero, one, or multiple characters
- The underscore sign `_` represents one, single character

#### Using Regular Expressions

    /* Find all customers whose last name starts with Q or Y */
    SELECT last_name, first_name
    FROM customer
    WHERE last_name REGEXP '^[QY]'

## Null: That Four-Letter Word
- Not applicable
- Value not yet known
- Value undefined

> An expression can be null, but it can never equal null
> Two nulls are never equal to each other

    SELECT rental_id, customer_id
    FROM rental
    WHERE return_date IS NULL; --or = NULL--

> `WHERE return_date NOT BETWEEN '2005-05-01' AND '2005-09-01'` not contains null value of return_date


