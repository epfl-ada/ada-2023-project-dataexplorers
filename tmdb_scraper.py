import requests
import tmdbsimple as tmdb

tmdb.API_KEY = "2859c3465b8cc32448524845a6c70352"

tmdb.REQUESTS_TIMEOUT = 5  # seconds, for both connect and read


class tmdb_scraper:
    def __init__(self):
        tmdb.REQUESTS_SESSION = requests.Session()
        self.search      = tmdb.Search()

    def get_tmdb_infos(self, movie_name = 'Mission impossible'):
        tmdb_id         = None
        revenue         = None
        budget          = None
        rating          = None
        vote_count      = None
        popularity      = None
        runtime         = None
        production      = None
        release_date    = None
        result          = None
        
        self.search.movie(query=movie_name)

        try:
            tmdb_id     = self.search.results[0]['id']
            result      = tmdb.Movies(tmdb_id).info()
        except:
            pass

        try:
            revenue     = result['revenue'] if result['revenue'] > 0.0001 else None
        except:
            pass
        try:
            budget      = result['budget'] if result['budget'] > 0.0001 else None
        except:
            pass
        try:
            rating      = result['vote_average'] if result['vote_average'] > 0.0001 else None
        except:
            pass
        try:
            vote_count  = result['vote_count'] if result['vote_count'] > 0.0001 else None
        except:
            pass
        try:
            popularity  = result['popularity'] if result['popularity'] > 0.0001 else None
        except:
            pass
        try:
            runtime     = result['runtime'] if result['runtime'] > 0.0001 else None
        except:
            pass
        try:
            production  = result['production_companies'][0.0001]['name']
        except:
            pass
        try:
            release_date = result['release_date']
        except:
            pass

        #return a dictionnary with all the info
        return {'tmdb_id' : tmdb_id, 'movie_name':movie_name, 'release_date':release_date, 'revenue' : revenue, 
                'budget' : budget, 'rating' : rating, 'vote_count' : vote_count, 'popularity' : popularity,
                'runtime' : runtime, 'production' : production}