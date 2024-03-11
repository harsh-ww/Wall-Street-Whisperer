import notifications as notifications

class TestNotifications:
    def insert(self, test_db):
        """
        Insert sample data to the database
        """
        with test_db.cursor() as cur:
            cur.execute("""INSERT INTO company (CompanyID, CompanyName, CurrentScore, CommonName, TickerCode, Currency) VALUES
                        (1, 'Amazon.com Inc', 10, 'Amazon', 'AMZN','USD'),
                        (2, 'NVIDIA Corporation', 10, 'Nvidia', 'NVDA','USD')
                        """)
            cur.execute("""INSERT INTO article ("articleid", "title", "articleurl", "overallscore", "companyid") VALUES
                        (1,	'Amazon article one',	'https://google.com/',	100, 1),
                        (2,	'Nvidia article one',	'https://google.com/',	100, 2),
                        (3,	'Amazon article two',	'https://google.com/',	100, 1)
                        """)
            cur.execute("""INSERT INTO notifications ("notificationid", "articleid", "visited") VALUES
                        (10,	1,false),
                        (20,	2,false),
                        (30,	3,false)
                        """)
            test_db.commit()

    def test_visit(self, client, test_db):
        """
        Test if visiting a company mark it as visited
        """
        self.insert(test_db)

        # Make a post request to visit the article
        response = client.post('http://localhost:5000/visit/1',
                                content_type='application/json')

        assert response.status_code == 201

        with test_db.cursor() as cur:

            # Test if there is only one article marked as tracked
            cur.execute("""SELECT count(*) FROM notifications WHERE visited = True""")
            result = cur.fetchone()
            assert result[0] == 1

            # Test if the article is marked as tracked
            cur.execute("""SELECT visited FROM notifications WHERE articleid = 1""")
            result = cur.fetchone()
            assert result[0]

    def test_visitall(self, client, test_db):
        """
        Test if visiting all companies at once works
        """
        self.insert(test_db)

        # Make a post request to visit all articles
        response = client.post('http://localhost:5000/visitAll',
                                content_type='application/json')

        assert response.status_code == 201

        with test_db.cursor() as cur:

            # Test if all articles are marked as visited
            cur.execute("""SELECT count(*) FROM notifications WHERE visited = True""")
            result = cur.fetchone()
            assert result[0] == 3


    def test_show_unvisited(self, client, test_db):
        """
        Test if showing all unvisited notification article works
        """
        self.insert(test_db)

        # Mark one article as visited
        with test_db.cursor() as cur:
            cur.execute("""UPDATE notifications SET visited = True WHERE articleid = 1""")
            test_db.commit()
            
        # Check if the correct articles are displayed
        response = client.get('/unvisitednotifications')
        assert response.status_code == 200

        data = response.json
        assert len(data) == 2
        
        assert all("Amazon article one" not in data[i]['title'] for i in range(2))
