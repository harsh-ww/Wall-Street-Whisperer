from flask import Flask, request, jsonify
from connect import get_db_connection

app = Flask(__name__)

@app.route('/get_articles', methods=['GET'])
def get_articles():
    try:
        company_id = request.args.get('company_id')  #assuming we pass the arguments company_id (CompanyID) from the company_articles table and from_date (PublishedDate) from the article table
        from_date = request.args.get('from_date')

        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            SELECT a.* 
            FROM article a
            JOIN company_articles ca ON a.ArticleID = ca.ArticleID
            WHERE ca.CompanyID = %s AND a.PublishedDate >= %s
        """
        cursor.execute(query, (company_id, from_date))
        articles = cursor.fetchall()

        conn.close()

        result = [{'ArticleID': article[0], 'Title': article[1], 'PublishedDate': article[3]} for article in articles]

        return jsonify(result)

    except Exception as e:
        print("An error occurred:", e)
        return jsonify({'error': 'An error occurred'}), 500

if __name__ == '__main__':
    app.run(debug=True)
