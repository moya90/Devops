# app.py - API REST para Catálogo de Películas
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# Configuración de la base de datos MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL', 
    'mysql+pymysql://root:password@db:3306/movies_catalog'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de la tabla Películas
class Pelicula(db.Model):
    __tablename__ = 'peliculas'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), nullable=False)
    categoria = db.Column(db.String(100), nullable=False)
    año = db.Column(db.Integer, nullable=False)
    director = db.Column(db.String(255), nullable=False)
    duracion = db.Column(db.Integer, nullable=False)  # en minutos
    calificacion = db.Column(db.Float, nullable=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'categoria': self.categoria,
            'año': self.año,
            'director': self.director,
            'duracion': self.duracion,
            'calificacion': self.calificacion,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'fecha_actualizacion': self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None
        }

# Crear las tablas en la base de datos
@app.before_first_request
def create_tables():
    db.create_all()

# Endpoint de salud de la API
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'OK',
        'message': 'API de Catálogo de Películas funcionando correctamente',
        'timestamp': datetime.utcnow().isoformat()
    }), 200

# GET /peliculas - Listar todas las películas
@app.route('/peliculas', methods=['GET'])
def get_peliculas():
    try:
        peliculas = Pelicula.query.all()
        return jsonify({
            'success': True,
            'data': [pelicula.to_dict() for pelicula in peliculas],
            'total': len(peliculas)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Error al obtener las películas',
            'message': str(e)
        }), 500

# ========================================
# NUEVA FUNCIONALIDAD - FASE 5
# Endpoint: /peliculas/top
# ========================================

@app.route('/peliculas/top', methods=['GET'])
def get_top_peliculas():
    """
    Devuelve las 5 películas con mejor calificación
    """
    try:
        peliculas = Pelicula.query.order_by(Pelicula.calificacion.desc()).limit(5).all()
        return jsonify({
            'success': True,
            'total': len(peliculas),
            'data': [p.to_dict() for p in peliculas],
            'message': 'Top 5 películas mejor calificadas'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Error al obtener el top de películas',
            'message': str(e)
        }), 500


# GET /peliculas/{id} - Obtener los detalles de una película por su ID
@app.route('/peliculas/<int:id>', methods=['GET'])
def get_pelicula(id):
    try:
        pelicula = Pelicula.query.get(id)
        if not pelicula:
            return jsonify({
                'success': False,
                'error': 'Película no encontrada'
            }), 404
        
        return jsonify({
            'success': True,
            'data': pelicula.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Error al obtener la película',
            'message': str(e)
        }), 500

# POST /peliculas - Agregar una nueva película
@app.route('/peliculas', methods=['POST'])
def create_pelicula():
    try:
        data = request.get_json()
        
        # Validar campos requeridos
        required_fields = ['nombre', 'categoria', 'año', 'director', 'duracion']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    'success': False,
                    'error': f'El campo {field} es requerido'
                }), 400
        
        # Validar tipos de datos
        if not isinstance(data['año'], int) or data['año'] < 1900 or data['año'] > 2030:
            return jsonify({
                'success': False,
                'error': 'El año debe ser un número entero entre 1900 y 2030'
            }), 400
            
        if not isinstance(data['duracion'], int) or data['duracion'] <= 0:
            return jsonify({
                'success': False,
                'error': 'La duración debe ser un número entero positivo (en minutos)'
            }), 400
        
        # Validar calificación si se proporciona
        if 'calificacion' in data and data['calificacion'] is not None:
            if not isinstance(data['calificacion'], (int, float)) or data['calificacion'] < 0 or data['calificacion'] > 10:
                return jsonify({
                    'success': False,
                    'error': 'La calificación debe ser un número entre 0 y 10'
                }), 400
        
        # Crear nueva película
        nueva_pelicula = Pelicula(
            nombre=data['nombre'],
            categoria=data['categoria'],
            año=data['año'],
            director=data['director'],
            duracion=data['duracion'],
            calificacion=data.get('calificacion')
        )
        
        db.session.add(nueva_pelicula)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Película creada exitosamente',
            'data': nueva_pelicula.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Error al crear la película',
            'message': str(e)
        }), 500

# PUT /peliculas/{id} - Actualizar los detalles de una película
@app.route('/peliculas/<int:id>', methods=['PUT'])
def update_pelicula(id):
    try:
        pelicula = Pelicula.query.get(id)
        if not pelicula:
            return jsonify({
                'success': False,
                'error': 'Película no encontrada'
            }), 404
        
        data = request.get_json()
        
        # Actualizar campos si se proporcionan
        if 'nombre' in data:
            pelicula.nombre = data['nombre']
        if 'categoria' in data:
            pelicula.categoria = data['categoria']
        if 'año' in data:
            if not isinstance(data['año'], int) or data['año'] < 1900 or data['año'] > 2030:
                return jsonify({
                    'success': False,
                    'error': 'El año debe ser un número entero entre 1900 y 2030'
                }), 400
            pelicula.año = data['año']
        if 'director' in data:
            pelicula.director = data['director']
        if 'duracion' in data:
            if not isinstance(data['duracion'], int) or data['duracion'] <= 0:
                return jsonify({
                    'success': False,
                    'error': 'La duración debe ser un número entero positivo (en minutos)'
                }), 400
            pelicula.duracion = data['duracion']
        if 'calificacion' in data:
            if data['calificacion'] is not None:
                if not isinstance(data['calificacion'], (int, float)) or data['calificacion'] < 0 or data['calificacion'] > 10:
                    return jsonify({
                        'success': False,
                        'error': 'La calificación debe ser un número entre 0 y 10'
                    }), 400
            pelicula.calificacion = data['calificacion']
        
        pelicula.fecha_actualizacion = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Película actualizada exitosamente',
            'data': pelicula.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Error al actualizar la película',
            'message': str(e)
        }), 500

# DELETE /peliculas/{id} - Eliminar una película
@app.route('/peliculas/<int:id>', methods=['DELETE'])
def delete_pelicula(id):
    try:
        pelicula = Pelicula.query.get(id)
        if not pelicula:
            return jsonify({
                'success': False,
                'error': 'Película no encontrada'
            }), 404
        
        db.session.delete(pelicula)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Película eliminada exitosamente'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Error al eliminar la película',
            'message': str(e)
        }), 500

# Manejo de errores 404
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint no encontrado'
    }), 404

# Manejo de errores 405 (método no permitido)
@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'success': False,
        'error': 'Método no permitido para este endpoint'
    }), 405

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)