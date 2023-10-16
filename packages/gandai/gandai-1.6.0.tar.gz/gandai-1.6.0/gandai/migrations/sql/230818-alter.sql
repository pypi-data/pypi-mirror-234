ALTER TABLE search ADD COLUMN fields JSONB DEFAULT '[]'::jsonb;
-- ALTER TABLE search DROP COLUMN client_domain;
-- ALTER TABLE search DROP COLUMN inclusion;
-- ALTER TABLE search DROP COLUMN exclusion;
-- ALTER TABLE search DROP COLUMN context;
-- ALTER TABLE search DROP COLUMN sort;

CREATE MATERIALIZED VIEW IF NOT EXISTS criteria AS
WITH RankedCriteria AS (
    SELECT *,
           ROW_NUMBER() OVER(PARTITION BY search_uid, domain ORDER BY created DESC) AS rank
    FROM event
    WHERE 
        type = 'criteria'       
)
SELECT 
	search_uid, actor_key, data, created
FROM RankedCriteria r
WHERE 
    rank = 1
;


CREATE MATERIALIZED VIEW IF NOT EXISTS maps AS
WITH RankedEvent AS (
    SELECT *,
           ROW_NUMBER() OVER(PARTITION BY search_uid, domain ORDER BY created DESC) AS rank
    FROM event
    WHERE 
        type = 'maps'       
)
SELECT 
	search_uid, actor_key, data, created
FROM RankedEvent r
WHERE 
    rank = 1
;

CREATE MATERIALIZED VIEW IF NOT EXISTS comment AS
SELECT 
    e.search_uid, 
    e.domain,
    to_jsonb(ARRAY_AGG(jsonb_build_object(
        'id', e.id,
        'actor_key', e.actor_key,
        'created', e.created,
        'author', a.name,
        'comment', e.data->>'comment'
    ))) AS comments
FROM event e
LEFT JOIN actor a ON e.actor_key = a.key
WHERE 
    e.type = 'comment'
GROUP BY e.search_uid, e.domain;

CREATE MATERIALIZED VIEW IF NOT EXISTS rating AS
WITH RankedRatings AS (
    SELECT *,
           ROW_NUMBER() OVER(PARTITION BY search_uid, domain ORDER BY created DESC) AS rr
    FROM event
    WHERE 
        type = 'rating'       
)
SELECT 
	r.rr,
    r.search_uid, 
    r.domain,
    (r.data->>'rating') AS rating
FROM RankedRatings r
WHERE 
    rr = 1
;