import pandas as pd
import numpy as np

#추천시스템 class

from sklearn.metrics.pairwise import cosine_similarity
import random
from sklearn.feature_extraction.text import CountVectorizer , TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

movies_df = pd.read_csv('./datasets/movies_small.csv')
ratings_df = pd.read_csv('./datasets/ratings_small.csv')

import random
average_series = ratings_df.groupby('movieId')['rating'].mean()
count_series = ratings_df.groupby('movieId')['rating'].count()


df_1 = average_series.reset_index()
df_2 = count_series.reset_index()
df_3 = df_1.rename(columns={'rating':'average_rating'})
df_4 = df_2.rename(columns={'rating':'rating_count'})
df = pd.merge(df_3, df_4 , on='movieId')
merge_df = pd.merge(movies_df, df , on='movieId')

# 가중평점 계산해서 weighted_rating 컬럼 추가
C = merge_df['average_rating'].mean()
# 투표횟수 중 60%이상의 횟수에 달하는 숫자
# 예를들어 총 투표횟수가 100과 1일때 m값은 매우 달라진다.
m = merge_df['rating_count'].quantile(0.6)

def weighted_vote_average(record):
    v = record['rating_count']
    R = record['average_rating']
    
    return ( (v/(v+m)) * R) + ( (m/(m+v)) * C)

merge_df['weighted_rating'] = merge_df.apply(weighted_vote_average, axis=1)


# timestamp 제거
ratings_df.drop('timestamp' ,axis=1, inplace=True)


class GET_REMMAND:
    def __init__(self , userId): #로그인한 유저 아이디
        self.userId = userId
        # timestamp 제거
        self.movie_ratings_df = pd.merge(movies_df, ratings_df, on="movieId")
        self.user_movie_rating_df = pd.pivot_table(self.movie_ratings_df, values='rating', index=['userId'],
                       columns=['title'])
        # null을 0을 처리
        self.user_movie_rating_df = self.user_movie_rating_df.fillna(0)
        target_user_rating_list = list(self.user_movie_rating_df.iloc[userId , : ])
        target_user_movie_idx_list = [x[0] for x in enumerate(target_user_rating_list) if x[1] !=0]
        movies_series = pd.Series(movies_df['title'] , index=movies_df.index)
        mymovie_series = movies_series[target_user_movie_idx_list]
        self.mymovie_series = mymovie_series
        
    def join_words(self , x):
        return (' ').join(x)
    
    def my_movies(self):
        # 타겟유저가 본영화(평점이 0이 아닌) 
        # target_user_rating_list = list(self.user_movie_rating_df.iloc[self.userId , : ])
        # my_movies_list = [x[0] for x in enumerate(target_user_rating_list) if x[1] !=0 ]
        return self.mymovie_series
        
    def cosine_similarity(self , based="user_based" , target_movie=None , user_n=5):
        cosine_sim = cosine_similarity(self.user_movie_rating_df , self.user_movie_rating_df)
        if based == "user_based":
            #user 코사인 유사도 
            return cosine_sim
        elif based == "content_based":
            user_sim_sorted_ind = cosine_sim.argsort()[: , ::-1]
            user_sim_idx = user_sim_sorted_ind[self.userId][1:6]
            # 유사 유저가 본영화
            other_user_movie_list = []
            taget_user = 1
            for i in user_sim_idx:
                # print(i)
                result = [x[0] for x in enumerate(list(self.user_movie_rating_df.iloc[i , :])) if x[1] !=0 ]
                other_user_movie_list += result
                
            # 타겟유저가 본영화
            target_user_rating_list = list(self.user_movie_rating_df.iloc[self.userId , : ])
            my_movies_list = [x[0] for x in enumerate(target_user_rating_list) if x[1] !=0 ]
            
            # 유사유저가 본영화중에 타겟유저가 안본영화 데이터프레임
            other_movie_index_list = list(set(other_user_movie_list) - set(my_movies_list))
            other_movie_df = merge_df.iloc[other_movie_index_list , :]

            # other_movie_df에 target_movie 의 정보를 추가한 데이티 프레임
            target_movie_df = merge_df[merge_df['title'] == target_movie]
            movie_df = pd.concat([other_movie_df, target_movie_df], ignore_index = True)
            movie_df = movie_df.reset_index(drop=True)
            target_movie_idx = movie_df[movie_df['title'] ==target_movie ].index[0]
            movie_df['genres'] = movie_df['genres'].str.split('|')
            movie_df['genres'] = movie_df['genres'].apply(self.join_words)

            # genres 콘텐츠 기반 cosine similarity 값구하기
            count_vector = CountVectorizer()
            genres_mat = count_vector.fit_transform(movie_df['genres'])
            cosine_sim = cosine_similarity(genres_mat , genres_mat)

            # return movie_df
            return {"movieId" : target_movie_idx , "content_similarity" :cosine_sim , 'df':merge_df}
    
    
    def target_user_movie_recommand(self , movieId , content_sim_dict , df , n=10):
        target_movie_sim = content_sim_dict[movieId]
        # 유사도가 큰것부터 영화ID를 내림차순 정리
        target_sim_idx = np.argsort(target_movie_sim)[::-1][1:n+1]
        recomman_df = df.iloc[target_sim_idx,:]

        return recomman_df['title']
    def weighted_vote_average(self, record):
        v = record['rating_count']
        R = record['average_rating']
        
        return ( (v/(v+m)) * R) + ( (m/(m+v)) * C)
    def target_weighted_ranking_recommand(self , movieId , content_sim_dict , df , n=10):
        target_movie_sim = content_sim_dict[movieId]
        # 유사도가 큰것부터 영화ID를 내림차순 정리
        target_sim_idx = np.argsort(target_movie_sim)
        recomman_df = df.iloc[target_sim_idx,:]
        #가중평점 컬럼 추가
        recomman_df['weighted_rating'] = recomman_df.apply(weighted_vote_average, axis=1)

        #가중평점 높은 순으로 영화 10개추출
        top10_movies = recomman_df.sort_values(by=['weighted_rating'] ,ascending=False)[:n]['title']
        # top10_movies

        return top10_movies