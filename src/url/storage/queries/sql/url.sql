-- name: save_url!
-- Save url info in the database
insert into urls(long, short) 
values (:long_url, :short_url);

-- name: get_url^
select long
from urls
where short = :short_url;