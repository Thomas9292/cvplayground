import os
from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template('home.html')


@app.context_processor
def override_url_for():
    '''
    Code to override url_for to expire css files. Tells browser to update style when
    changes have been made to css
    '''
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    '''
    Attaches timestamp to url
    '''
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


if __name__ == '__main__':
    app.run(debug=True)
