from flask import Flask, jsonify, request 
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Hello(Resource): 
  
    # corresponds to the GET request. 
    # this function is called whenever there 
    # is a GET request for this resource 
    def get(self): 
  
        return jsonify({'message': 'hello world'}) 
  
    # Corresponds to POST request 
    def post(self): 
          
        data = request.get_json()
        return jsonify({'data': data}), 201

# Resource to calculate a + b
class Add(Resource): 
  
    def get(self, a, b): 
  
        return jsonify({'a plus b': a + b})

# Resource to calculate a - b
class Subtract(Resource): 
  
    def get(self, a, b): 
  
        return jsonify({'a minus b': a - b})
   
# Resource to calculate a * b
class Multiply(Resource): 
  
    def get(self, a, b): 
  
        return jsonify({'a times b': a * b})
    
# Resource to calculate a * b
class Divide(Resource): 
  
    def get(self, a, b): 
  
        return jsonify({'a divided by b': a / b})

# Resource to calculate a % b 
class Modulus(Resource): 
  
    def get(self, a, b): 
  
        return jsonify({'square': a % b})

# Resource to calculate square 
class Square(Resource): 
  
    def get(self, num): 
  
        return jsonify({'a modulus b': num ** 2})

api.add_resource(Hello, '/') 
api.add_resource(Add, '/add/<int:a>/<int:b>')
api.add_resource(Subtract, '/subtract/<int:a>/<int:b>')
api.add_resource(Multiply, '/multiply/<int:a>/<int:b>')
api.add_resource(Divide, '/divide/<int:a>/<int:b>')
api.add_resource(Modulus, '/modulus/<int:a>/<int:b>')
api.add_resource(Square, '/square/<int:num>')


if __name__ == '__main__':
    app.run(debug = True)