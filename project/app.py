from flask import Flask
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'plyy_page'
app.permanent_session_lifetime = timedelta(minutes=30)

from views import logout, mypage, mypage_edit, mypage_edit_currentpw, mypage_edit_changepw, mypage_edit_nickname, login, curator, api_curator, like_curator, unlike_curator, like_plyy, unlike_plyy, signup, signup_email, signup_nickname, signup_final 
from views2 import main, plyy, search, api_main, api_plyy, api_c_plyy, api_search, api_like

app.register_blueprint(main, url_prefix='/')
app.register_blueprint(plyy, url_prefix='/plyy')
app.register_blueprint(search, url_prefix='/search')
app.register_blueprint(api_search, url_prefix='/api/search')
app.register_blueprint(api_like, url_prefix='/api/like')
app.register_blueprint(api_main, url_prefix='/api/main')
app.register_blueprint(api_plyy, url_prefix='/api/plyy')
app.register_blueprint(api_c_plyy, url_prefix='/api/c_plyy')
app.register_blueprint(login, url_prefix='/')
app.register_blueprint(signup, url_prefix='/')
app.register_blueprint(signup_email, url_prefix='/')
app.register_blueprint(signup_nickname, url_prefix ='/')
app.register_blueprint(signup_final, url_prefix='/')
app.register_blueprint(logout, url_prefix='/')
app.register_blueprint(mypage, url_prefix='/')
app.register_blueprint(mypage_edit, url_prefix='/')
app.register_blueprint(mypage_edit_currentpw, url_prefix='/')
app.register_blueprint(mypage_edit_changepw, url_prefix='/')
app.register_blueprint(mypage_edit_nickname, url_prefix='/')
app.register_blueprint(curator, url_prefix='/')
app.register_blueprint(api_curator, url_prefix='/')
app.register_blueprint(like_curator, url_prefix='/')
app.register_blueprint(unlike_curator, url_prefix='/')
app.register_blueprint(like_plyy, url_prefix='/')
app.register_blueprint(unlike_plyy, url_prefix='/')


if __name__ == "__main__":
    app.run(debug=True, port=5000)
