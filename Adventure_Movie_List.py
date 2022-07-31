from bs4 import BeautifulSoup
import requests, openpyxl


# CREATE EXCEL FILE FOR LOAD THIS CONTENT
excel = openpyxl.Workbook()
sheet = excel.active
sheet.append(['Adventure Movies List'])
# Append Table Heading
sheet.append(['Rank', 'Movie Name', 'Year', 'Genres', 'Rating', 'Description', 'Directors', 'Stars', 'Gross_Amount'])


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
        # Append Each column values in row wise
        sheet.append([rank, movie_name, year, genre, rating, description, directors, stars, gross_amount])
    else:
        excel.save("Adventure_movie_list.xlsx")
except Exception as e:
    print(e)