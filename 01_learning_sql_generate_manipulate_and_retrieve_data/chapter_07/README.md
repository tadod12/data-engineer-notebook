# Chapter 7. Data Generation, Manipulation, and Conversion

## Working with String Data

### String Generation

The simplest way to populate a character column is to enclose a string in quotes

#### Including Single Quotes

    UPDATE string_tbl
    SET text_fld = 'This string didn\'t work, but it does now';

If you are retrieving the string to add to a file that another program will read, in MySQL, you can use the built-in
function quote(), which places quotes around the entire string and adds escapes to any single quotes/apostrophes within
the string

    SELECT quote(text_fld)
    FROM string_tbl;

#### Including Special Character

The SQL Server and MySQL servers include the built-in function `char()` so that you can build strings from any of the
255 characters in the ASCII character set (Oracle Database users can use the `chr()` function)

    SELECT CHAR(97, 98, 99, 100, 101, 102, 103);
    +--------------------------------+
    | CHAR(97,98,99,100,101,102,103) |
    +--------------------------------+
    | abcdefg                        |
    +--------------------------------+
    1 row in set (0.01 sec)

The `concat()` function to concatenate individual strings

    SELECT CONCAT('danke sch', CHAR(148), 'n');

### String Manipulation

#### String Functions That Return Numbers

One of the most commonly used is the `length()` function, which returns the number of characters in the string

    SELECT LENGTH(char_fld) char_length
    FROM string_tbl;

Along with finding the length of a string, you might want to find the location of a substring within a string. You could
use the `position()` function

    SELECT POSITION('characters' IN vchar_fld)
    FROM string tbl;

> For those of you who program in a language such as C or C++, where the first element of an array is at position 0,
> remember when working with databases that the first character in a string is at position 1. A return value of 0 from
> instr() indicates that the substring could not be found, not that the substring was found at the first position in the
> string

`locate()` function, which is similar to the `position()` function except that it allows an optional third parameter,
which is used to define the search’s start position

    SELECT LOCATE('is', vchar_fld, 5)
    FROM string_tbl;
    /* start searching from fifth character */

`strcmp()` takes 2 strings as arguments and returns one of the following:

- `-1` if the first string comes before the second string in sort order
- `0` if the strings are identical
- `1` if the first string comes after the second string in sort order

#### String Functions That Return Strings

`concat()` function

    SELECT concat(first_name, ' ', last_name, ' has been a customer since ', date(create_date)) cust_narrative
    FROM customer;

`insert()` function - Add/replace characters in the `middle` of a string. The `insert()` function takes 4 arguments: The
original string, the position at which to start, the number of characters to replace, and the replacement string

    SELECT INSERT('goodbye world', 9, 0, 'cruel ') string; -- string is alias
    /* goodbye cruel world */

    SELECT INSERT('goodbye world', 1, 7, 'hello') string;
    /* hello world */

`replace()` function - Replacing one substring with another

    SELECT REPLACE('goodbye world', 'goodbye', 'hello')
    from dual; -- line for Oracle

`substring()` function - Extract a substring from a string

    SELECT SUBSTRING('goodbye cruel world', 9, 5);
    /* cruel (index start from 1 not 0) */

## Working with Numeric Data

### Performing Arithmetic Functions

- `acos(x)` - arc cos of x
- `asin(x)` - arc sin of x
- `atan(x)` - arc tan of x
- `cos(x)` - cos of x
- `exp(x)` - e^x
- `ln(x)` - natural log of x
- `sin(x)` - sin of x
- `sqrt(x)` - square root of x
- `tan(x)` - tan of x

`mod()` function

    SELECT MOD(10, 4);
    /* 2, with MySQL also use for real number: MOD(22.75, 5) -> 2.75 */

`pow()` function

    SELECT POW(2, 8);
    /* 256 */

### Controlling Number Precision

`ceil()` function - round up
`floor()` function - round down
`round()` function - round up or down from the _midpoint_ between two integers

    SELECT ROUND(72.0909) -- 72
    SELECT ROUND(72.0909, 1) -- 72.1
    SELECT ROUND(72.0909, 2) -- 72.09

`truncate()` function - simply discards the unwanted digits without rounding

> Both truncate() and round() also allow a negative value for the second argument, meaning that numbers to the left of
> the decimal place are truncated or rounded

### Handling Signed Data

`sign()` function - returns `-1` if the number is negative, `0` if zero and `1` if positive
`abs()` function - returns absolute

    SELECT account_id, SIGN(balance), ABS(balance)
    FROM account;

## Working with Temporal Data

### Dealing with Time Zones

`utc_timestamp()` function (MySQL) - returns the current UTC timestamp

Check time zone setting:

    SELECT @@global.time_zone, @@session.time_zone;

### Generating Temporal Data

You can generate temporal data via any of the following means:

- Copying data from an existing `date`, `datetime`, or `time` column
- Executing a built-in function that returns a `date`, `datetime`, or `time`
- Building a string representation of the temporal data to be evaluated by the server

If the server is expecting a datetime value

    UPDATE rental
    SET return_date = '2019-09-17 15:30:00' -- datetime format: YYYY-MM-DD HH:MM:SS
    WHERE rental_id = 99999;

#### String-to-Date Conversions

If the server is not expecting a datetime value or if you would like to represent the datetime using a non default
format, you will need to tell the server to convert the string to a datetime

    SELECT CAST('2019-09-17 15:30:00' AS DATETIME) datetime_fld,
        CAST('108:17:57' AS TIME) time_fld;

> While some servers are quite strict regarding the date format, the MySQL server is quite lenient about the separators
> used between the components

For example, MySQL will accept all the following strings as valid representations of 3:30 P.M. on September 17, 2019:

    '2019-09-17 15:30:00'
    '2019/09/17 15:30:00'
    '2019,09,17,15,30,00'
    '20190917153000'

#### Functions for Generating Dates

If you need to generate temporal data from a string and the string is not in the proper form to use the cast() function,
you can use a built-in function that allows you to provide a format string along with the date string

`str_to_date()` function, the second argument defines the format of the date string (format in chap2)

    UPDATE rental
    SET return_date = STR_TO_DATE('Septemer 17, 2019', '%M %d, %Y')
    WHERE rental_id = 99999;

Generate _current_ date/time: `CURRENT_DATE()`, `CURRENT_TIME()`, `CURRENT_TIMESTAMP()`

### Manipulating Temporal Data

Take date arguments and return dates, strings, or numbers

#### Temporal Functions that return Dates

`date_add()` function - adds any kind of interval (days, months, years, ...) to a specific date. The second argument is
composed of three elements: the interval keyword, the desired quantity, and the type of interval

    SELECT DATE_ADD(CURRENT_DATE(), INTERVAL 5 DAY);

    UPDATE rental
    SET return_date = DATE_ADD(return_date, INTERVAL '3:27:11' HOUR_SECOND)
    WHERE rental_id = 99999;

`last_day()` function - return the final day of the month

    SELECT LAST_DAY('2019-09-17');
    /* 2019-09-30 */

> Whether you provide a `date` or `datetime` value, the `last_day()` function always returns a date

#### Temporal Functions that return Strings

`dayname()` function - determines which day of the week a certain date falls on
    
    SELECT DAYNAME('2019-09-18');
    /* Wednesday */

`extract()` function (Recommended)

    SELECT EXTRACT(YEAR FROM '2019-09-18 22:19:05');
    -- the interval types same as date_add

#### Temporal Functions that return Numbers

`datediff()` function - determines the number of days between the two dates
    
    SELECT DATEDIFF('2019-09-03', '2019-06-21');
    /* 74 */

## Conversion Functions

`cast()` function

    SELECT CAST('1456328' AS SIGNED INTEGER); -- string to integer
