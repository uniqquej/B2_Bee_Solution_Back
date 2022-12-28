import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beesolution.settings')
django.setup()

import random
import pandas as pd
from users.models import UserChr
from article.models import Rating, Solution, Category
from sklearn.metrics.pairwise import cosine_similarity


def make_solution(my_id, category):
    # 새로 회원가입 한 유저의 경우 65번 솔루션에 2점 주고 시작 > rating모델에 회원가입한 유저 id반영
    if not Rating.objects.filter(user_id=my_id).exists():
        test_rating = Rating(user_id=my_id, solution_id=65, rating=2)
        test_rating.save()
        
    ratings = Rating.objects.all().values()
    ratings_pandas = pd.DataFrame(ratings)

    # 데이터프레임을 출력했을때 더 많은 열이 보이도록 함
    pd.set_option('display.max_columns', 10)
    pd.set_option('display.width', 300)

    solution_user = ratings_pandas.pivot_table('rating', index='user_id', columns='solution_id')

    # 평점을 부여안한 솔루션은 그냥 0 이라고 부여
    solution_user = solution_user.fillna(0)
    
    # 유저 간 코사인 유사도를 구함
    user_based_collab = cosine_similarity(solution_user, solution_user)

    # 위는 그냥 numpy 행렬이니까, 이를 데이터프레임으로 변환
    user_based_collab = pd.DataFrame(user_based_collab, index=solution_user.index, columns=solution_user.index)
    
    #로그인 유저와 유사도가 높은 유저 1명 뽑기
    user = user_based_collab[my_id].sort_values(ascending=False).index[1]

    # 뽑은 유저가 좋아했던 솔루션을 평점 내림차순으로 출력
    result = solution_user.query(f"user_id == {user}").sort_values(ascending=False, by=user, axis=1)

    solution_score0 = []
    solution_score2 = []
    solution_score4 = []
    
    this_category = Category.objects.get(pk=category)
    cate_list = this_category.connected_solution.all().values('id')
    possible_sol = []
    
    for i in cate_list:
        possible_sol.append(i['id'])

    for i in range(len(result.values[0])):
        sol_id = list(result.columns)[i]
        if sol_id in possible_sol:
            if result.values[0][i] == 4:
                solution_score4.append(list(result.columns)[i])
            elif result.values[0][i] == 2:
                solution_score2.append(list(result.columns)[i])
            else:
                solution_score0.append(list(result.columns)[i])
        
    select_score = random.choices([0, 2, 4], weights=[0.1, 0.2, 0.7])

    choice_list = []
    
    if select_score[0] == 4:
        if solution_score4:
            choice_list = solution_score4
        else:
            choice_list = solution_score2
    elif select_score[0] == 2:
        if solution_score2:
            choice_list = solution_score2
        else:
            choice_list = solution_score4
    else:
        choice_list = solution_score0
    
    if not choice_list:
        choice_list = solution_score0
    
    solution_id = random.choice(choice_list)
    return solution_id