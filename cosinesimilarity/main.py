
import pandas as pd
from scipy import sparse
from sklearn.metrics.pairwise import cosine_similarity


ratings = pd.read_csv('ratings.csv')  # set first column as index
movies = pd.read_csv('movies.csv')
ratings = pd.merge(movies, ratings)
print(type(ratings))

user_ratings = ratings.pivot_table(index=['userId'], columns=['title'], values='rating')
user_ratings.head()

# drop movies that have less than 100 users rating it
user_ratings = user_ratings.dropna(thresh=100, axis=1).fillna(0)  # fill NaN with 0
user_ratings.head()


# build the similarity matrix

def standardize(row):
    new_row = (row - row.mean()) / (row.max() - row.min())
    return new_row


ratings_std = user_ratings.apply(standardize)

# the calculation of similarity is between rows
item_similarity = cosine_similarity(ratings_std.T)  # transpose matrix so that it's item2item filtering
# print(item_similarity)

#得到相似度矩阵模型
item_similarity_df = pd.DataFrame(item_similarity, index=user_ratings.columns, columns=user_ratings.columns)

# make the recommendations
def get_similar_movies(movie_name, user_rating):
    similar_score = item_similarity_df[movie_name] * (user_rating - 2.5)
    similar_score = similar_score.sort_values(ascending=False)  # similarity in descending order
    return similar_score


# print(get_similar_movies('Willy Wonka & the Chocolate Factory (1971)', 5))

#测试推荐结果
test_user = [('Toy Story (1995)', 2), ('Star Trek: Generations (1994)', 5),('Fight Club (1999)', 5)]
similar_movies = []

for movie, rating in test_user:
    similar_movies.extend(get_similar_movies(movie, rating).items())

similar_movies_df = pd.DataFrame(similar_movies, columns=['Movie', 'Similarity Score'])
similar_movies_df = similar_movies_df.groupby('Movie').sum().sort_values('Similarity Score', ascending=False)

print(similar_movies_df)
