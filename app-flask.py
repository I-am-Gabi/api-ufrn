from flask import Flask, render_template, redirect, request, session, Markup

from config import BaseConfig
from oauth_fiware import OAuth2

app = Flask(__name__)
app.config.from_object(BaseConfig)
auth_app = OAuth2()

@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/authenticate')
def authenticate():
    auth_url = auth_app.authorize_url()
    return redirect(auth_url)


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    error = request.args.get('error', '')
    if error:
        return "Error: " + error

    if request.method == 'GET':
        auth_code = request.args.get('code')
        token_dict = auth_app.get_token(auth_code)
        session['access_token'] = token_dict['access_token']
        session['expires_in'] = token_dict['expires_in']
        content_token = "access_token: {} </br> token_type: {} </br> expires_in: {} </br> refresh_token: {}".format(
            token_dict['access_token'], token_dict['token_type'], str(token_dict['expires_in']),
            token_dict['refresh_token']
        )
        return render_template('index.html', content=Markup(content_token))

@app.route('/get_info', methods=['GET', 'POST'])
def user_info():
    if 'access_token' not in session:
        error = 'You are not authenticated!'
        return render_template('index.html', error=error)

    error = request.args.get('error', '')
    if error:
        return "Error: " + error

    user_info = auth_app.get_info(session['access_token'])
    return render_template('index.html', content=user_info)

if __name__ == '__main__':
    app.run()
