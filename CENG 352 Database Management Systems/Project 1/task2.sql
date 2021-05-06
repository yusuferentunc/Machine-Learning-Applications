/*Question 1*/
SELECT u.user_id, u.user_name, u.review_count-u.fans AS Difference
FROM Users u
WHERE u.review_count > u.fans AND u.user_id IN (
    SELECT r.user_id
    FROM Review r, Business b
    WHERE r.business_id = b.business_id AND b.stars > 3.5
    )
GROUP BY u.user_id
ORDER BY u.review_count-u.fans DESC, user_id  DESC;


/*Question 2*/
SELECT user_name,business_name, A.date, A.compliment_count
FROM Users u
RIGHT JOIN
(SELECT *
FROM Tip t, Business b
WHERE b.state = 'TX' AND t.bussines_id = b.business_id AND t.compliment_count > 2 AND b.is_open = 1
) A
ON A.user_id = u.user_id
ORDER BY A.compliment_count DESC, A.date DESC;


/*Question 3*/
SELECT user_name, A.count
FROM Users u
RIGHT JOIN
(SELECT user_id1, COUNT(user_id1) AS count
FROM Friend
GROUP BY user_id1
ORDER BY count DESC LIMIT 20) A
ON A.user_id1 = u.user_id
ORDER BY count DESC, user_name DESC;


/*Question 4*/
SELECT user_name, average_stars, yelping_since
FROM Users u
WHERE EXISTS
(SELECT *
FROM Review r, business b
WHERE r.user_id = u.user_id AND r.business_id = b.business_id AND r.stars < b.stars)
ORDER BY average_stars DESC, yelping_since DESC;


/*Question 5*/
SELECT bussines_id, business_name,state,stars
FROM tip t, business b
WHERE date > '2019-12-31' AND date < '2021-01-01' AND tip_text LIKE 'good' AND b.is_open = 1 AND t.bussines_id = b.business_id
GROUP BY bussines_id,business_name,state,stars
ORDER BY stars DESC, business_name DESC;


/*Question 6*/
SELECT user_name,yelping_since,average_stars
FROM Users,(
SELECT user_id1, MAX(avg_1 - avg_2) AS Difference
FROM (
    SELECT user_id1, user_id2, average_stars as avg_1
    FROM Friend
    LEFT JOIN
        (
        SELECT user_id, average_stars
        FROM Users
        ) A
        ON user_id1 = user_id) B
    LEFT JOIN
    (SELECT user_id ,average_stars AS avg_2
     FROM Users) C
ON user_id2 = C.user_id
GROUP BY user_id1) Result
WHERE Difference < 0 AND user_id = user_id1
ORDER BY average_stars DESC, yelping_since DESC;

/*Second Solution (I couldn't run due to long time computing)
SELECT user_name,yelping_since,average_stars
FROM Users u1, Friend f
WHERE u1.user_id = f.user_id1 AND u1.average_stars < ALL(
                                                        SELECT u2.average_stars
                                                        FROM Users u2
                                                        WHERE u2.user_id = f.user_id2);
*/



/*Question 7*/
SELECT state, AVG(stars) as Average
FROM Business
GROUP BY state
ORDER BY Average DESC LIMIT 10;


/*Question 8*/
SELECT *
FROM
    (SELECT EXTRACT(year from date) as Year, SUM(compliment_count)*100/COUNT(compliment_count) AS average_compliment_count
    FROM tip
    GROUP BY Year) Result
WHERE average_compliment_count > 0.99999
ORDER BY year ASC;


/*Question 9*/
SELECT user_name
FROM users, (
    SELECT user_id, MIN(b.stars) AS min_stars
    FROM Review r, business b
    WHERE r.business_id = b.business_id
    GROUP BY user_id
    ) U
WHERE U.min_stars > 3.5 AND users.user_id = U.user_id;


/*Question 10*/
SELECT business_name,year,average_stars
FROM(
SELECT subq.business_name, EXTRACT(year from date) as Year, AVG(review.stars) AS average_stars
FROM review,
    (SELECT business_id,business_name
    FROM business
    WHERE review_count > 1000) subq
WHERE review.business_id = subq.business_id
GROUP BY subq.business_id,subq.business_name,Year) D
WHERE average_stars > 3
ORDER BY Year ASC,business_name ASC;


/*Question 11*/
SELECT user_name,sum_useful,sum_cool,difference
FROM
    (SELECT r.user_id,u.user_name,SUM(r.useful) AS sum_useful, SUM(r.cool) AS sum_cool, SUM(r.useful)-SUM(r.cool) AS difference
    FROM review r, users u
    WHERE u.user_id = r.user_id
    GROUP BY r.user_id,u.user_name) subq
WHERE difference > 0
ORDER BY difference DESC, user_name DESC


/*Question 12*/
SELECT user_id1,user_id2,rdb.business_id,rdb.stars
    FROM
(SELECT *
FROM (SELECT *
FROM friend f
WHERE user_id1 NOT IN (SELECT user_id2 FROM friend f2 WHERE f.user_id2 = f2.user_id1) )friendf
INNER JOIN
    (SELECT user_id, business_id,stars
        FROM review
        ) rdb
ON rdb.user_id = user_id1) temp
INNER JOIN
    (SELECT user_id,business_id,stars
        FROM review
        ) rdb
ON temp.user_id2 = rdb.user_id AND temp.business_id = rdb.business_id AND temp.stars = rdb.stars;
ORDER BY business_id DESC, stars DESC;


/*Question 13*/
SELECT stars,state,count(business_id)
FROM business
WHERE is_open = 1
GROUP BY CUBE (stars,state);


/*Question 14*/
SELECT *
FROM
(SELECT user_id, user_name, review_count, fans, rank() OVER(PARTITION BY fans ORDER BY review_count DESC) as rank
FROM users
WHERE fans > 49 AND fans < 61 ) as result
WHERE rank < 4;



