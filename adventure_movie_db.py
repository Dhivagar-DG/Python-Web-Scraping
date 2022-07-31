from bs4 import BeautifulSoup
import requests, pandas, sqlite3


adventure_movie_list = {'rank':[], 'movie_name':[], 'year': [], 'genres': [], 'rating': [], 'description': [],
                        'directors': [], 'stars': [], 'gross_amount': []}

try:
    response = requests.get("https://www.imdb.com/search/title/?genres=adventure&sort=user_rating,desc&title_type=feature&num_votes=25000,&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=5aab685f-35eb-40f3-95f7-c53f09d542c3&pf_rd_r=RQ3W5893D0JMVJMKWNBK&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_gnr_2")
    soup = BeautifulSoup(response.text, "html.parser")
    adventureMovies = soup.find('div', class_="lister-list").find_all('div', class_="lister-item")

    for movie in adventureMovies:
        rank = movie.find('h3', class_="lister-item-header").span.text.replace('.','')
        movie_name = movie.find('h3', class_="lister-item-header").a.text
        year = movie.find('span', class_="lister-item-year").text.replace('(','').replace(')','')
        genre = movie.find('span', class_="genre").text.strip()
        rating = movie.find('div', class_="ratings-imdb-rating").strong.text
        description = movie.find('div', class_="ratings-bar").find_next_sibling('p').text
        director_list = movie.find('div', class_="ratings-bar").find_next_sibling('p').find_next_sibling('p').find('span', class_="ghost").find_previous_siblings('a')
        directors = ", ".join([i.text for i in director_list])
        stars_list = movie.find('div', class_="ratings-bar").find_next_sibling('p').find_next_sibling('p').find('span', class_="ghost").find_next_siblings('a')
        stars = ", ".join([i.text for i in stars_list])
        try:
            gross_amount = movie.find('p', class_="sort-num_votes-visible").find('span', class_="ghost").find_next_sibling('span').find_next_sibling('span').text
        except:
            gross_amount = "Not Provided"

        adventure_movie_list['rank'].append(rank)
        adventure_movie_list['movie_name'].append(movie_name)
        adventure_movie_list['year'].append(year)
        adventure_movie_list['genres'].append(genre)
        adventure_movie_list['rating'].append(rating)
        adventure_movie_list['description'].append(description)
        adventure_movie_list['directors'].append(directors)
        adventure_movie_list['stars'].append(stars)
        adventure_movie_list['gross_amount'].append(gross_amount)

except Exception as e:
    print(e)

con = sqlite3.connect('web_scraping.db')
cursor = con.cursor()
tbl_qry = 'CREATE TABLE IF NOT EXISTS tbl_imdb_adventure_movies(rank, movie_name, year, genres, rating, description, directors, stars, gross_amount)'
cursor.execute(tbl_qry)

df = pandas.DataFrame(data=adventure_movie_list)

for i in range(len(df)):
    cursor.execute('insert into tbl_imdb_adventure_movies values(?, ?, ?, ?, ?, ?, ?, ?, ?)', df.iloc[i])
con.commit()
con.close()