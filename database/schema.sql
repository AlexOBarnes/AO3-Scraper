DROP TABLE IF EXISTS fanfic_category, fanfic_rating, fanfic_warning, fanfic_fandom, fanfic_tag;
DROP TABLE IF EXISTS category, rating, warning, fandom, tag, fanfic, author;

CREATE TABLE author(
    author_id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    author_name VARCHAR(255) NOT NULL
);

CREATE TABLE fanfic(
    date_posted TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    fanfic_id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    fanfic_name TEXT NOT NULL,
    comments INTEGER NOT NULL,
    language VARCHAR(255) NOT NULL,
    word_count INTEGER NOT NULL,
    hits INTEGER NOT NULL,
    fanfic_url VARCHAR(255) NOT NULL,
    kudos INTEGER NOT NULL,
    author_id BIGINT NOT NULL,
    FOREIGN KEY (author_id) REFERENCES author(author_id)
);

CREATE TABLE rating(
    rating_id SMALLINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    rating_name VARCHAR(255) NOT NULL
);

CREATE TABLE tag(
    tag_name VARCHAR(255) NOT NULL,
    tag_id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    tag_type VARCHAR(20) NOT NULL
);

CREATE TABLE category(
    category_name VARCHAR(255) NOT NULL,
    category_id SMALLINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY
);

CREATE TABLE warning(
    warning_id SMALLINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    warning_name VARCHAR(255) NOT NULL
);

CREATE TABLE fandom(
    fandom_name VARCHAR(255) NOT NULL,
    fandom_id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY
);

CREATE TABLE fanfic_warning(
    fanfic_warning_id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    warning_id SMALLINT NOT NULL,
    fanfic_id BIGINT NOT NULL,
    FOREIGN KEY (warning_id) REFERENCES warning(warning_id),
    FOREIGN KEY (fanfic_id) REFERENCES fanfic(fanfic_id)
);



CREATE TABLE fanfic_category(
    fanfic_id BIGINT NOT NULL,
    fanfic_category_id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    category_id SMALLINT NOT NULL,
    FOREIGN KEY (category_id) REFERENCES category(category_id),
    FOREIGN KEY (fanfic_id) REFERENCES fanfic(fanfic_id)
);

CREATE TABLE fanfic_rating(
    fanfic_id BIGINT NOT NULL,
    fanfic_rating_id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    rating_id SMALLINT NOT NULL,
    FOREIGN KEY (rating_id) REFERENCES rating(rating_id),
    FOREIGN KEY (fanfic_id) REFERENCES fanfic(fanfic_id)
);



CREATE TABLE fanfic_tag(
    fanfic_id BIGINT NOT NULL,
    fanfic_tag_id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    tag_id BIGINT NOT NULL,
    FOREIGN KEY (tag_id) REFERENCES tag(tag_id),
    FOREIGN KEY (fanfic_id) REFERENCES fanfic(fanfic_id)
);


CREATE TABLE fanfic_fandom(
    fandom_id BIGINT NOT NULL,
    fanfic_id BIGINT NOT NULL,
    fanfic_fandom_id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    FOREIGN KEY (fandom_id) REFERENCES fandom(fandom_id),
    FOREIGN KEY (fanfic_id) REFERENCES fanfic(fanfic_id)
);


INSERT INTO category (category_name)
VALUES 
('F/F'),
('F/M'),
('Gen'),
('M/M'),
('Multi'),
('Other');

INSERT INTO warning (warning_name)
VALUES 
('Creator Chose Not To Use Archive Warnings'),
('Graphic Depictions Of Violence'),
('Major Character Death'),
('No Archive Warnings Apply'),
('Rape/Non-Con'),
('Underage Sex');

INSERT INTO rating (rating_name)
VALUES
('Not Rated'),
('General Audiences'),
('Teen And Up Audiences'),
('Mature'),
('Explicit');

