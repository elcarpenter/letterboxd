import requests
import time

# Takes the URL of a user's "FILMS" section of their profile and creates a ranked list of
# the user's favorite directors, based on the user's average rating of the director's films.

urlstring = 'https://letterboxd.com/elcarpenter/films/?filters=hide-shorts+hide-tv'
response = requests.get(url=urlstring)
string = response.text

def get_director(link):
    """
    Visit film page to access director(s).
    """
    urlstring = 'https://letterboxd.com' + link
    response = requests.get(url=urlstring)
    string = response.text

    # Get director
    start1 = string.find('Directed by" /><meta name="twitter:data1" content="', 0)
    end1 = string.find('"',start1+52)
    directors = string[start1+51:end1]

    return directors

def director_data(string, director_dict):
    """
    Create director dictionary with names and ratings.
    """
    init = 0
    test = 0

    nextstart = string.find('a class="next"')
    nextend = string.find('">Older</a>')
    link = 'https://letterboxd.com' + string[nextstart + 21:nextend] + "?filters=hide-shorts+hide-tv"

    start = string.find('data-film-id=',init)
    end = string.find('</ul>',start + 1)

    while test != -1:

        # Get film id
        start1 = string.find('data-film-id=',init)
        end1 = string.find('"',start1+15)
        # film_id = string[start1+14:end1]

        # Get film url
        start1 = string.find('data-target-link=', end1)
        end1 = string.find('"', start1+19)
        film_url = string[start1+18:end1]

        # Get title and director(s)
        start1 = string.find('alt="',end1)
        end1 = string.find('"',start1+6)
        title = string[start1+5:end1]
        director = get_director(film_url)

        # Get the rating
        start1 = string.find(' rated-',end1)
        end1 = string.find('"',start1+8)
        rating = string[start1+7:end1]
        rating = int(rating)

        # Add to dictionary
        if isinstance(director, list):
            # Protect Scorsese and Tarantino
            if title != "Four Rooms" or title != "New York Stories":
                for direct in director:
                    if direct in director_dict:
                        director_dict[dir].append(rating)
                    else:
                        director_dict[dir] = [rating]
        else:
            if director in director_dict:
                director_dict[director].append(rating)
            else:
                director_dict[director] = [rating]


        init = end1
        test = string.find('data-film-id=',end1,end)
        if test == -1 and nextstart == -1:
            return director_dict

    if nextstart != -1:
        response = requests.get(url=link)
        string = response.text
        time.sleep(5)
        director_data(string, director_dict)
    return director_dict

director_dict = {}
director_data(string, director_dict)

def get_director_ranking(director_dict):
    "Calculate average and rank accordingly"
    ranking = []
    for director in director_dict.keys():
        num = len(director_dict[director])
        avg = sum(director_dict[director]) / num

        # Add .1 for every 10 films seen
        if num >= 10:
            avg = avg + (num // 10 * .1)

        # Minimum of 5 movies to make the list
        if num > 4:
            ranking.append([director, round(avg / 2, 3), num])

    count = 0
    # Sort highest to lowest by avg rating
    ranking.sort(reverse=True, key=lambda x: x[1])
    for item in ranking:
        count = count + 1
        print(f'{count}. {item[0]} - {item[1]} avg ({item[2]} films)')

get_director_ranking(director_dict)
