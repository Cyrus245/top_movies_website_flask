from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from models.movie import db, Movie
from forms.forms import EditForm, AddForm
from sqlalchemy import desc
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456789'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movies.db"
Bootstrap(app)
db.init_app(app)

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9"
                     ".eyJhdWQiOiIyZmQyNjY2NTRhODZhZDVkOGM2NmJhNzliZGZkMzM1NSIsInN1YiI6IjY1MmY4ZWExMzU4ZGE3NWI2MWY5ZWI2OSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.CkGh3hpKB4C3A-S0GJQ6G_NGmlGIxEhseSO-XfLRK_c"
}

with app.app_context():
    # creating the db tables
    db.create_all()


@app.route('/')
def home():
    """This route handler renders the home page"""
    # querying based on the highest ranking(desc to asc)
    all_entry = db.session.query(Movie).order_by(desc(Movie.rating)).all()

    for i in range(len(all_entry)):
        # making the ranking number
        all_entry[i].ranking = i + 1
    db.session.commit()

    return render_template('index.html', all_entry=all_entry)


@app.route('/edit/<id>', methods=["POST", "GET"])
def edit(id):
    """This route handler edits the rating and review"""

    edit_form = EditForm()
    selected_movie = Movie.query.get(id)

    if edit_form.validate_on_submit():
        selected_movie.rating = float(edit_form.rating.data)
        selected_movie.review = edit_form.review.data
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('edit.html', form=edit_form)


@app.route('/delete/<id>')
def delete(id):
    """This route handler deletes a movie from db"""

    item_to_delete = Movie.query.get(id)
    db.session.delete(item_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/add', methods=['GET', 'POST'])
def add_entry():
    """This route handler adds movie data into db"""
    add_form = AddForm()
    if add_form.validate_on_submit():
        movie_name = add_form.title.data
        url = f"https://api.themoviedb.org/3/search/movie?query={movie_name}&include_adult=false&language=en-US&page=1"
        all_data = requests.get(url, headers=headers).json()['results']
        return render_template('select.html', search_result=all_data)
    return render_template('add.html', form=add_form)


@app.route('/details/<movie_api_id>')
def get_details(movie_api_id):
    """This route handler fetches the details and saves it to db"""

    url = f"https://api.themoviedb.org/3/movie/{movie_api_id}?language=en-US"
    detailed_data = requests.get(url, headers=headers).json()
    new_entry = Movie(title=detailed_data['original_title'],
                      year=detailed_data['release_date'].split('-')[0],
                      description=detailed_data['overview'],
                      img_url=f"https://image.tmdb.org/t/p/w500/{detailed_data['poster_path']}")
    db.session.add(new_entry)
    db.session.commit()
    return redirect(url_for('edit', id=new_entry.id))


if __name__ == '__main__':
    app.run(debug=True)
