from project import app
import dotenv
import os

dotenv.load_dotenv()  # load FLASK_RUN_PORT

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("FLASK_RUN_PORT"))
