from flask import Blueprint, redirect, request, jsonify
from connect import get_db_connection
import json

notifications_blueprint = Blueprint('notifications', __name__)

# Visit an article by setting it to visited
@notifications_blueprint.route('/visit/<articleID>', methods=['POST'])
def visit(articleID):
    
    conn = get_db_connection()
    # Mark the article as visited
    with conn.cursor() as cur:
        markVisited = """UPDATE notifications SET Visited = TRUE WHERE ArticleID = %s"""
        cur.execute(markVisited, (articleID,))
        conn.commit()
    conn.close()

    return jsonify({'message': 'Notification marked as visited'}), 201

# Mark all articles as visited
@notifications_blueprint.route('/visitAll', methods=['POST'])
def visitAll():
    conn = get_db_connection()
    
    with conn.cursor() as cur:
        markAllVisited = """UPDATE notifications SET Visited = TRUE"""
        cur.execute(markAllVisited)
        conn.commit()

    conn.close()

    return jsonify({'message': 'All notifications marked as visited'}), 201

# Endpoint to get all unvisited articles that appear in notifications
@notifications_blueprint.route('/unvisitednotifications', methods = ['GET'])
def unvisitednotifications():
    conn = get_db_connection()

    articles = []
    
    with conn.cursor() as cur:
        query = """SELECT a.Title, a.ArticleURL, a.SourceID, a.PublishedDate, a.Authors, a.ImageURL, a.SentimentLabel, a.SentimentScore, a.OverallScore, a.Summary, a.Keywords, c.CompanyName, c.TickerCode
        FROM notifications JOIN article a ON notifications.articleID = a.articleID
        JOIN company c ON a.companyID = c.companyID
        WHERE Visited = FALSE
        ORDER BY publisheddate DESC"""

        cur.execute(query)
        
        data = cur.fetchall()
        for row in data:
                row_dict = dict(zip([column[0] for column in cur.description], row))
                articles.append(row_dict)
    conn.close()
    return articles


# Endpoint to get all articles that have appeared in notifications
@notifications_blueprint.route('/notifications', methods = ['GET'])
def notifications():
    conn = get_db_connection()
    
    with conn.cursor() as cur:
        query = """SELECT ("title", "articleurl", "sourceid", "publisheddate", "authors", "imageurl", "sentimentlabel", "sentimentscore", "overallscore", "summary", "keywords") 
        FROM notifications JOIN article ON notifications.articleID = article.articleID
        ORDER BY publisheddate DESC"""
        cur.execute(query)
        
        data = cur.fetchall()
    conn.close()
    return data


    