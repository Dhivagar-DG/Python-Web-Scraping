# IMPORT MODULES
from bs4 import BeautifulSoup
import requests, openpyxl


# CREATE EXCEL FILE
excel = openpyxl.Workbook()
excel_sheet = excel.active
excel_sheet.append(['Rank', 'Movie Name', 'Rating', 'Year_Of_Release'])


try:
    # Response for given URL
    response = requests.get("https://www.imdb.com/chart/top/")
    soup = BeautifulSoup(response.text, "html.parser")
    movies = soup.find('tbody', class_="lister-list").find_all('tr')
    for movie in movies:
        rank = movie.find('td', class_="titleColumn").text.split('.')[0] #get_text(strip= True)
        movie_name = movie.find('td', class_="titleColumn").a.text
        rating = movie.find('td', class_="ratingColumn").strong.text
        year = movie.find('td', class_="titleColumn").span.text.replace("(","").replace(")","")
        excel_sheet.append([rank, movie_name, rating, year])
    else:
        excel.save("IMDB_Top_250_Movies.xlsx")
except Exception as e:
    print(e)
