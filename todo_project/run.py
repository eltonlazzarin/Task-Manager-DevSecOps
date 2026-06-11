import os
from todo_project import app

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'False') == 'True'
    host = os.getenv('FLASK_RUN_HOST', '127.0.0.1')

    app.run(host=host, port=5000, debug=debug_mode)