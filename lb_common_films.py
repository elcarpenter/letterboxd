import requests

urlstring = 'https://letterboxd.com/elcarpenter/list/films-leaving-the-criterion-channel-at-the/'
response = requests.get(url=urlstring)
string = response.text

urlstring = 'https://letterboxd.com/thisisdrew/list/they-shoot-pictures-dont-they-1000-greatest-5/'
response = requests.get(url=urlstring)
otherString = response.text


def ID_title_rank(string, films, count):
    """
    Identify the title, film ID, and ranking on secondary list
    """
    ranked = string.find('list-number')
    init = 0
    test = 0

    nextstart = string.find('a class="next"')
    nextend = string.find('">Next</a>')
    link = 'https://letterboxd.com' + string[nextstart + 21:nextend]

    start = string.find('data-film-id=',init)
    end = string.find('</ul>',start + 1)

    while test != -1:
        films.append([])
        start1 = string.find('data-film-id=',init)
        end1 = string.find('"',start1+15)
        film_id = string[start1+14:end1]
        films[count].append(film_id)
        start1 = string.find('alt="',end1)
        end1 = string.find('"',start1+6)
        title = string[start1+5:end1]
        films[count].append(title)
        if ranked != -1:
            start1 = string.find('"list-number"',end1)
            end1 = string.find('<',start1 + 1)
            rank =string[start1 + 14:end1]
            films[count].append(rank)
        init = end1
        test = string.find('data-film-id=',end1,end)
        if test == -1 and nextstart == -1:
            return films
        count = count + 1

    if nextstart != -1:
        response = requests.get(url=link)
        string = response.text
        ID_title_rank(string, films, count)
    return films


def compare_lists(string, otherString):
    """
    Get list of films common to both LB lists.
    """
    films = []
    otherFilms =[]
    common = []
    films = ID_title_rank(string, films, 0)
    otherFilms = ID_title_rank(otherString, otherFilms, 0)

    count = 0

    for otherFilm in otherFilms:
        for film in films:
            if film[0] == otherFilm[0]:
                common.append([])
                common[count].append(otherFilm[2])
                common[count].append(otherFilm[1])
                count = count + 1
                break
    return common

compare = compare_lists(string, otherString)
for i in compare:
    print("#%s %s" % tuple(i))
