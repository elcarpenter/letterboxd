import requests

urlstring = 'https://letterboxd.com/elcarpenter/list/the-criterion-channel-every-narrative-film/by/rating/'
response = requests.get(url=urlstring)
string = response.text

def get_num_ratings(link):
    """
    Retrieves the number of ratings (not watches) a film has.
    """
    urlstring = 'https://letterboxd.com' + link
    response = requests.get(url=urlstring)
    string = response.text

    # get rating count
    start1 = string.find('ratingCount', 0)
    end1 = string.find(',',start1+14)
    ratings = string[start1+13:end1]

    return ratings

def ID_Title_Rank(string, films, count):
    init = 0
    test = 0

    # Find next page
    nextstart = string.find('a class="next"')
    nextend = string.find('">Lower</a>')
    link = 'https://letterboxd.com' + string[nextstart + 21:nextend]

    start = string.find('data-film-id=',init)
    end = string.find('</ul>',start + 1)

    while test != -1:

        # Get film ID
        start1 = string.find('data-film-id=',init)
        end1 = string.find('"',start1+15)
        film_id = string[start1+14:end1]

        # Get film url
        start1 = string.find('data-target-link=', end1)
        end1 = string.find('"', start1+19)
        film_url = string[start1+18:end1]

        # Get the title
        start1 = string.find('alt="',end1)
        end1 = string.find('"',start1+6)
        title = string[start1+5:end1]
        ratings = int(get_num_ratings(film_url))
        if ratings < 10000:
            films.append([])
            films[count].append(film_id)
            films[count].append(title)
            films[count].append(film_url)
            count = count + 1
            print(count, title)
            if count == 100:
                return

        init = end1
        test = string.find('data-film-id=',end1,end)
        if (test == -1) and nextstart == -1:
            return films

    # Find next page
    if nextstart != -1:
        response = requests.get(url=link)
        string = response.text
        ID_Title_Rank(string, films, count)

films = []
ID_Title_Rank(string, films, 0)
