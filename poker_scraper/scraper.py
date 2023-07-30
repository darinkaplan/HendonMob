import requests
import bs4
from datetime import datetime
import urllib.parse as parse
from urlextract import URLExtract

def convert_to_float(input_string):
    # Remove any non-numeric characters except for the dot (.)
    cleaned_string = ''.join(filter(lambda x: x.isdigit() or x == '.', input_string))
    # Convert the cleaned string to a float
    try:
        result = float(cleaned_string)
    except ValueError:
        result = None
    return result

def tournament_results(hendon_mob_id):
    # URL is the page on Hendon Mob Database with the player's results, based on their hendon_mob_id
    URL = f"https://pokerdb.thehendonmob.com/player.php?a=r&n={hendon_mob_id}"
    page = requests.get(URL)

    soup = bs4.BeautifulSoup(page.content, "html5lib")

    # The tournament result data is in "tr" tags all using class "row0"
    scraped_data = soup.select('tr.row0, tr.row1')

    results = []

    for result in scraped_data:
        tournament_date = result.find("td", class_="date")
        venue_flag = result.find("td", class_="venue_flag")
        event_name = result.find("td", class_="event_name")
        place = result.find("td", class_="place")
        currency = result.find("td", class_="currency")
        points = result.find("td", class_="points")

        if currency is not None:
            tournament_result = {
                'date': datetime.strptime(tournament_date.text.strip(), "%d-%b-%Y"),
                'venue_flag': venue_flag.text.strip(),
                'event_name': event_name.text.strip(),
                'place': place.text.strip(),
                'currency': convert_to_float(currency.text.strip()),
                'points': float(points.text.strip()) if points.text.strip() != '' else 0.0,
            }
            results.append(tournament_result)
    return results

def player_search(search_string):
    extractor = URLExtract()
    final = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    name = parse.quote(search_string, safe=' ')

    url = "https://www.thehendonmob.com/search/?q=" + name
    scraped = requests.get(url, headers=headers)

    hendonmob_search = bs4.BeautifulSoup(scraped.content.decode(), 'lxml')
    players = []
    first_player = hendonmob_search.find('div', attrs={'class': 'db-gallery__item'})
    players.append(first_player)

    i = 0
    while players[i].next_sibling.next_sibling is not None:
        next_player = players[i].next_sibling.next_sibling
        players.append(next_player)
        i += 1

    for player in players:
        player_info = bs4.BeautifulSoup(player.decode(), 'lxml')

        player_name = player_info.find('div', attrs={'class': 'name'}).string

        player_web = player_info.find('a').get('href')
        player_id = parse.parse_qsl(player_web)[1][1]

        player_img = player_info.find('span', attrs={'class': 'db-gallery__thumbnail-image'}).get('style')
        player_img = extractor.find_urls(player_img)[0]

        player_birth = player_info.find('div', attrs={'class': 'db-gallery__item-subtext'}).string

        player_info_dic = {'name': player_name,
                           'id': player_id,
                           'image': player_img,
                           'birthplace': player_birth}
        final.append(player_info_dic)

    return final

#
# x = tournament_results(171541)
# print(x)