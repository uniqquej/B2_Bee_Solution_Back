import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beesolution.settings')
django.setup()

import random
import pandas as pd
from users.models import UserChr
from article.models import Rating
from sklearn.metrics.pairwise import cosine_similarity


def make_solution(my_id):
    ratings = Rating().objects.all().values()
    ratings_pandas = pd.DataFrame(ratings)
    chars = UserChr.objects.all().values()
    chars_pandas = pd.DataFrame(chars)
    
    solution_rating = pd.merge(ratings_pandas, chars_pandas, on='user_id') #user_id로 병합 

    # 데이터프레임을 출력했을때 더 많은 열이 보이도록 함
    pd.set_option('display.max_columns', 10)
    pd.set_option('display.width', 300)

    solution_user = solution_rating.pivot_table('rating', index='user_id', columns='solution')

    # 평점을 부여안한 솔루션은 그냥 0 이라고 부여
    solution_user = solution_user.fillna(0)
    
    # 유저 간 코사인 유사도를 구함
    user_based_collab = cosine_similarity(solution_user, solution_user)

    # 위는 그냥 numpy 행렬이니까, 이를 데이터프레임으로 변환
    user_based_collab = pd.DataFrame(user_based_collab, index=solution_user.index, columns=solution_user.index)
    print('********데이터프레임***********')
    print(user_based_collab.head)
    #로그인 유저와 유사도가 높은 유저 1명 뽑기
    user = user_based_collab[my_id].sort_values(ascending=False).index[1]

    # 뽑은 유저가 좋아했던 솔루션을 평점 내림차순으로 출력
    result = solution_user.query(f"user_id == {user}").sort_values(ascending=False, by=user, axis=1) #axis=1 : 열방향으로 동작
    
    solution_ids = [] # 평점이 4점인 솔루션 id list
    for i in range(len(result.values[0])):
        if result.values[0][i]==4:
            solution_ids.append(list(result.columns)[i])
    
    solution_id = random.choice(solution_ids) # 랜덤으로 solution_id 반환
    return solution_id
    