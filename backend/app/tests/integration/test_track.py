import requests
import json 


def track(client, data):
        """
        Method to track a company
        """
        response = client.post('http://localhost:5000/track',
                                content_type='application/json',
                                data = json.dumps(dict(data)))
        return response

def untrack(client, data):
        """
        Method to untrack a company
        """
        response = client.post('http://localhost:5000/untrack',
                                content_type='application/json',
                                data = json.dumps(dict(data)))
        return response

class TestTrack:
    def test_track_valid(self, client, test_db):
        """
        Test if user can track a company and if the data is correctly added to database
        """
        common_name = "Amazon"
        ticker_code = "AMZN"

        data = {'common_name': common_name, 'ticker_code': ticker_code}

        # Make a post request to track company
        response = track(client, data)

        # Test if the post request was successful
        assert response.status_code == 201

        with test_db.cursor() as cur:
            # Check if the data has exactly one row
            cur.execute('SELECT COUNT(*) FROM company WHERE Tracked=True')
            rows_count = cur.fetchone()
            assert rows_count[0] == 1

            # Check if the company data is present in the database
            cur.execute('SELECT CompanyName, TickerCode FROM company LIMIT 1')
            rows = cur.fetchone()
            assert rows[0] == "Amazon.com Inc"
            assert rows[1] == "AMZN"

    def test_track_already_tracked(self, client, test_db):
        """
        Test if a user cannot click track twice to track an already tracked company
        """
        common_name = "Amazon"
        ticker_code = "AMZN"

        data = {'common_name': common_name, 'ticker_code': ticker_code}

        # Make a post request to track company
        response = track(client, data)
        assert response.status_code == 201

        # Make the same post request again
        response_invalid = track(client, data)
        assert response_invalid.status_code == 409
        assert response_invalid.json == {'error': 'Company already tracked'}

        # Test that it does not add duplicated data to the database
        with test_db.cursor() as cur:
            # Check if the data has exactly one row
            cur.execute('SELECT COUNT(*) FROM company WHERE Tracked=True')
            rows_count = cur.fetchone()
            assert rows_count[0] == 1

class TestUntrack:
    def insert(self, test_db):
        """
        Insert company data into database
        """
        with test_db.cursor() as cur:
            cur.execute("INSERT INTO company (CompanyName, CurrentScore, CommonName, TickerCode, Currency) VALUES (%s, %s, %s, %s, %s)", 
                        ('Amazon.com Inc', 10, 'Amazon', 'AMZN','USD'))
            test_db.commit()

    def test_untrack(self, client, test_db):
        """
        Test if user can untrack a company and if the data is correctly removed from database
        """
        self.insert(test_db)

        common_name = "Amazon"
        ticker_code = "AMZN"

        data = {'common_name': common_name, 'ticker_code': ticker_code}

        # Make a post request to untrack company
        response = untrack(client, data)

        # Test if the post request was successful
        assert response.status_code == 204

        with test_db.cursor() as cur:
            # Check if the data has no rows now
            cur.execute('SELECT COUNT(*) FROM company WHERE Tracked=True')
            assert not cur.fetchone()[0]

    def test_untrack_invalid(self, client, test_db):
        """
        Test if user cannot untrack a company that is not tracked
        """
        common_name = "Amazon"
        ticker_code = "AMZN"

        data = {'common_name': common_name, 'ticker_code': ticker_code}

        # Make a post request to untrack company
        response = untrack(client, data)

        # Test if the post request was successful
        assert response.status_code == 400

        assert response.json == {'error': 'Ticker AMZN is not tracked'}
