# Related-Genre Artist Recommendation Program
# This program suggests artists from your preference and
# recommends others you will probably never know.
# This program requires the following external libraries to run:
# pandas, spotipy(official Spotify API for Python), matplotlib, networkx
#
# This module collects and provides data frame for the main module(main.py)
# This requires standard input to set the initial artist and
# the threshold of popularity.
#
# @Author Daiyu Horii <daiyuhorii@gmail.com>
from src import visualize as vl


def main():
    vl.visualize()


if __name__ == '__main__':
    main()