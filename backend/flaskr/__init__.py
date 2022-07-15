import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import time

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_categories(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    categories = [category.format() for category in selection]
    current_categories = categories[start:end]

    return current_categories

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories', methods=['GET'])
    def retrieve_categories():
        selection = Category.query.order_by(Category.id).all()
        current_categories = paginate_categories(request, selection)
        
        if len(current_categories) == 0:
            abort(404)

        final_categories = {}
        for x in current_categories:
            final_categories.update({x['id']: x['type']})
           
        return jsonify({
            'success':True,
            'categories': final_categories,
            #'total_categories': len(Category.query.all())
        })

       #return 'Category %d' % category_id
    
    {
      "categories": {
          "1": "Science", 
          "2": "Art", 
          "3": "Geography", 
          "4": "History", 
          "5": "Entertainment", 
          "6": "Sports"
      }, 
      "success": True
  }

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions')
    def get_questions():

        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 10
        end = start + 10

        questions = Question.query.all()
        formatted_questions = [question.format() for question in questions]

        categories = Category.query.order_by(Category.id).all()
        current_categories = [category.format() for category in categories]
        
        final_categories = {}
        for x in current_categories:
            final_categories.update({x['id']: x['type']})

        return jsonify({
            'success': True,
            'questions': formatted_questions[start:end],
            'total_questions':len(formatted_questions),
            'categories': final_categories,
            'current_category': 1

            })
    #return app
  
  
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    
    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        #print('got here')
        try:
            #print(question_id)
            question = Question.query.get(id)

            #print(question)
                
            if question is None:
                abort(404)

            question.delete()
            #selection = Question.query.order_by(id).all()
            #current_questions = paginate_questions(request, selection)

            return jsonify ({
              'success': True,
               
            })

        except:
            abort(422)
        
    
    """
    '''deleted': question_id, 
              'questions': current_questions,
              'total_questions': len(Question.query.all())'''
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """    
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        #new_rating = body.get('rating', None)
        new_difficulty = body.get('difficulty', None)
        new_category = body.get('category', None)

        try:
            question = Question(question=new_question, answer=new_answer,
                                difficulty=new_difficulty, category=new_category)
            question.insert()

            return jsonify({
               'success': True,
            })

        except:
            abort(422)

  
    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        body = request.get_json()
        searchTerm = body.get("searchTerm", None)

        try:
            if searchTerm:
                search = "%{}%".format(searchTerm)
                questions = Question.query.filter(
                    Question.question.like(search)).all()
                current_questions = [question.format()
                                     for question in questions]

                return jsonify({
                    'success': True,
                    'questions': current_questions,
                    'total_questions': len(current_questions),
                })

        except:
            abort(422)
 
        
        
    {
    }

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions')
    def retreive_category_questions(category_id):
        page = request.args.get('page',1,type=int)

        current_category = Category.query.get(category_id)
        if current_category is None:
            abort(404)

        categories = Category.query.all()
        categories = [category.format() for category in categories]

        questions = Question.query.filter(Question.category == category_id).all()

        start = (page - 1) * QUESTIONS_PER_PAGE
        if(start > len(questions)):
            abort(404)
        end = start + QUESTIONS_PER_PAGE

        formatted_questions = [question.format() for question in questions[start:end]]
        return jsonify({
        'success':True,
        'questions':formatted_questions,
        'total_questions': len(questions),
        'current_category': current_category.format(),
        'categories': categories
    })
    
    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    
    @app.route('/quizzes', methods=['POST'])
    def get_quiz_question():

        body = request.get_json()

        previous_questions = body.get('previous_questions', None)
        quiz_category = body.get('quiz_category', None)

        try:
            if quiz_category['id']:
                questions = Question.query.filter(
                    Question.category == quiz_category['id']).all()
            else:
                questions = Question.query.all()

            current_questions = [question.format() for question in questions]

            newset = []
            for x in current_questions:
                if x['id'] not in previous_questions:
                    newset.append(x)

            if len(newset) is 0:
                return jsonify({
                    'success': True,
                    'question': None
                })

            return jsonify({
                'success': True,
                'question': newset[random.randint(0, len(newset)-1)]
            })

        except:
            abort(422)
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found_404(error):
        return jsonify({
            'success':False,
            'message':"Resource Not Found",
            'error':404
         }),404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success":False,
            "message": "Method Not Alowed",
            "error": 405
        }),405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(500)
    def server_error_500(error):
        return jsonify({
            'success':False,
            'message':"server error",
            'error':500
        }),500
   
 
    return app
