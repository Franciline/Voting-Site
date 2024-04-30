# Voting-Site

## Description
A website to simulate an electoral vote. There are seven voting methods implemented:
- plurality
- veto
- borda
- stv (single transferable vote)
- condorcet
- copeland
- simpson

You can elect a single candidate in a normal electoral vote, in a liquid democratie, or elect a committee under global and individual constraints.

## Installation
To clone and run the application, you will need to have pip (package manager for python) and have python (3.10.11 or more).
The languages used are Python, HTML, JS and CSS. The modules used are Flask and SQLite3.

```
# Download Flask
$ pip install Flask

# Download SQLite
$ pip install SQLite

# Clone this repository
$ git clone https://github.com/Franciline/Voting-Site.git

# Go into the repository
$ cd atlas/Site

# Run the app
$ python code_final.py
```

After running the file, you will have to open the local server that will show on your terminal.

## Contributors
This project was made by :
[Franciline](https://github.com/Franciline)
[Maiiana](https://github.com/Maiiana)
[Marlhene](https://github.com/marlhene)

My main role in this project was to link the python functions used to calculate the winner of an election and the WebSite. I used SQLite3 to save on a database the candidates generated, and manipulated it using Flask to send the results to the HTML pages.
