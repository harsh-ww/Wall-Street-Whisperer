-- User Profile

DROP TABLE IF EXISTS users CASCADE;
CREATE TABLE users (
    UserID SERIAL PRIMARY KEY,
    Username VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL,
    Password VARCHAR(255) NOT NULL
);

-- Companies

DROP TABLE IF EXISTS company CASCADE; 
CREATE TABLE company (
    CompanyID SERIAL PRIMARY KEY,
    CompanyName VARCHAR(255) NOT NULL,
    CommonName VARCHAR(255) NOT NULL,
    TickerCode VARCHAR(10) NOT NULL,
    Exchange VARCHAR(10) NOT NULL CHECK (Exchange IN ('NASDAQ', 'LSE', 'NYSE')), -- Need to add more exchanges here, not exhausted
    CurrentScore FLOAT
);


DROP TABLE IF EXISTS stock_price CASCADE;
CREATE TABLE stock_price (
    StockPriceID INT PRIMARY KEY,
    CompanyID INT,
    LiveStockPrice INT,
    Date DATE,
    FOREIGN KEY (CompanyID) REFERENCES company(CompanyID)
);

DROP TABLE IF EXISTS user_follows_company CASCADE;
CREATE TABLE user_follows_company (
    UserID INT,
    CompanyID INT,
    PRIMARY KEY (UserID, CompanyID),
    FOREIGN KEY (UserID) REFERENCES users(UserID),
    FOREIGN KEY (CompanyID) REFERENCES company(CompanyID)
);

-- News 

DROP TABLE IF EXISTS web_source CASCADE;
CREATE TABLE web_source (
    SourceID INT PRIMARY KEY,
    SourceName VARCHAR(255) NOT NULL,
    SourceURL VARCHAR(255) NOT NULL,
    Popularity INT,
    PopularityLastFetched TIMESTAMP
);

DROP TABLE IF EXISTS article CASCADE;
CREATE TABLE article (
    ArticleID INT PRIMARY KEY,
    Title VARCHAR(255) NOT NULL,
    SourceID INT,
    PublishedDate DATE,
    Sentiment INT,
    Summary TEXT,
    FOREIGN KEY (SourceID) REFERENCES web_source(SourceID)
);

DROP TABLE IF EXISTS social_post CASCADE;
CREATE TABLE social_post (
    SocialPostID SERIAL PRIMARY KEY,
    Published DATE,
    Sentiment INT,
    RawText TEXT,
    SourceID INT,
    FOREIGN KEY (SourceID) REFERENCES web_source(SourceID)
);
-- If you decide not to include social media, it may be better to delete the table mentioned above altogether (and naturally CompanySocialPosts as well)


-- Associating articles and social posts with companies 

DROP TABLE IF EXISTS company_articles CASCADE;
CREATE TABLE company_articles (
    CompanyID INT,
    ArticleID INT,
    PRIMARY KEY (CompanyID, ArticleID),
    FOREIGN KEY (CompanyID) REFERENCES company(CompanyID),
    FOREIGN KEY (ArticleID) REFERENCES article(ArticleID)
);

DROP TABLE IF EXISTS company_social_posts CASCADE;
CREATE TABLE company_social_posts (
    CompanyID INT,
    SocialPostID INT,
    PRIMARY KEY (CompanyID, SocialPostID),
    FOREIGN KEY (CompanyID) REFERENCES company(CompanyID),
    FOREIGN KEY (SocialPostID) REFERENCES social_post(SocialPostID)
);
