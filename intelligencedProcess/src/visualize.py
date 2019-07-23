import json
import networkx as nx
from matplotlib import pyplot as plt
from src import collect as clt


def set_data():
    """
    Sets and collect data for dataFrame.
    This requires inputs, and returns the dataFrame.
    """
    dataframe = clt.collect_data()
    return dataframe


def search_top_genre(dict):
    genres = []
    for genre in dict.values():
        for genre_name in genre:
            genres.append(genre_name)

    genre_counter = {}
    genre_set = set(genres)
    # get the most ordinary genre's value: [integer]
    for element in genre_set:
        genre_counter[element] = genres.count(element)
    most_general_genre = sorted(genre_counter.values(), reverse=True)[0]

    # name of genre to remove from artists' genre lists
    del_genre = ""
    for genre, count in genre_counter.items():
        if count == most_general_genre:
            del_genre = genre
    return del_genre


def plot_graph(g, genres):
    # remove the most ambiguous genre name such as "j-pop", or "rock".
    vague_genre = search_top_genre(genres)
    for node, genre in genres.items():
        if vague_genre in genre:
            genres[node].remove(vague_genre)
    # set colors by genres
    groups = []
    for group in genres.values():
        groups.append(group[0])
    print("groups:", groups)

    groupset = list(set(groups))
    print("group set:", len(groupset), groupset)

    color_combinations = {genre: "" for genre in groupset}
    colorlist = ["red", "orange", "yellow", "green", "blue", "purple", "cyan",
                 "magenta", "crimson", "indigo", "aqua", "royalblue"]
    print("color combs: before:", color_combinations)
    for i in range(0, len(groups)):
        color_combinations[groups[i]] = colorlist[i % len(colorlist)]

    print("color combs:", color_combinations)

    colormap = []
    for group in groups:
        if group in color_combinations.keys():
            colormap.append(color_combinations[group])
    print("colormap:", colormap)

    for k, v in color_combinations.items():
        plt.scatter(0, 0, c=v, label=k)
    plt.legend()

    centrality = nx.communicability_betweenness_centrality(g)
    pos = nx.spring_layout(g, iterations=200, k=0.7)
    node_size = [5000 * size for size in centrality.values()]
    nx.draw_networkx_nodes(g, pos=pos, node_size=node_size, alpha=0.5, nodelist=g.nodes,
                           node_color=colormap)
    nx.draw_networkx_labels(g, pos=pos, font_size=10, font_color='black', alpha=0.8)
    nx.draw_networkx_edges(g, pos=pos, alpha=0.5, edge_color="gray")
    return g


def set_dicts(df):
    relation_list = []
    for relation in df['relations']:
        rel_names = []
        for i in range(len(relation)):
            rel_names.append(relation[i]['name'])
            print(rel_names[i])
        relation_list.append(rel_names)
    name_list = df['name'].to_list()
    genres_list = df['genres'].to_list()
    genres_dict = dict(zip(name_list, genres_list))
    return name_list, relation_list, genres_dict


def visualize():
    # vector = {artist1: ["related1", "related2"...], artist2: [...], ...}
    df = set_data()
    names, rels, genres = set_dicts(df=df)
    vector = dict(zip(names, rels))

    with open("relation.json", "wt") as f:
        json.dump(rels, f, indent=4)

    g = nx.Graph(vector)

    del_list = []
    for node in g.nodes:
        if node not in names:
            del_list.append(node)
    g.remove_nodes_from(del_list)
    plot_graph(g, genres)
    plt.show()
