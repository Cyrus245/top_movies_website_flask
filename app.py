from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from models.movie import db, Movie
from forms.forms import EditForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456789'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movies.db"
Bootstrap(app)
db.init_app(app)

with app.app_context():
    # creating the db tables
    db.create_all()


@app.route('/')
def home():
    """This route handler renders the home page"""
    all_entry = db.session.query(Movie).all()

    return render_template('index.html', all_entry=all_entry)


@app.route('/test')
def test():
    new_entry = Movie(title="Phone Booth",
                      year=2002,
                      description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
                      rating=7.3,
                      ranking=10,
                      review="My favourite character was the caller.",
                      img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg")
    db.session.add(new_entry)
    db.session.commit()
    return "Successfully entry the information"


@app.route('/edit/<id>', methods=["POST", "GET"])
def edit(id):
    """This route handler edits the rating and review"""
    edit_form = EditForm()
    selected_movie = Movie.query.get(id)

    if edit_form.validate_on_submit():
        selected_movie.rating = edit_form.rating.data
        selected_movie.review = edit_form.review.data
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('edit.html', form=edit_form)


if __name__ == '__main__':
    app.run()
