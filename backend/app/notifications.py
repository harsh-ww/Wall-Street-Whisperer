"""
This module contains function that interact with the notifications table
Which is used to display notifications when a major story occurs
"""
from flask import Blueprint, jsonify
from connect import get_db_connection

notifications_blueprint = Blueprint("notifications", __name__)


@notifications_blueprint.route("/visit/<articleID>", methods=["POST"])
def visit(articleID):
    """
    Update an article notification to mark it as visited
    """

    conn = get_db_connection()
    # Mark the article as visited
    with conn.cursor() as cur:
        markVisited = """UPDATE notifications SET Visited = TRUE WHERE ArticleID = %s"""
        cur.execute(markVisited, (articleID,))
        conn.commit()

    return jsonify({"message": "Notification marked as visited"}), 201


@notifications_blueprint.route("/visitAll", methods=["POST"])
def visitAll():
    """
    Mark all notifications as visited
    """
    conn = get_db_connection()

    with conn.cursor() as cur:
        markAllVisited = """UPDATE notifications SET Visited = TRUE"""
        cur.execute(markAllVisited)
        conn.commit()

    return jsonify({"message": "All notifications marked as visited"}), 201


@notifications_blueprint.route("/unvisitednotifications", methods=["GET"])
def unvisitednotifications():
    """
    Endpoint to get all unvisited articles that appear in notifications
    """
    conn = get_db_connection()

    with conn.cursor() as cur:
        query = """SELECT ("title", "articleurl", "sourceid", "publisheddate", "authors", "imageurl", "sentimentlabel", "sentimentscore", "overallscore", "summary", "keywords") 
        FROM notifications JOIN article ON notifications.articleID = article.articleID
        WHERE Visited = FALSE
        ORDER BY publisheddate DESC"""

        cur.execute(query)

        data = cur.fetchall()
        return data


@notifications_blueprint.route("/notifications", methods=["GET"])
def notifications():
    """
    Endpoint to get all articles that have appeared in notifications
    So they can be displayed in the notifications tab
    """
    conn = get_db_connection()

    with conn.cursor() as cur:
        query = """SELECT ("title", "articleurl", "sourceid", "publisheddate", "authors", "imageurl", "sentimentlabel", "sentimentscore", "overallscore", "summary", "keywords") 
        FROM notifications JOIN article ON notifications.articleID = article.articleID
        ORDER BY publisheddate DESC"""
        cur.execute(query)

        data = cur.fetchall()
        return data
