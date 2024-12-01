SELECT name,
CASE
    WHEN name IN ('English', 'Italian', 'French', 'German') THEN 'latin1'
    WHEN name IN ('Japanese', 'Mandarin') THEN 'utf8'
    ELSE 'Unknown'
END character_set
FROM language;
