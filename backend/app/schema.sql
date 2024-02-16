--SELECT 'CREATE DATABASE db26'
--WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'db26')\gexec

-- User Profile

DROP TABLE IF EXISTS User CASCADE;
CREATE TABLE User (
    UserID INT PRIMARY KEY SERIAL,
    Username VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL,
    Password VARCHAR(255) NOT NULL
);

-- Companies

DROP TABLE IF EXISTS Company CASCADE; 
CREATE TABLE Company (
    CompanyID INT PRIMARY KEY,
    CompanyName VARCHAR(255) NOT NULL,
    TickerCode VARCHAR(10) NOT NULL,
    CurrentScore FLOAT
);


DROP TABLE IF EXISTS StockPrice CASCADE;
CREATE TABLE StockPrice (
    StockPriceID INT PRIMARY KEY,
    CompanyID INT,
    LiveStockPrice INT,
    Date DATE,
    FOREIGN KEY (CompanyID) REFERENCES Company(CompanyID)
);

DROP TABLE IF EXISTS UserFollowsCompany CASCADE;
CREATE TABLE UserFollowsCompany (
    UserID INT,
    CompanyID INT,
    PRIMARY KEY (UserID, CompanyID),
    FOREIGN KEY (UserID) REFERENCES User(UserID),
    FOREIGN KEY (CompanyID) REFERENCES Company(CompanyID)
);

-- News 

DROP TABLE IF EXISTS WebSource CASCADE;
CREATE TABLE WebSource (
    SourceID INT PRIMARY KEY,
    SourceName VARCHAR(255) NOT NULL,
    SourceURL VARCHAR(255) NOT NULL,
    Popularity INT,
    PopularityLastFetched INT
);

DROP TABLE IF EXISTS Article CASCADE;
CREATE TABLE Article (
    ArticleID INT PRIMARY KEY,
    Title VARCHAR(255) NOT NULL,
    SourceID INT,
    PublishedDate DATE,
    Sentiment INT,
    Summary TEXT,
    FOREIGN KEY (SourceID) REFERENCES WebSource(SourceID)
);

DROP TABLE IF EXISTS SocialPost CASCADE;
CREATE TABLE SocialPost (
    SocialPostID SERIAL PRIMARY KEY,
    Published DATE,
    Sentiment INT,
    RawText TEXT,
    SourceID INT,
    FOREIGN KEY (SourceID) REFERENCES WebSource(SourceID)
);
-- If you decide not to include social media, it may be better to delete the table mentioned above altogether (and naturally CompanySocialPosts as well)


-- Associating articles and social posts with companies 

DROP TABLE IF EXISTS CompanyArticles CASCADE;
CREATE TABLE CompanyArticles (
    CompanyID INT,
    ArticleID INT,
    PRIMARY KEY (CompanyID, ArticleID),
    FOREIGN KEY (CompanyID) REFERENCES Company(CompanyID),
    FOREIGN KEY (ArticleID) REFERENCES Article(ArticleID)
);

DROP TABLE IF EXISTS CompanySocialPosts CASCADE;
CREATE TABLE CompanySocialPosts (
    CompanyID INT,
    SocialPostID INT,
    PRIMARY KEY (CompanyID, SocialPostID),
    FOREIGN KEY (CompanyID) REFERENCES Company(CompanyID),
    FOREIGN KEY (SocialPostID) REFERENCES SocialPost(SocialPostID)
);
