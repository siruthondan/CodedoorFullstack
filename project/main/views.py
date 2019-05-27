# project/main/views.py


from flask import render_template, Blueprint, redirect, url_for, jsonify
from .forms import SearchForm
import json
import requests

main_blueprint = Blueprint('main', __name__,)


@main_blueprint.route('/', methods=('GET', 'POST'))
def search():
    form = SearchForm()
    if form.validate_on_submit():
        return search_results(form.searchterm.data)

    return render_template('main/index.html', form=form)


@main_blueprint.route("/results")
def search_results(search_query):
    return render_template('main/results.html', results= query_API(search_query),
                           query=search_query)


def query_API(searchterm):
    lmt = 10
    tenor_apikey = '4NVGKX55MSMJ'
    tenor_anon = '0361d5061be248679b8be21891021709'
    r = requests.get("https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s&anon_id=%s" % (searchterm, tenor_apikey, lmt, tenor_anon))
    if r.status_code == 200:
        top_8gifs = json.loads(r.content)
    else:
        top_8gifs = None
    top = top_8gifs["results"][0]["media"][0]["tinygif"]["url"]
    abc = len(top_8gifs['results'])
    imglist = []

    for i in range(abc):
        imglist.append(top_8gifs["results"][i]["media"][0]["tinygif"]["url"])

    return imglist
