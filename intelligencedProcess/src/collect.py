import pandas as pd
import json
# spotify API
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


# API Authentication
with open("apikey.json") as f:
    api = json.load(f)
client_id = api["CLIENT_ID"]
client_secret = api["CLIENT_SECRET"]
client_credentials_manager = \
    spotipy.oauth2.SpotifyClientCredentials(client_id, client_secret)
spotipy.oauth2.SpotifyClientCredentials(client_id, client_secret)
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# ID list for loop searching
id_list = []


def get_artist_info(artist):
    """searches artist and returns its attributes of it as a dict.
    Argument is the name of the artist."""

    search_result = spotify.search(q='artist:' + artist, type='artist')
    # get the first artist comes up in the result
    artist_items = search_result['artists']['items'][0]
    artist_name = artist_items['name']
    artist_id = artist_items['id']
    artist_genres = artist_items['genres']
    artist_popularity = artist_items['popularity']
    artist_relations = spotify.artist_related_artists(artist_id=artist_id)
    return {'name': artist_name, 'id': artist_id, 'genres': artist_genres,
            'popularity': artist_popularity, 'relations': artist_relations}


def append_to_lists(df, artist, threshold):
    """appends artist info to each attribute list.
    Arguments: ([pandas.DataFrame df], [dict artist], threshold)"""

    id_list.append(artist['id'])
    candidates = spotify.artist_related_artists(artist['id'])
    candidates = candidates['artists']
    # remove redundant values from relation and
    # select related artists which exceeds the threshold from relation
    print(len(candidates))
    for i in range(len(candidates)):
        del candidates[i]['images'], candidates[i]['external_urls'], \
            candidates[i]['followers'], candidates[i]['href'], \
            candidates[i]['type'], candidates[i]['uri']

    relation = []
    for i in range(len(candidates)):
        in_id_list = candidates[i]['id'] in id_list
        # if related artist does not succeed the threshold, remove it from it
        if ~in_id_list & candidates[i]['popularity'] >= threshold:
            relation.append(candidates[i])

    data = pd.Series([artist['name'], artist['id'],
                      artist['genres'], artist['popularity'],
                      relation], index=df.columns)
    df = df.append(data, ignore_index=True)
    return df

# -------------------- Data Collection -------------------- #


def collect_data():
    # Pandas dataFrame
    artist_df = pd.DataFrame(columns=['name', 'id', 'genres', 'popularity', 'relations'])

    # initializes of the first artist and appends it to pandas data frame
    # change to input("Set initial artist:") after all checks are done
    init_name = input("Set initial artist:")
    # change to input("Set the popularity threshold. A range from 55 to 63 is recommended:") later
    threshold = input("Set the popularity threshold. A range from 55 to 63 is recommended:")
    threshold = int(threshold)
    init_artist = get_artist_info(init_name)
    artist_df = append_to_lists(artist_df, init_artist, threshold)
    print("Added", init_artist['name'])

    # add related artists and append them to pandas data frame
    relations = spotify.artist_related_artists(init_artist['id'])
    for artist in relations['artists']:
        if artist['popularity'] >= threshold:
            artist_df = append_to_lists(artist_df, artist, threshold)
            print("Added", artist['name'])
    # get related artists of each related artist
    loops = 3
    # the number of each artist's related artists is 20,
    # so that the next loop skips artists already searched
    search_from = 1
    print("--- SEARCHING RELATIONS ---")
    for i in range(loops):
        start = search_from
        end = len(id_list)
        for artist_id in id_list[start:end]:
            spotify_search = spotify.artist_related_artists(artist_id)
            for related_artist in spotify_search['artists']:
                is_in_list = related_artist['id'] in id_list
                if (~is_in_list) & (related_artist['popularity'] >= threshold):
                    print("Added", related_artist['name'])
                    artist_df = append_to_lists(artist_df, related_artist, threshold)
                    continue
        search_from = len(id_list) - i * 20
    print("--- FINISHED SEARCHING ---")
    print(artist_df)
    return artist_df
# -------------------- Data Collection End-------------------- #
