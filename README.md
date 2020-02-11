## Treasure Hunt Utilities

This repo just holds the script that traverses the rooms from the treasure hunt api to create the treasure hunt map, and the script used to mine a coin.

- parse.py: contains the traversal script
- mine.py contains the mining script
- output: the old output is the map from the test server, output2 is the map from the production server
- util.py: holds the Queue for the breadth first search
- formatD3: converts the map into a more d3 friendly format

You will need an env file with an api key in order to hit the treasure hunt api
