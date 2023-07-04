from flask import jsonify, request

from app import app
from app import db
from models.course import Course


@app.route('/courses')
def courses():
    search_query = request.args.get('search', '')

    if search_query:
        # Query the database for courses matching the search query
        course_recs = db.session. \
            query(Course). \
            filter(Course.course_name.ilike(f"%{search_query}%")). \
            all()
    else:
        # Query the database for all courses
        course_recs = db.session.query(Course).all()

    courses = []
    for course in course_recs:
        course.__dict__.pop('_sa_instance_state')
        courses.append(course.__dict__)
    return jsonify(courses), 200


@app.route('/course', methods=['GET', 'POST', 'DELETE'])
def course():
    course_id = request.args.get('course_id')
    if request.method == 'GET':
        if course_id:
            course = Course.query.get(course_id)
            course.__dict__.pop('_sa_instance_state')
            return jsonify(course.__dict__), 200
    elif request.method == 'POST':
        course_id = request.form['course_id']
        course_name = request.form['course_name']
        course_author = request.form['course_author']
        course_endpoint = request.form['course_endpoint']
        if course_id:
            course = Course.query.get(course_id)
            course.course_name = course_name
            course.course_author = course_author
            course.course_endpoint = course_endpoint
            db.session.commit()
            return jsonify({'message': 'Course updated successfully...'}), 200
        else:
            course = Course(
                course_name=course_name,
                course_author=course_author,
                course_endpoint=course_endpoint,
            )
            db.session.add(course)
            db.session.commit()
            return jsonify({'message': 'Course added successfully...'}), 200
    elif request.method == 'DELETE':
        if course_id:
            course = Course.query.get(course_id)
            db.session.delete(course)
            db.session.commit()
            return jsonify({'message': 'Course deleted successfully...'}), 200