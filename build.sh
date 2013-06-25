#!/bin/bash

INSERT INTO `entity_movie`(  `entity_id`, `user_id`, `title`, `en_title`, `content`, `year`, `thumbnail`, `category`, `country`, `company`, `language`, `actor`, `director`, `writer`, `alias`, `release_date`, `runtime`)  (SELECT  id, 1, `title`, `en_title`,   `summary`,  `year`,  `logo`, `category`, `country`, `company`, `language`,  `actor`, `director`, '', cn_name,  `publish_time`, `runtime` FROM test.`lwj_movie` limit 30 )


./manage.py schemamigration pins --initial

python ../manage.py makemessages -l zh_CN

python ../manage.py compilemessages -l zh_CN
