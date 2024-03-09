from flask import current_app, request, Blueprint, jsonify, render_template
from flask_mail import Message, Mail
from connect import get_db_connection
from services.AlphaVantageService import getCurrentStockPrice
import requests, json, logging, datetime

emails_blueprint = Blueprint('emails', __name__)

# Generate daily update email content
def daily_email_content():
    # Extract details about tracked companies
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur = conn.cursor()

        # Fetch company details from company table, currently it fetches all companies
        cur.execute("SELECT CompanyName, TickerCode FROM company ORDER BY CompanyName ASC")
        stock_data = [{"CompanyName":item[0], "TickerCode":item[1]} for item in cur.fetchall()]

        if not stock_data:
            return None
        
        else:
            current_date = datetime.datetime.now().date()
            # Add the price and change columns from the API call
            # These are the details displayed in the email
            for company in stock_data:
                stock = getCurrentStockPrice(company['TickerCode'])
                company['Price'] = float(stock['price'])
                company['Change'] = float(stock['change'])
            
                # Find the highest scoring article on the last 24 hours that belongs to that company
                # Add the article data to the company dictionary
                query = """SELECT Title, Articleurl, PublishedDate, Imageurl, Summary, OverallScore
                        FROM article JOIN company_articles ON article.articleID = company_articles.articleID 
                        JOIN company ON company_articles.companyID = company.companyID
                        WHERE CompanyName = %s AND PublishedDate = %s
                        ORDER BY ABS(OverallScore) DESC LIMIT 1
                        """
                
                cur.execute(query, (company['CompanyName'], current_date,))
                if cur.fetchall():
                    article = cur.fetchall()[0]

                    company["Title"] = article[0]
                    company["Articleurl"] = article[1]
                    company["PublishedDate"] = article[2]
                    company["Imageurl"] = article[3]
                    company["Summary"] = article[4]
                    company["OverallScore"] = float(article[5])

            
            return render_template("daily_email.html", stock_data = stock_data, date = current_date)

# Generate article email content
def article_email_content(articleList):

    # Extract articles from a list of article IDs supplied
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur = conn.cursor()

        query = """SELECT CompanyName, TickerCode, Title, Articleurl, PublishedDate, Imageurl, Summary, OverallScore
                FROM article JOIN company_articles ON article.articleID = company_articles.articleID 
                JOIN company ON company_articles.companyID = company.companyID
                WHERE article.articleID = ANY(%s)
                ORDER BY CompanyName ASC
                """
        
        cur.execute(query, (articleList,))

        # This is in the format of { name: [TickerCode, [{articles}] ] }
        company_article_data = {}

        for article in cur.fetchall():
            companyName = article[0]
            article_data = {} 
            # Modify this to control what to be displayed in the email
            article_data["Title"] = article[2]
            article_data["Articleurl"] = article[3]
            article_data["PublishedDate"] = article[4]
            article_data["Imageurl"] = article[5]
            article_data["Summary"] = article[6]
            article_data["OverallScore"] = float(article[7])

            if companyName not in company_article_data:
                company_article_data[companyName] = [article[1], [article_data]]  # The ticker code of company is stored in a tuple with articles

            else:
                company_article_data[companyName][1].append(article_data)


        return render_template("article_email.html", company_article_data = company_article_data)
        
# Endpoint to send daily update email
@emails_blueprint.route('/senddailyemail', methods = ['POST'])
def senddailyemail():

    # Create mail object
    mail = Mail(current_app)

    # Retrieve post data
    data = request.get_json()
    msg_recipients = data.get("recipients")  # Will be changed when users are implemented

    # Generate daily email content
    email_content = daily_email_content()

    # Dont send email if there are no users, or users do not follow any companies
    if not msg_recipients or not email_content:
        return jsonify({'message': 'No emails are sent'}), 200
    
    # Construct email
    msg_title = "Daily Stock Market Update"
    msg = Message(msg_title, recipients = msg_recipients)
    msg.html = email_content

    try:
        # Send the mail
        mail.send(msg)
        return jsonify({'message': 'Emails successfully sent'}), 201

    except Exception as e:
        error = str(e)
        return jsonify({"error" : "Error sending emails: " + error}), 500

# Endpoint to send article email, given a list of article IDs
@emails_blueprint.route('/sendarticleemail', methods = ['POST'])
def sendarticleemail():

    # Create mail object
    mail = Mail(current_app)

    # Retrieve post data
    data = request.get_json()
    msg_recipients = data.get("recipients")  
    articleList = data.get("articleList")

    # Generate article email content when given an article ID
    email_content = article_email_content(articleList)

    # Dont send email if there are no users
    if not msg_recipients:
        return jsonify({'message': 'No emails are sent'}), 200
    
    # Construct email
    msg_title = "News Article From Your Tracked Companies"
    msg = Message(msg_title, recipients = msg_recipients)
    msg.html = email_content

    try:
        # Send the mail
        mail.send(msg)
        return jsonify({'message': 'Emails successfully sent'}), 201

    except Exception as e:
        error = str(e)
        return jsonify({"error" : "Error sending emails: " + error}), 500
    

# CRON Job to send daily email every 23:59pm
def job():
    data = {'recipients':["stockapp220@gmail.com"]} #CHANGE

    response = requests.post('http://localhost:5000/senddailyemail',
                        content_type='application/json',
                        data = json.dumps(dict(data)))
    
    if response.status_code == 201:
        logging.info("Daily emails sent successfully.")
    else:
        logging.error("There is an error sending daily emails.")

if __name__ == "__main__":
    job()
