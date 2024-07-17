from flask_blog import create_app
import os
# Command prompt method to run flask application

# (virtualenv) C:\Users\abc\Desktop\Python\flask_project>set FLASK_APP=flask_blog.py
# (virtualenv) C:j\Users\abc\Desktop\Python\flask_project>set FLASK_DEBUG=1
# (virtualenv) C:\Users\abc\Desktop\Python\flask_project>flask run
app = create_app()
if __name__ ==  '__main__':
    app.run(debug=True)