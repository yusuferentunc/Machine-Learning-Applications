/*Question 1*/
/*Trigger 1*/
CREATE FUNCTION trigf()
    RETURNS TRIGGER
    LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE users
    SET review_count = review_count + 1
    WHERE NEW.user_id = user_id;
    RETURN NULL;
END;
$$;

CREATE TRIGGER urc
    AFTER INSERT ON review
    FOR EACH ROW
        EXECUTE PROCEDURE trigf();



/*Trigger 2*/
CREATE FUNCTION trigf2()
    RETURNS TRIGGER
    LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM review WHERE review_id = NEW.review_id;
    DELETE FROM review WHERE user_id = NEW.user_id;
    DELETE FROM tip WHERE user_id = NEW.user_id;
    RETURN NULL;
END;
$$;

CREATE TRIGGER rsc
    BEFORE INSERT ON review
    FOR EACH ROW
    WHEN ( NEW.stars = 0 )
        EXECUTE PROCEDURE trigf2();

/*Question 2*/
/*View 1*/

CREATE VIEW BusinessCount AS
    SELECT review.business_id,business_name,COUNT(review_id)
    FROM review, business
    WHERE review.business_id = business.business_id
    GROUP BY review.business_id,business_name;
