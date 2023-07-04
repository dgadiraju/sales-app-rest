from flask import jsonify, request

from app import app
from app import db
from models.user import User


@app.route('/users')
def users():
    search_email = request.args.get('email', '')  

    if search_email:
        # Query the database and filter users based on the pattern match
        user_recs = db.session.query(User).filter(User.email.like(f'{search_email.lower()}%')).all()
    else:
        # Retrieve all users if no search query is provided
        user_recs = db.session.query(User).all()

    # below commented code throws error as the SQL Alchemy 
    # get response includes attributes such as _sa_instance_state. 
    # The values of these attributes are not JSON Serializable

    # users = list(map(lambda rec: rec.__dict__, user_recs))
    
    # Fix: We need to Serialize Database Model Objects to JSON
    users = []
    for user in user_recs:
        user.__dict__.pop('_sa_instance_state')
        users.append(user.__dict__)

    return jsonify(users), 200
    

@app.route('/user', methods=['GET', 'POST', 'DELETE'])
def user():
    id = request.args.get('id')
    if request.method == 'GET':
        if id:
            user = User.query.get(id)
            user.__dict__.pop('_sa_instance_state')
            return jsonify(user.__dict__), 200
    elif request.method == 'POST':
        id = request.form['id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        email = request.form['email']
        if id:
            user = User.query.get(id)
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.email = email
            db.session.commit()
            return jsonify({'message': 'User updated successfully...'}), 200
        else:
            user = User(
                first_name=first_name,
                last_name=last_name,
                username = username,
                email=email
            )
            db.session.add(user)
            db.session.commit()
            return jsonify({'message': 'User added successfully...'}), 200
    elif request.method == 'DELETE':
        if id:
            user = User.query.get(id)
            db.session.delete(user)
            db.session.commit()
            return jsonify({'message': 'User deleted successfully...'}), 200
