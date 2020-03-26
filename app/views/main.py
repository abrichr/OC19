from flask import render_template
from app import app


@app.route('/')
@app.route('/index')
def index():
    return render_template(
        'index.html',
        title='OnCOVID19 - Find problems, form teams, build solutions'
    )
