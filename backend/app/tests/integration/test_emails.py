import json
import emails as emails
import datetime

class TestDailyEmail:
    def insert(self, test_db):
        """
        Insert company data into database to mark it as tracked
        """
        with test_db.cursor() as cur:
            cur.execute("""INSERT INTO company (CompanyName, CurrentScore, CommonName, TickerCode, Currency) VALUES
                        ('Amazon.com Inc', 10, 'Amazon', 'AMZN','USD'),
                        ('NVIDIA Corporation', 10, 'Nvidia', 'NVDA','USD')""")

            test_db.commit()

    def remove(self, test_db):
        """
        Remove amazon to mark it as untracked
        """
        with test_db.cursor() as cur:
            cur.execute("DELETE FROM company WHERE TickerCode = %s", ('AMZN',))
            test_db.commit()
        
    def test_daily_email_follow(self, client, test_db, test_app_context):
        """
        Test if the company appears in the daily email if it is followed
        """
        # Insert data to mark the companies as tracked
        self.insert(test_db)

        # Check if the correct company names are in the email
        content = emails.daily_email_content()
        assert "Amazon.com Inc" in content
        assert "NVIDIA Corporation" in content

        # Check if the correct date is displayed
        current_date = datetime.datetime.now().date()
        assert str(current_date) in content


    def test_daily_email_unfollow(self, test_db, test_app_context):
        """
        Test if the company no longer appears in daily emails after 
        the user unfollows a company
        """
        # Insert data to mark the companies as tracked
        self.insert(test_db)

        # Remove amazon company
        self.remove(test_db)

        # Check if the correct company names are in the email
        content = emails.daily_email_content()
        assert "Amazon.com Inc" not in content
        assert "NVIDIA Corporation" in content


class TestArticleEmail:
    def insert(self, test_db):
        """
        Insert news articles to be displayed in the email
        """
        with test_db.cursor() as cur:
            # Insert 2 companies
            cur.execute("""INSERT INTO company (CompanyID, CompanyName, CurrentScore, CommonName, TickerCode, Currency) VALUES
                        (1, 'Amazon.com Inc', 10, 'Amazon', 'AMZN','USD'),
                        (2, 'NVIDIA Corporation', 10, 'Nvidia', 'NVDA','USD'),
                        (3, 'Apple Inc', 10, 'Apple', 'AAPL','USD')
                        """)
            
            cur.execute("""INSERT INTO article ("articleid", "title", "articleurl", "overallscore", "companyid") VALUES
                        (1,	'Amazon article one',	'https://google.com/',	100, 1),
                        (2,	'Nvidia article one',	'https://google.com/',	100, 2),
                        (3,	'Amazon article two',	'https://google.com/',	100, 1),
                        (4,	'Amazon unselected article',	'https://google.com/',	10, 1)
                        """)

            test_db.commit()

    def test_article_email_group(self, test_db, test_app_context):
        """
        Test if the article email content can group companies together
        """
        # Insert article data 
        self.insert(test_db)

        # Check if the correct company names has appeared only once
        article_list = [1,2,3]
        content = emails.article_email_content(article_list)

        assert len(content.split("Amazon.com Inc")) == 2
        assert len(content.split("NVIDIA Corporation")) == 2

        # Check if companies that are not related are not in the email content
        assert "Apple Inc" not in content

    def test_article_content(self, test_db, test_app_context):
        """
        Test if only articles identified as important are shown
        """
        # Insert article data 
        self.insert(test_db)

        # Check if the correct article titles are displayed
        article_list = [1,2,3]
        content = emails.article_email_content(article_list)

        assert "Amazon article one" in content
        assert "Amazon article two" in content
        assert "Nvidia article one" in content
        assert "Amazon unselected article" not in content

class TestEndPoints:
    def insert(self, test_db):
        """
        Insert news articles to be displayed in the email
        """
        with test_db.cursor() as cur:
            cur.execute("""INSERT INTO company (CompanyID, CompanyName, CurrentScore, CommonName, TickerCode, Currency) VALUES
                        (1, 'Amazon.com Inc', 10, 'Amazon', 'AMZN','USD')
                        """)
            
            cur.execute("""INSERT INTO article ("articleid", "title", "articleurl", "overallscore", "companyid") VALUES
                        (1,	'Amazon article one',	'https://google.com/',	100, 1)
                        """)

            test_db.commit()

    def test_daily_email_endpoint(self, client, test_db, test_app_context):
        """
        Test if the daily email endpoint works
        """
        self.insert(test_db)
        data_daily = {'recipients':["stockapp220@gmail.com"]}

        # Make a post request to send daily email
        response_daily = client.post('http://localhost:5000/senddailyemail',
                                content_type='application/json',
                                data = json.dumps(dict(data_daily)))

        assert response_daily.status_code == 201
        assert response_daily.json == {'message': 'Emails successfully sent'}

    def test_daily_email_endpoint_no_company(self, client, test_db, test_app_context):
        """
        Test if no emails are sent if the user does not follow any company
        """
        data_daily = {'recipients':["stockapp220@gmail.com"]}

        # Make a post request to send daily email
        response_daily = client.post('http://localhost:5000/senddailyemail',
                                content_type='application/json',
                                data = json.dumps(dict(data_daily)))

        assert response_daily.json == {'message': 'No emails are sent'}

    def test_article_email_endpoint(self, client, test_db, test_app_context):
        """
        Test if article email endpoint works
        """
        self.insert(test_db)
        data_article = {'recipients':["stockapp220@gmail.com"], 'articleList':[1]}

        # Make a post request to send article email
        response_article = client.post('http://localhost:5000/sendarticleemail',
                                content_type='application/json',
                                data = json.dumps(dict(data_article)))

        assert response_article.status_code == 201
        assert response_article.json == {'message': 'Emails successfully sent'}

    def test_article_email_endpoint_no_article(self, client, test_db, test_app_context):
        """
        Test if no article emails are sent if there are no important articles
        """
        data_article = {'recipients':["stockapp220@gmail.com"], 'articleList':[]}

        # Make a post request to send article email
        response_article = client.post('http://localhost:5000/sendarticleemail',
                                content_type='application/json',
                                data = json.dumps(dict(data_article)))

        assert response_article.json == {'message': 'No emails are sent'}