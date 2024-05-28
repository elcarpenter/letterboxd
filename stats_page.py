import requests

urlstring = 'https://letterboxd.com/elcarpenter/list/films-leaving-the-criterion-channel-at-the/'
response = requests.get(url=urlstring)
web_string = response.text


def get_ID_title(web_string, films, count):
    """
    Gather film IDs and film titles in LB list.
    """
    ranked = web_string.find('list-number')
    init = 0
    test = 0

    nextstart = web_string.find('a class="next"')
    nextend = web_string.find('">Next</a>')
    link = 'https://letterboxd.com' + web_string[nextstart + 21:nextend]

    start = web_string.find('data-film-id=',init)
    end = web_string.find('</ul>',start + 1)

    while test != -1:
        # Initialize the tuple
        films.append([])
        start1 = web_string.find('data-film-id=',init)
        end1 = web_string.find('"',start1+15)
        film_id = web_string[start1+14:end1]
        # Add film ID
        films[count].append(film_id)
        start1 = web_string.find('alt="',end1)
        end1 = web_string.find('"',start1+6)
        title = web_string[start1+5:end1]
        # Add title
        films[count].append(title)
        if ranked != -1:
            start1 = web_string.find('"list-number"',end1)
            end1 = web_string.find('<',start1 + 1)
        init = end1
        test = web_string.find('data-film-id=',end1,end)
        if test == -1 and nextstart == -1:
            return films
        count = count + 1

    if nextstart != -1:
        response = requests.get(url=link)
        web_string = response.text
        get_ID_title(web_string, films, count)
    return films

def stats_page(web_string):
    """
    Compares leaving films against all lists on the LB stats page
    """
    leaving_films = []
    leaving_films = get_ID_title(web_string, leaving_films, 0)

    stats_lists = {
        'Letterboxd': 'https://letterboxd.com/dave/list/official-top-250-narrative-feature-films/',
        'Oscars': 'https://letterboxd.com/jake_ziegler/list/academy-award-winners-for-best-picture/',
        'IMDb': 'https://letterboxd.com/dave/list/imdb-top-250/',
        'Box Office': 'https://letterboxd.com/matthew/list/box-office-mojo-all-time-worldwide/',
        'Sight & Sound': 'https://letterboxd.com/bfi/list/sight-and-sounds-greatest-films-of-all-time/',
        'AFI': 'https://letterboxd.com/moseschan/list/afi-100-years-100-movies/',
        'Edgar Wright': 'https://letterboxd.com/crew/list/edgar-wrights-1000-favorite-movies/',
        '1001 Movies': 'https://boxd.it/2JIM',
        'Documentaries': 'https://letterboxd.com/jack/list/official-top-250-documentary-films/',
        'Women': 'https://letterboxd.com/jack/list/women-directors-the-official-top-250-narrative/',
        'Animated': 'https://letterboxd.com/lifeasfiction/list/letterboxd-100-animation/',
        'Horror': 'https://letterboxd.com/darrencb/list/letterboxds-top-250-horror-films/',
        'Palme dOr': 'https://letterboxd.com/brsan/list/cannes-palme-dor-winners/',
        'Ebert': 'https://letterboxd.com/dvideostor/list/roger-eberts-great-movies/',
        'Black': 'https://letterboxd.com/jack/list/black-directors-the-official-top-100-narrative/',
        'Most Fans': 'https://letterboxd.com/jack/list/official-top-250-films-with-the-most-fans/',
        'Every Nominee': 'https://letterboxd.com/elcarpenter/list/every-best-picture-nominee/',
    }

    for name, link in stats_lists.items():
        urlstring = link
        response = requests.get(url=urlstring)
        movie_string = response.text
        movies = []
        movies = get_ID_title(movie_string, movies, 0)
        common_movies = []

        for leaving_film in leaving_films:
            for stat_film in movies:
                if leaving_film[0] == stat_film[0]:
                    common_movies.append(stat_film[1])
                    break
        print(name, common_movies)

stats_page(web_string)
