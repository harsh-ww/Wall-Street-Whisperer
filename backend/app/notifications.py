from flask import Blueprint, redirect, request, jsonify
from connect import get_db_connection
import json

notifications_blueprint = Blueprint('notifications', __name__)

# Visit an article by setting it to visited and redirecting to its link
@notifications_blueprint.route('/visit/<articleID>', methods=['GET', 'POST'])
def visit(articleID):
    if request.method == 'GET':
        conn = get_db_connection()
        link = "http://localhost:5173/"

        with conn.cursor() as cur:
            # Redirect to the link of the article
            getLink = """SELECT ArticleURL FROM article WHERE ArticleID = %s"""
            cur.execute(getLink, (articleID,))
            link = cur.fetchone()[0]
        
        return redirect(link)
    
    if request.method == 'POST':
        conn = get_db_connection()
        # Mark the article as visited
        with conn.cursor() as cur:
            markVisited = """UPDATE notifications SET Visited = TRUE WHERE ArticleID = %s"""
            cur.execute(markVisited, (articleID,))
            conn.commit()

        return jsonify({'message': 'Notification marked as visited'}), 201

# Mark all articles as visited
@notifications_blueprint.route('/visitAll', methods=['POST'])
def visitAll():
    conn = get_db_connection()
    
    with conn.cursor() as cur:
        markAllVisited = """UPDATE notifications SET Visited = TRUE"""
        cur.execute(markAllVisited)
        conn.commit()

    return jsonify({'message': 'All notifications marked as visited'}), 201

# Endpoint to get all unvisited articles that appear in notifications
@notifications_blueprint.route('/unvisitednotifications', methods = ['GET'])
def unvisitednotifications():
    conn = get_db_connection()
    
    with conn.cursor() as cur:
        query = """SELECT ("title", "articleurl", "sourceid", "publisheddate", "authors", "imageurl", "sentimentlabel", "sentimentscore", "overallscore", "summary", "keywords") 
        FROM notifications JOIN article ON notifications.articleID = article.articleID
        WHERE Visited = FALSE
        ORDER BY publisheddate DESC"""

        cur.execute(query)
        
        data = cur.fetchall()
        return data


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
        return data


    