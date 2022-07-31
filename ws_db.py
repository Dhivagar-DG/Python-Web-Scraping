# IMPORT MODULES
from bs4 import BeautifulSoup
import requests
import pandas, sqlite3


try:
    # Response for given URL
    response = requests.get("https://www.imdb.com/chart/top/")
    soup = BeautifulSoup(response.text, "html.parser")
    movies = soup.find('tbody', class_="lister-list").find_all('tr')

    # DATA FRAME
    movies_list = {'rank':[], 'movie_name':[], 'rating':[], 'year':[]}

    for movie in movies:
        rank = movie.find('td', class_="titleColumn").text.split('.')[0].strip() #get_text(strip= True)
        movie_name = movie.find('td', class_="titleColumn").a.text.strip()
        rating = movie.find('td', class_="ratingColumn").strong.text.strip()
        year = movie.find('td', class_="titleColumn").span.text.replace("(","").replace(")","").strip()

        #Append each column values to dataframe
        movies_list['rank'].append(rank)
        movies_list['movie_name'].append(movie_name)
        movies_list['rating'].append(rating)
        movies_list['year'].append(year)
except Exception as e:
    print(e)

con = sqlite3.connect("web_scraping.db")
cursor = con.cursor()
TBL_QRY = 'CREATE TABLE IF NOT EXISTS tbl_imdb_top_250_movies(movie_rank, movie_name, movie_rating, year)'
cursor.execute(TBL_QRY)

df = pandas.DataFrame(data= movies_list)

for i in range(len(df)):
    cursor.execute("insert into tbl_imdb_top_250_movies values (?, ?, ?, ?)", df.iloc[i])
else:
    con.commit()
    con.close()
print(df.head())
