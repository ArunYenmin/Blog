from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:yenmin123@localhost/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    parent = db.Column(db.Integer)
    created_date = db.Column(db.Date)
    modified_date = db.Column(db.Date)

    def __init__(self, title, parent, created_date, modified_date):
        self.title = title
        self.parent = parent
        self.created_date = created_date
        self.modified_date = modified_date

class CategoriesSchema(ma.Schema):
    class Meta:
        fields = ("title", "parent", "created_date", "modified_date")

categories_schema = CategoriesSchema()
categoriess_schema = CategoriesSchema(many=True)

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(1000000))
    category = db.Column(db.Integer, db.ForeignKey("categories.id"))
    img = db.Column(db.String(1000000))
    created_date = db.Column(db.Date)
    modified_date = db.Column(db.Date)

    def __init__(self, title, description, category, img, created_date, modified_date):
        self.title = title
        self.description = description
        self.category = category
        self.img = img
        self.created_date = created_date
        self.modified_date = modified_date

class PostsSchema(ma.Schema):
    class Meta:
        fields = ("title", "description", "category", "img", "created_date", "modified_date")

posts_schema = PostsSchema()
postss_schema = PostsSchema(many=True)

@app.errorhandler(405)
def handle_405_error(_error):
    return make_response(jsonify({'error':'check given method'}), 405)

@app.errorhandler(404)
def handle_404_error(_error):
    return make_response(jsonify({'error':'not found'}), 404)

@app.route('/create_a_category', methods = ['POST'])
def create_category():
    data = request.get_json()
    if not 'parent' in data:
        return jsonify({
            'error': 'Bad Request',
            'message': 'Some Field Is Missing'
        }), 400

    if not 'title' in data:
        return jsonify({
            'error': 'Bad Request',
            'message': 'Some Field Is Missing'
        }), 400

    if not 'created_date' in data:
        return jsonify({
            'error': 'Bad Request',
            'message': 'Some Field Is Missing'
        }), 400

    if not 'modified_date' in data:
        return jsonify({
            'error': 'Bad Request',
            'message': 'Some Field Is Missing'
        }), 400

    c = Categories(
        title=data['title'],
        parent=data['parent'],
        created_date=data['created_date'],
        modified_date=data['modified_date']
    )
    db.session.add(c)
    db.session.commit()

    if request.authorization and request.authorization.username == 'u' and request.authorization.password == 'a':
        return {
               'id': c.id, 'title': c.title, 'parent': c.parent, 'created_date': c.created_date,
               'modified_date': c.modified_date
           }, 201
    return make_response('authorization failed')

@app.route('/create_post', methods=['POST'])
def create_post():
    data = request.get_json()

    if not 'title' in data:
        return jsonify({
            'error': 'Bad Request',
            'message': 'Some Field Is Missing'
        }), 400

    if not 'description' in data:
        return jsonify({
            'error': 'Bad Request',
            'message': 'Some Field Is Missing'
        }), 400

    if not 'category' in data:
        return jsonify({
            'error': 'Bad Request',
            'message': 'Some Field Is Missing'
        }), 400

    if not 'img' in data:
        return jsonify({
            'error': 'Bad Request',
            'message': 'Some Field Is Missing'
        }), 400

    if not 'created_date' in data:
        return jsonify({
            'error': 'Bad Request',
            'message': 'Some Field Is Missing'
        }), 400

    if not 'modified_date' in data:
        return jsonify({
            'error': 'Bad Request',
            'message': 'Some Field Is Missing'
        }), 40

    d = Posts(
        title=data['title'],
        description=data['description'],
        category=data['category'],
        img=data['img'],
        created_date=data['created_date'],
        modified_date=data['modified_date']
    )
    db.session.add(d)
    db.session.commit()

    return jsonify({'message': "Post created!"})

@app.route('/categories', methods = ['GET'])
def get_categories():
    if request.authorization and request.authorization.username == 'u' and request.authorization.password == 'a':
        return jsonify([
            {
                'id': categories.id, 'title': categories.title, 'parent': categories.parent,
                'created_date': categories.created_date, 'modified_date': categories.modified_date
            } for categories in Categories.query.all()
        ])
    return make_response('authorization failed')

@app.route('/posts', methods = ['GET'])
def get_posts():
    if request.authorization and request.authorization.username == 'u' and request.authorization.password == 'a':
        return jsonify([
        {
            'id': posts.id, 'title': posts.title, 'description': posts.description, 'category': posts.category,
            'img': posts.img,
            'created_date': posts.created_date, 'modified_date': posts.modified_date
        } for posts in Posts.query.all()
    ])
    return make_response('authorization failed')

@app.route('/category/<id>', methods = ['GET'])
def get_category(id):
    categories = Categories.query.filter_by(id=id).first_or_404()
    if request.authorization and request.authorization.username == 'u' and request.authorization.password == 'a':
        return {
        'id': categories.id, 'title': categories.title, 'parent': categories.parent, 'created_date': categories.created_date, 'modified_date': categories.modified_date
    }
    return make_response('authorization failed')

@app.route('/post/<id>', methods = ['GET'])
def get_post(id):
    posts = Posts.query.filter_by(id=id).first_or_404()
    if request.authorization and request.authorization.username == 'u' and request.authorization.password == 'a':
        return jsonify({
        'id': posts.id, 'title': posts.title, 'description': posts.description, 'category': posts.category,
        'img': posts.img, 'created_date': posts.created_date, 'modified_date': posts.modified_date
    })
    return make_response('authorization failed')

@app.route('/category/<id>', methods=['PUT'])
def update_category(id):
    data = request.get_json()
    categories = Categories.query.filter_by(id=id).first_or_404()
    categories.title = data['title']
    categories.parent = data['parent']
    categories.created_date = data['created_date']
    categories.modified_date = data['modified_date']
    if 'parent' not in data:
        categories.parent = data['parent']
    db.session.commit()
    if request.authorization and request.authorization.username == 'u' and request.authorization.password == 'a':
        return jsonify({
        'id': categories.id,
        'title': categories.title,
        'parent': categories.parent,
        'created_date': categories.created_date,
        'modified_date': categories.modified_date
        })
    return make_response('authorization failed')

@app.route('/post/<id>', methods=['PUT'])
def update_post(id):
    data = request.get_json()
    posts = Posts.query.filter_by(id=id).first_or_404()
    posts.title = data['title']
    posts.description = data['description']
    posts.category = data['category']
    posts.img = data['img']
    posts.created_date = data['created_date']
    posts.modified_date = data['modified_date']

    if not posts:
        return jsonify({'message': 'Post cant update!'})

    posts.complete = True
    db.session.commit()

    return jsonify({'message': 'post item has been updated!'})

@app.route('/category/<id>', methods=['DELETE'])
def delete_categories(id):
    categories = Categories.query.filter_by(id=id).first_or_404()
    db.session.delete(categories)
    db.session.commit()
    if request.authorization and request.authorization.username == 'u' and request.authorization.password == 'a':
        return {
        'success' : 'Category deleted successfully'
    }
    return make_response('authorization failed')

@app.route('/post/<id>', methods=['DELETE'])
def delete_posts(id):
    posts = Posts.query.filter_by(id=id).first_or_404()
    db.session.delete(posts)
    db.session.commit()
    if request.authorization and request.authorization.username == 'u' and request.authorization.password == 'a':
        return {
        'success' : 'Post deleted successfully'
    }
    return make_response('authorization failed')

if __name__ == "__main__":
    app.run(debug=True)
#pattampoochi book, madhagu, nagila nagila