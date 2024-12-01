SELECT actor_role.name, actor_level.level, actor_role.num_roles
FROM (
    SELECT CONCAT(a.first_name, ' ', a.last_name) name,
       count(*) num_roles
    FROM actor a
        INNER JOIN film_actor fa
            ON a.actor_id = fa.actor_id
    GROUP BY a.actor_id
) actor_role INNER JOIN (
    SELECT 'Hollywood Star' level, 30 min_roles, 99999 max_roles
    UNION ALL
    SELECT 'Prolific Actor' level, 20 min_roles, 29 max_roles
    UNION ALL
    SELECT 'Newcomer' level, 1 min_roles, 19 max_roles
) actor_level
ON actor_role.num_roles BETWEEN actor_level.min_roles AND actor_level.max_roles
ORDER BY actor_role.name;