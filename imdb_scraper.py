# Imbd website scraping
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re


class ImdbScraper:
    def __init__(self):
        # set up the webdriver
        chrome_options = webdriver.ChromeOptions()
        #chrome_options.add_argument('--headless')
        #chrome_options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=chrome_options)

        # access the webpage
        driver.get("https://www.imdb.com/")
        self.driver = driver

    def get_imdb_infos(self, movie_name = "The Godfather", close_page=False):
        """
        Scrapes the IMBD webpage of a movie to extract useful information

        Inputs:
            movie_name (str) : The name of the movie to search for
            close_page (bool): Whether to close the webpage after scraping or not

        Outputs:
            global_revenue (float)      : The global revenue of the movie
            budget (float)              : The budget of the movie
            gross_domestic (float)      : The gross domestic of the movie
            opening_weekend (float)     : The opening weekend of the movie
            rating_score (float)        : The rating score of the movie
            number_of_ratings (float)   : The number of ratings of the movie
            watched_rank (float)        : The watched rank of the movie
            producer (str)              : The producer of the movie
        """
        try:
            # find the search bar & search button
            search_bar = self.driver.find_element("xpath", '//*[@id="suggestion-search"]')
            search_button = self.driver.find_element("xpath", '//*[@id="suggestion-search-button"]')

            # search for the movie
            search_bar.send_keys(movie_name)
            search_button.click()

            # find the first result
            first_result = self.driver.find_element("xpath", '//*[@id="__next"]/main/div[2]/div[3]/section/div/div[1]/section[2]/div[2]/ul/li[1]')
            first_result.click()

            # parse the resulting webpage
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
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
                number_of_ratings_div   = soup.find('div', {'data-testid' : "hero-rating-bar__aggregate-rating"})
                number_of_ratings_raw   = number_of_ratings_div.find('div', {'class' : "sc-bde20123-3 bjjENQ"}).text
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
                cast_section            = soup.find('section', {"data-testid" : "title-cast"})
                cast_ul                 = cast_section.find('ul', {"class" : "ipc-metadata-list ipc-metadata-list--dividers-all sc-bfec09a1-8 iiDmgX ipc-metadata-list--base"})
                cast_raw                = cast_ul.find('a', {'class' : 'ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link'}).text
                producer                = cast_raw
            except:
                producer                = None

        except:
            global_revenue              = None
            budget                      = None
            gross_domestic              = None
            opening_weekend             = None
            rating_score                = None
            number_of_ratings           = None
            watched_rank                = None
            producer                    = None

        # close the webself.driver
        if (close_page):
            self.driver.close()

        return {"global_revenue":global_revenue, "budget":budget, "gross_domestic":gross_domestic, "opening_weekend":opening_weekend,
                "rating_score":rating_score, "number_of_ratings":number_of_ratings, "watched_rank":watched_rank, "producer":producer}