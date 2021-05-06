CREATE TABLE Business (
  business_id VARCHAR(50) PRIMARY KEY,
  business_name VARCHAR(255),
  address VARCHAR(255),
  state VARCHAR(10),
  is_open INT,
  stars FLOAT,
  review_count INT
);

COPY Business(business_id, business_name, address, state, is_open, stars, review_count)
FROM '/home/eren/Desktop/Dersler/DBMS/THE1/yelp_academic_dataset/yelp_academic_dataset_business.csv'
DELIMITER ','
CSV HEADER;


CREATE TABLE Users (
    user_id VARCHAR(55) PRIMARY KEY,
    user_name VARCHAR(55),
    review_count INT,
    yelping_since DATE,
    useful INT,
    funny INT,
    cool INT,
    fans INT,
    average_stars FLOAT
);

COPY Users(user_id, user_name, review_count, yelping_since, useful, funny, cool, fans, average_stars)
FROM '/home/eren/Desktop/Dersler/DBMS/THE1/yelp_academic_dataset/yelp_academic_dataset_user.csv'
DELIMITER ','
CSV HEADER;


CREATE TABLE Friend(
    user_id1 CHAR(55),
    user_id2 CHAR(55),
    FOREIGN KEY (user_id1)
                   REFERENCES Users(user_id),
    FOREIGN KEY (user_id2)
                   REFERENCES Users(user_id)
);

COPY Friend(user_id1, user_id2)
FROM '/home/eren/Desktop/Dersler/DBMS/THE1/yelp_academic_dataset/yelp_academic_dataset_friend.csv'
DELIMITER ','
CSV HEADER;


CREATE TABLE Review(
    review_id CHAR(55) PRIMARY KEY ,
    user_id CHAR(55),
    business_id CHAR(55),
    stars FLOAT,
    date DATE,
    useful INT,
    funny INT,
    cool INT,
    FOREIGN KEY (user_id)
                   REFERENCES Users(user_id),
    FOREIGN KEY (business_id)
                   REFERENCES Business(business_id)
)

COPY Review(review_id, user_id, business_id, stars, date, useful, funny, cool)
FROM '/home/eren/Desktop/Dersler/DBMS/THE1/yelp_academic_dataset/yelp_academic_dataset_reviewNoText.csv'
DELIMITER ','
CSV HEADER;


CREATE TABLE Tip (
    id SERIAL PRIMARY KEY ,
    bussines_id CHAR(55),
    user_id CHAR(55),
    date DATE,
    compliment_count INT,
    tip_text TEXT,
    FOREIGN KEY (user_id)
        REFERENCES Users(user_id),
    FOREIGN KEY (bussines_id)
                 REFERENCES Business(business_id)
);

COPY Tip(tip_text,date, compliment_count,bussines_id, user_id)
FROM '/home/eren/Desktop/Dersler/DBMS/THE1/yelp_academic_dataset/yelp_academic_dataset_tip.csv'
DELIMITER ','
CSV HEADER;
