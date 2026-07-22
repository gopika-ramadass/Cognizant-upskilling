from flask import Flask, jsonify
from config import Config
from extensions import db, migrate
from courses.routes import courses_bp

def create_app(config_class=Config):
    """
    Application Factory Pattern integrating Flask-SQLAlchemy and Flask-Migrate.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints
    app.register_blueprint(courses_bp)

    # Custom 404 handler for HTML or JSON
    @app.errorhandler(404)
    def handle_404(error):
        # Handle Werkzeug NotFound exception or get_or_404
        return jsonify({
            'status': 'error',
            'error_code': 404,
            'message': getattr(error, 'description', 'Requested resource or URL was not found')
        }), 404

    @app.errorhandler(500)
    def handle_500(error):
        return jsonify({
            'status': 'error',
            'error_code': 500,
            'message': 'Internal Server Error'
        }), 500

    return app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='127.0.0.1', port=5000, debug=True)
