# The formula for a perfect movie

### Abstract:
‘The Formula for a Perfect Movie’ is a project that aims to uncover the complexity of cinematic success by examining diverse features, including ratings, revenue, genre, inclusivity, and more. Motivated by the nuanced nature of film achievement, we introduce a new Movie Score metric that considers ratings and revenue, providing a robust measure of a movie's success. By validating our findings on a dataset of unseen movies and comparing them with a neural network model, we aim to offer valuable insights into the secrets of successful filmmaking. By considering diverse and valuable data sources, this project seeks to explore the value that can be extracted thanks to Data Science. 

In our data story, we guide our readers through the investigative processes that were utilized on our journey to detect the key influencers of good movies. As we unravel the insights embedded in the data, we hope that the reader will be encouraged towards introspection, thinking about what they believe makes a successful movie.

# Research questions

In this project, we aim to tackle the following research questions:

* How can we define the success of a movie?
* Can we consider ratings and movie revenue to determine a success metric? Is there a correlation between ratings and
  movie revenue?
* Have movies become better over time?
* Which features influence the success of a movie?
    * Considering: movie duration, language, geographical location of the setting, budget, genre, ethnic inclusivity,
      fame of actors, fame of directors, movie plot sentiment analysis, and movie sequels.

# Proposed additional datasets:

To answer our research questions, we will be using additional datasets:

* To study the effects of inclusivity on a movie’s success, we needed actors' information so we scraped
  the [Wikidata](https://query.wikidata.org/sparql)
  website. The dataset generated includes information about the actors’ ethnicity.
* Movie ratings are an important part of our project, yet we have no information about it in the given datasets.
  Therefore, a bot that looks for each movie on [IMDb](https://www.imdb.com) and extracts relevant information (e.g.
  ratings, number of ratings,
  revenue in the United States and Canada, global revenue, and revenue on the week of release) was used:
* To adjust box-office revenue for inflation, we fetched data from the [“US Department of Labor Bureau
  Statistic”](https://www.usinflationcalculator.com/inflation/consumer-price-index-and-annual-percent-changes-from-1913-to-2008/).
* To know which movies were sequels, we used a [dataset with movie-series](https://data.world/priyankad0993/sequels).

# Work Organization

In order to realize this project, we collectively augmented and preprocessed the data. Then, when we noticed that there
was little correlation between movie ratings and revenue, we established a movie success score that considered both.
After that, each team member took a specialized aspect and examined if and how it shapes a film’s success or failure in
terms of the defined score. Aymeric delved into temporal factors and population dynamics, understanding their
correlation with financial success and viewer opinions. Yara studied genre analysis, as well as the effect of sequels.
Eric explored inclusivity. Anthony analyzed features like duration and language, while Anton focused on the influence of
actors’ fame. Finally, we brought our insights together and started building the recipe for a good movie. 


# Methods

To find the recipe for a good movie, we follow this methodology:

1) Data augmentation and processing

   One can’t start working with data before cleaning it and preparing it, which is why we carry the following steps:

   *  Find datasets (e.g. Kaggle, scraping IMDB and Wikidata) containing additional data we need for our project and
   don’t have yet (e.g. movie ratings, inclusivity in movies, inflation, …).
   *  Fill NaN values for inclusivity with data from more datasets (found online from scraping).
   *  In the movies datasets, remove the movies without revenue and ratings data.
   *  Adjust box office revenue to inflation to have comparable values.
   *  In the actors datasets, remove lasting NaN values for inclusivity data.
   *  Preprocess the data: convert data in each column into a more convenient format.
   *  Analyze data balance and decide what to do if imbalanced, depending on the feature being analyzed.

3) Analysis of the correlation between movie revenue and rating
   Film directors define a good or bad movie according to its ratings and the revenue it generates. But are these two
   elements correlated? To answer this question, we conduct a Pearson correlation test and visualize the two distributions

4) Definition of a success score metric that considers both rating and revenue
   Since movie ratings and revenue are not significantly correlated, we define a movie success score metric (Movie
   Score), that considers them both:

   The rating component (RC) is defined as the min-max normalization of the ratings.

   $$RC = \frac{Movie Rating - MinMovieRating]}{MaxMovieRating - MinMovieRating}$$

  The Box Office Revenue Component (BORC) is a bit more complex as box office revenue ranges over multiple orders of magnitude and varies greatly over the years. Firstly, to have comparable revenues, we need to adjust them for inflation. Secondly, to avoid excessively considering outliers, we decide to take the log of these values. As such, we perform the min-max normalization of the log of adjusted revenues. 

   $$BORC = \frac{log(Adjusted Movie Revenue) - log(MinAdjustedMovieRevenue)}{log(MaxAdjustedMovieRevenue) - log(
   MinAdjustedMovieRevenue)}$$

   Finally, we want our score to be defined as a score over 100 so we perform adequate operations.
   Here is the final formula:

   $$Movie Score = (BORC + RC) * 50$$

   Only then can we define two classes of good and bad movies by defining a percentage threshold on movie scores.


4) Find the effect of each feature on the movie’s success score.

   | Feature                             | Description                                                                                                                                                                                                         |
      |:------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
   | Movie budget                        | Wonder if higher budgets are a gage of qualitative movies.                                                                                                                                                                                                             |
   | Genres                              | Analyze the most successful genres.                                                                                                                                                                                                               |
   | Ethnic diversity of the cast        | Get insight into the appeal of movies with a diverse cast.                                                                                                                                                                                                               |
   | Sequels                             | Analyze the popularity of sequels as opposed to prequels.                                                                                                                                                                                                                |
   | Actors' popularity                  | Define an actor's popularity as the sum of movie scores of the previous movies he acted in. Look at the correlation between the popularity of the cast and the movie score. |
   | Movie directors' popularity         | Define the director's popularity as the sum of movie scores of the previous movies he directed and study its correlation with the movie score.                                                                                                                                                                                                               |
   | Sentiment analysis of movie endings | Get insight into the interest in movies with happy endings (and other types of endings).                                                                                                                                                                                                             |
   | Duration                            | Analyze the correlation between movie metadata and its success.                                                                                                                                                                                                               |
   | Language                            | Look into the most successful movie languages.                                                                                                                                                                                                             |
   | Country                             | Analyze whether certain movie settings are more appealing than others.                                                                                                                                                                                                               |


6) Finally, a recipe for good movies …

From the above tests, we identify the features that affect the movie’s success the most thus defining a “recipe for good
movies”. To validate our results, it would be interesting to first apply our model to a test set (movies published since
2012 that are not featured in the dataset), then compare the recipe-generated score prediction for each movie with their
ground-truth success score. We can also train a Neural Network and compare it with our recipe, to assess unseen
dependencies. 
