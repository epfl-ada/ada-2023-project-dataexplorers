# Imbd website scraping
from bs4 import BeautifulSoup
import re
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class ImdbScraper:
    def __init__(self):
        """
        Initializes the ImdbScraper class
        """
        chrome_options  = webdriver.ChromeOptions()
        chrome_options.add_argument("--lang=fr")
        self.driver     = webdriver.Chrome(options=chrome_options, executable_path='./chromedriver/chromedriver.exe')
    
    def close(self):
        """
        Closes the driver
        """
        self.driver.close()

    def get_imdb_infos(self, movie_id=0):
        """
        Scrapes the IMBD webpage of a movie to extract useful information

        Inputs:
            movie_id (int)              : The movie's wikipedia id

        Outputs:
            global_revenue (float)      : The global revenue of the movie
            budget (float)              : The budget of the movie
            gross_domestic (float)      : The gross domestic of the movie
            opening_weekend (float)     : The opening weekend of the movie
            rating_score (float)        : The rating score of the movie
            number_of_ratings (float)   : The number of ratings of the movie
            watched_rank (float)        : The watched rank of the movie
            producer (str)              : The producer of the movie
            release_year (str)          : The release year of the movie
        """
        try:
            # access wikipedia api to retrieve the link of the page from the wikipedia id
            resp = requests.get(f"http://en.wikipedia.org/w/api.php?action=query&prop=info&pageids={movie_id}&inprop=url&format=json")
            wikipedia_movie_link = resp.json()['query']['pages'][str(movie_id)]['fullurl']
            html = requests.get(wikipedia_movie_link)

            # access the movie's wikipedia page and find the link to its wikidata page
            soup = BeautifulSoup(html.text, 'html.parser')
            tools = soup.find_all('div', {'id': 'vector-page-tools'})
            wikidata_link = tools[0].find('li', {'id':'t-wikibase'}).find('a')['href']
            wikidata_html = requests.get(wikidata_link)

            # parse the wikidata page of the movie to find its imdb id
            new_soup = BeautifulSoup(wikidata_html.text, 'html.parser')
            wiki_imdb = new_soup.find('div', {'id': 'P345'})
            imdb_id = wiki_imdb.find('div', {'class': 'wikibase-snakview-value wikibase-snakview-variation-valuesnak'}).text
            imdb_link = "https://www.imdb.com/title/" + str(imdb_id) + "/"

            # access the imdb page of the movie using selenium to parse it & extract useful information
            self.driver.get(imdb_link)
            imdb_html = self.driver.page_source

            soup = BeautifulSoup(imdb_html, 'html.parser')
            box_office = soup.find('div', {'data-testid': "title-boxoffice-section"})
            
            # get global revenue
            try:
                brut_li                 = box_office.find('li', {'data-testid' : "title-boxoffice-cumulativeworldwidegross"})
                global_revenue_raw      = brut_li.find('span', {'class' : "ipc-metadata-list-item__list-content-item"}).text
                global_revenue          = float(re.findall(r'\d+', global_revenue_raw.replace('\u202f', ''))[0])
            except:
                global_revenue          = None
            
            # get budget
            try:
                budget_li               = box_office.find('li', {'data-testid' : "title-boxoffice-budget"})
                budget_raw              = budget_li.find('span', {'class' : "ipc-metadata-list-item__list-content-item"}).text
                budget                  = float(re.findall(r'\d+', budget_raw.replace('\u202f', ''))[0])
            except:
                budget = None

            # get budget gross revenue in US & Canada
            try:
                gross_domestic_li       = box_office.find('li', {'data-testid' : "title-boxoffice-grossdomestic"})
                gross_domestic_raw      = gross_domestic_li.find('span', {'class' : "ipc-metadata-list-item__list-content-item"}).text
                gross_domestic          = float(re.findall(r'\d+', gross_domestic_raw.replace('\u202f', ''))[0])
            except:
                gross_domestic          = None
            
            # get opening weekend revenue in US & Canada
            try:
                opening_weekend_li      = box_office.find('li', {'data-testid' : "title-boxoffice-openingweekenddomestic"})
                opening_weekend_raw     = opening_weekend_li.find('span', {'class' : "ipc-metadata-list-item__list-content-item"}).text
                opening_weekend         = float(re.findall(r'\d+', opening_weekend_raw.replace('\u202f', ''))[0])
            except:
                opening_weekend         = None
            
            # get rating score
            try:
                rating_score_div        = soup.find('div', {'data-testid' : "hero-rating-bar__aggregate-rating__score"})
                rating_score_raw        = rating_score_div.text
                rating_score            = float(re.findall(r'\d{1}.\d{1}', rating_score_raw.replace(',', '.').replace('\u202f', ''))[0])
            except:
                rating_score            = None

            # get number of ratings
            try:
                #number_of_ratings_div   = soup.find('div', {'data-testid' : "hero-rating-bar__aggregate-rating"})
                #number_of_ratings_raw   = number_of_ratings_div.find('div', {'class' : "sc-bde20123-3 bjjENQ"}).text
                number_of_ratings_raw = soup.find('div', {'class': 'sc-bde20123-3 gPVQxL'}).text
                number_of_ratings       = float(re.findall(r'\d+.?\d?', number_of_ratings_raw.replace(',', '.').replace('\u202f', ''))[0])
                
                rating_unit             = number_of_ratings_raw[-1]
                if (rating_unit=='M'):
                    number_of_ratings   = 1000000*number_of_ratings
                elif (rating_unit=='k'):
                    number_of_ratings   = 1000*number_of_ratings
            except:
                number_of_ratings       = None

            # get watched rank
            try:
                watched_rank_div        = soup.find('div', {'data-testid' : "hero-rating-bar__popularity"})
                watched_rank_raw        = watched_rank_div.find('div', {'data-testid' : "hero-rating-bar__popularity__score"}).text
                watched_rank            = float(re.findall(r'\d+', watched_rank_raw.replace('\u202f', ''))[0])
            except:
                watched_rank            = None

            # get producer
            try:
                producer                = soup.find("a", {"class":"ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link"}).text
            except:
                producer                = None

            # get release year
            try:
                release_year            = soup.find('div', {'class': 'sc-dffc6c81-0 grcyBP'}).find('a', {'class': 'ipc-link ipc-link--baseAlt ipc-link--inherit-color'}).text
                release_year            = int(release_year)
            except:
                release_year            = None
        
        except:
            global_revenue = None
            budget = None
            gross_domestic = None
            opening_weekend = None
            rating_score = None
            number_of_ratings = None
            watched_rank = None
            producer = None
            release_year = None

        return {"global_revenue":global_revenue, "budget":budget, "gross_domestic":gross_domestic, "opening_weekend":opening_weekend,
                "rating_score":rating_score, "number_of_ratings":number_of_ratings, "watched_rank":watched_rank, "producer":producer,
                "release_year":release_year}