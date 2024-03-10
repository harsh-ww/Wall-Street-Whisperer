from connect import get_db_connection
import routes.company_routes as company

class TestGetCompanyDetailsDb:
    # Inserts sample data into the database
    def insert(self):
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute("INSERT INTO company (CompanyName, CurrentScore, CommonName, TickerCode, Exchange, Currency) VALUES (%s, %s, %s, %s, %s, %s)", ('Tesco PLC', 100.5, 'Tesco', 'TSCO.LON', 'United Kingdom', 'GBX'))
            conn.commit()
        conn.close()


    def test_get_company_details_db_valid(self, clear_data):
        self.insert()
        result = company.get_company_details_db('TSCO.LON')
        assert result == {
            'tracked': True,
            'score': 100.5,
            'name': 'Tesco PLC'
        }
    
    def test_get_company_details_invalid(self, clear_data):
        result = company.get_company_details_db('MADEUP')

        assert result == {}




class TestSearchCompanyDB:
    # Inserts sample data into the database
    def insert(self):
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute("INSERT INTO company (CompanyName, CurrentScore, CommonName, TickerCode, Exchange, Currency) VALUES (%s, %s, %s, %s, %s, %s)", ('Tesco PLC', 100.5, 'Tesco', 'TSCO.LON', 'United Kingdom', 'GBX'))
            cur.execute("INSERT INTO company (CompanyName, CurrentScore, CommonName, TickerCode, Exchange, Currency) VALUES (%s, %s, %s, %s, %s, %s)", ('Amazon.com Inc', 100.5, 'Amazon', 'AMZN', 'NASDAQ', 'USD'))

            conn.commit()
        conn.close()
    
    def test_by_full_name(self, clear_data):
        self.insert()
        result = company.search_companies_db('Tesco')
        expected = [{
            'name': 'Tesco PLC',
            'ticker': 'TSCO.LON',
            'exchange': 'United Kingdom',
            'tracked': True
        }]

        assert result == expected
    
    def test_by_full_ticker(self, clear_data):
        self.insert()
        result = company.search_companies_db('TSCO.LON')
        expected = [{
            'name': 'Tesco PLC',
            'ticker': 'TSCO.LON',
            'exchange': 'United Kingdom',
            'tracked': True
        }]

        assert result == expected

    def test_by_partial_name(self, clear_data):
        self.insert()

        # Capitalised
        result = company.search_companies_db('Amaz')
        expected = [{
            'name': 'Amazon.com Inc',
            'ticker': 'AMZN',
            'exchange': 'NASDAQ',
            'tracked': True
        }]

        assert result == expected

        # Case insensitive
        result_ci = company.search_companies_db('amaz')

        assert result_ci == expected

    def test_by_partial_ticker(self, clear_data):
        self.insert()

        # Capitalised
        result = company.search_companies_db('TSC')
        expected = [{
            'name': 'Tesco PLC',
            'ticker': 'TSCO.LON',
            'exchange': 'United Kingdom',
            'tracked': True
        }]

        assert result == expected

        # Case insensitive
        result_ci = company.search_companies_db('amzn')
        expected_ci = [{
            'name': 'Amazon.com Inc',
            'ticker': 'AMZN',
            'exchange': 'NASDAQ',
            'tracked': True
        }]

        assert result_ci == expected_ci





