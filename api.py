from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

tareas = {
    '1': {'tarea': 'Tarea 1'},
    '2': {'tarea': 'Tarea 2'}
}

def abort_tarea_no_existe(tarea_id):
    if tarea_id not in tareas:
        print(tareas)
        abort(404, message=f'Tarea {tarea_id} no existe')

parser = reqparse.RequestParser()
parser.add_argument('tarea')

class Tarea(Resource):
    def get(self, tarea_id):
        abort_tarea_no_existe(tarea_id)
        return tareas[tarea_id]
    
    def delete(self, tarea_id):
        abort_tarea_no_existe(tarea_id)
        del tareas[tarea_id]
        return '', 204

    def put(self, tarea_id):
        abort_tarea_no_existe(tarea_id)
        args = parser.parse_args()
        tarea = {'tarea': args['tarea']}
        tareas[tarea_id] = tarea
        return tarea, 201

class ListaTareas(Resource):
    def get(self):
        return tareas

    def post(self):
        args = parser.parse_args()
        tarea = {'tarea': args['tarea']}
        max_key = 0

        for key in tareas.keys():
            if max_key < int(key):
                max_key = int(key)

        tareas[str(max_key + 1)] = tarea
        return tarea, 201

api.add_resource(ListaTareas, '/tareas')
api.add_resource(Tarea, '/tareas/<tarea_id>')

if __name__ == '__main__':
    app.run(debug=True)
