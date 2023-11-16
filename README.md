# The formula for a perfect movie

‘The formula for a perfect movie’ is a project whose purpose is to discover what makes a movie great. A dataset composed
of data collected for over 80,000 movies will be used in this regard. The dataset contains information about the movies
themselves, as well as the actors performing in them, and it will be completed with data about the movies’ ratings.

The project will articulate around two main axes. The first part will be about noticing that movie ratings don't
necessarily correlate with movie revenue, then determining which features impact the revenue made by a movie, and which
impact its rating. The second step will thus be to combine these two pieces of information into a single metric by
taking a weighted average of the two, as a great movie has both large revenue and high ratings.

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

* To study the effects of inclusivity on a movie’s success, we needed actors' information so we scraped the [Wikidata](https://query.wikidata.org/sparql)
  website. The dataset generated includes information about actors’ ethnicity.
* Movie ratings are an important part of our project, yet we have no information about it in the given datasets.
  Therefore, a bot that looks for each movie on [IMDb](https://www.imdb.com) and extracts relevant information (e.g. ratings, number of ratings,
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
actors’ fame. Finally, and based on our analysis, we were able to determine together the recipe for a good movie.

# Methods

To find the recipe for a good movie, we follow this methodology:

1) Data augmentation and processing
   One can’t start working with data before cleaning it and preparing it, which is why we carry the following steps:
   a) Find datasets (e.g. Kaggle, scraping IMDB and Wikidata) containing additional data we need for our project and
   don’t have yet (e.g. movie ratings, inclusivity in movies, inflation, …).
   b) Fill NaN values for inclusivity with data from more datasets (found online from scraping).
   c) In the movies datasets, remove the movies without revenue and ratings data.
   d) Adjust box office revenue to inflation to have comparable values.
   e) In the actors datasets, remove lasting NaN values for inclusivity data.
   f) Preprocess the data: convert data in each column into a more convenient format.
   g) Analyze data balance and decide what to do if imbalanced, depending on the feature being analyzed.
2) Analysis of the correlation between movie revenue and rating
   Film directors define a good or bad movie according to its ratings and the revenue it generates. But are these two
   elements correlated? In order to answer this question, we conduct the following tests:

    * $\chi^2$ test
    * T-test
    * Pearson correlation test

3) Definition of a success score metric that considers both rating and revenue
   Since movie ratings and revenue are not significantly correlated, we define a movie success score metric (Movie
   Score), that considers them both:

   The rating component (RC) is defined as the min-max normalization of the ratings.

   $$RC = \frac{Movie Rating - MinMovieRating]}{MaxMovieRating - MinMovieRating}$$

   The Box Office Revenue Component (BORC) is a bit more complex as box office revenue ranges over multiple orders of
   magnitude and varies greatly over the years. Firstly, to have comparable revenues, we need to adjust them for
   inflation.
   Secondly, to avoid excessively considering outliers, we decide to take the log of these values. As such, we perform
   the
   min-max normalization of the ratings.

   $$BORC = \frac{log(Adjusted Movie Revenue) - log(MinAdjustedMovieRevenue)}{log(MaxAdjustedMovieRevenue) - log(
   MinAdjustedMovieRevenue)}$$

   Finally, we want our score to be defined as a score over 100 so we perform adequate operations.
   Here is the final formula:

   $$Movie Score = (BORC + RC) * 50$$

   We also define two classes: good and bad movies by defining a percentage threshold on movie scores.

4) Find the effect of each feature on the movie’s success score.

   | Feature                             | Description |
   |:------------------------------------|:------------|
   | Duration                            | TODO        |
   | Language                            | TODO        |
   | Country                             | TODO        |
   | Movie budget                        | TODO        |
   | Genres                              | TODO        |
   | Ethnic diversity of the cast        | TODO        |
   | Sequels                             | TODO        |
   | Actors' popularity                  | TODO        |
   | Movie directors' popularity         | TODO        |
   | Sentiment analysis of movie endings | TODO        |

5) Finally, a recipe for good movies …

From the above tests, we identify the features that affect the movie’s success the most thus defining a “recipe for good
movies”. To validate our results, it would be interesting to first apply our model to a test set (movies published since
2012 that are not featured in the dataset), then compare the recipe-generated score prediction for each movie with their
ground-truth success score. We can also train a Neural Network and compare it with our recipe, to assess unseen
dependencies. 
