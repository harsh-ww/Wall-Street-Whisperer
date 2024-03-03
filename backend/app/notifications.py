from flask import current_app, request, Blueprint, jsonify
from flask_mail import Message, Mail

notifications_blueprint = Blueprint('notifications', __name__)

# Endpoint to send email
@notifications_blueprint.route('/sendemail', methods = ['POST'])
def sendemail():

    # Create mail object
    mail = Mail(current_app)

    # Retrieve post data
    data = request.get_json()

    # Construct message 

    msg_recipients = data.get("recipients")  
    # Can be null
    if not msg_recipients:
        return jsonify({'message': 'No emails are sent'}), 200
    
    msg_title = "News article from your tracked companies"
    msg_body = "There is a news article from one of your tracked companies.\nClick the following link to view."
    msg = Message(msg_title, 
            recipients = msg_recipients)
    msg.body = msg_body

    try:
        # Send the mail
        mail.send(msg)
        return jsonify({'message': 'Emails successfully sent'}), 201

    except Exception as e:
        error = str(e)
        return jsonify({"error" : "Error sending emails: " + error}), 500