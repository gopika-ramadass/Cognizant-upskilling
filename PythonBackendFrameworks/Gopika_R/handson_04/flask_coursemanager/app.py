from flask import Flask, jsonify
from config import Config
from courses.routes import courses_bp

def create_app(config_class=Config):
    """
    Application Factory Pattern for creating Flask app instances.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Register Blueprints
    app.register_blueprint(courses_bp)

    # Step 45: Custom JSON Error Handlers (APIs should never return HTML error pages)
    @app.errorhandler(404)
    def handle_404(error):
        return jsonify({
            'status': 'error',
            'error_code': 404,
            'message': 'Requested resource or URL was not found'
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
    app.run(host='127.0.0.1', port=5000, debug=True)
