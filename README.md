## Super Bees - AI Bee-Soultion 프로젝트

# 1. 프로젝트 개요
 ## 프로젝트 소개
 - 일상과 고민들을 공유하고 솔루션을 얻을 수 있는 웹 서비스 'Beesolution' 개발

## 프로젝트 노션
- [비솔루션 소개 노션](https://www.notion.so/Super-Bees-AI-3-AI-Bee-solution-S-A-14f050d1286243889061802f2e7510d2)

## 기간
 - 2022.12.01 ~ 2022.12.29 (5주)

## 팀명 및 팀원
 * 팀명 : Super Bees (Bees : Back-end engineers)
 * 팀장 : [김병문](https://github.com/kbm1933)
 * 팀원 : [김동익](https://github.com/DongIkkk), [오형석](https://github.com/auberr), [이혜원](https://github.com/wonprogrammer), [최정윤](https://github.com/uniqquej)
 
# 2. 서비스
 ## 서비스 소개 - [www.beesolution.tk](https://beesolution.tk)
- [www.beesolution.tk](https://beesolution.tk)
- 익명의 사용자가 고민을 올리면 꿀벌들이 협동하듯 사용자들이 솔루션을 주고 인공지능 Superbee가 최적의 솔루션을 제시 해주는 웹 서비스
- 최적의 솔루션은 분석을 통해 상황에 맞는 재미있는 짤과 함께 제공됩니다.
- 솔루션을 바탕으로 사용자들과 소통할 수 있는 커뮤니티 서비스가 있습니다.

### - [www.beesolution.tk](https://beesolution.tk)

## 📰페이지 소개
| 회원가입 & 로그인 | 고민 작성 & 솔루션 추천  |
|:----------:|:----------:|
| <img src = "https://user-images.githubusercontent.com/6766202/209770786-d85266ff-be7f-4d33-90fc-4bf11396ffe8.gif" /> <img src = "https://user-images.githubusercontent.com/110454344/209803334-035a0a1b-3984-4e01-90e5-683e3d14c949.png" />  | <img src = "https://user-images.githubusercontent.com/110454344/209767124-8df558d0-ba85-40f1-9993-33be1b535be0.gif" /> <img src = "https://user-images.githubusercontent.com/110454344/209803450-836dc8cd-472e-43c7-a22f-d172062acdb8.png" />  |

| 솔루션 생성 & 평가 & 삭제  | 게시글 디테일 & 수정 & 추천 솔루션 |
|:----------:|:----------:|
| <img src = "https://user-images.githubusercontent.com/110454344/209767453-8730fafc-8f2b-4a22-9d7b-5806ec9bc212.gif" /> <img src = "https://user-images.githubusercontent.com/110454344/209803508-1b944278-225a-4895-83f0-5cd9d95d7017.png" />  | <img src = "https://user-images.githubusercontent.com/6766202/209770864-3a44bab5-22f6-4ce0-9675-7bbb9995a7d1.gif" /> <img src = "https://user-images.githubusercontent.com/110454344/209803562-9b4630dc-fd3c-41ec-ae6c-64e16661c813.png" />  |

| 댓글 작성 & 수정 & 삭제 | 프로필 기능들 |
|:----------:|:----------:|
| <img src = "https://user-images.githubusercontent.com/6766202/209770895-ed3aeb35-7272-4836-a922-97144cab34a4.gif" /> <img src = "https://user-images.githubusercontent.com/110454344/209803604-8e7097ba-6c30-4d11-9566-e6c4705be8c7.png" />  | <img src = "https://user-images.githubusercontent.com/113076205/209771362-f9e3d0d5-a326-41d6-a239-846bccc027ad.gif" /> <img src = "https://user-images.githubusercontent.com/110454344/209803640-85586fbb-ecc9-4363-9951-331b84a6f40b.png" />  |

| 쪽지 기능 | 댓글 알림 기능 |
|:----------:|:----------:|
| <img src = "https://user-images.githubusercontent.com/113076205/209771433-af8c41c2-a7e9-488c-b49d-85655954a263.gif" /> <img src = "https://user-images.githubusercontent.com/110454344/209803695-ad701e55-bf70-4d8f-afb7-23fc98099f98.png" />  | <img src = "https://user-images.githubusercontent.com/110454344/209767461-a6e425f3-c209-4ca1-94bf-8f9c887d1b3a.gif" /> <img src = "https://user-images.githubusercontent.com/110454344/209803702-7c149ba3-1529-4b63-80ca-ba24af20ff51.png" />  |

# 3. 기술

## Structure
<details>
<summary>프로젝트 구성</summary>
<div markdown="1">

<br>

```markup
Backend
├── article
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── pagination.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── viewss.py
├── beesolution
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └──  wsgi.py
├── fonts
│   └── NotoSerifKR-Bold.otf
├── users
│   ├── management
│   │   ├── commands
│   │   │   ├── init.py
│   │   │   └── seed_users.py
│   │   └── init.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── viewss.py
│   load_csv.py
│   ratings.csv
│   solutions.csv
│   makesolution.py
│   manage.py
│   similarity.py
└── requirements.txt

Frontend
├── css
│   ├── alarm.css
│   ├── article_detail.css
│   ├── articles.css
│   ├── create_solution.css
│   ├── index.css
│   ├── kakao.css
│   ├── main.css
│   ├── message.css
│   ├── profile.css
│   ├── profile_detail.css
│   ├── promotion.css
│   ├── signup_userchr.css
│   ├── solution.css
│   ├── solution_collection.css
│   └──  solution_detail.css
├── imgs
│   ├── bee_logo.jpg
│   ├── beealarmoff.png
│   ├── beealarmon.png
│   ├── delete.png
│   └── sadbee.jpg
├── js
│   ├── alarm.js
│   ├── article_detail.js
│   ├── articles.js
│   ├── create_solution.js
│   ├── index.js
│   ├── kakao.js
│   ├── main.js
│   ├── message.js
│   ├── profile.js
│   ├── profile_detail.js
│   ├── promotion.js
│   ├── signup_userchr.js
│   ├── solution.js
│   ├── solution_collection.js
│   └── solution_detail.js
├── alarm.html
├── article_detail.html
├── articles.html
├── create_solution.html
├── index.html
├── kakao.html
├── main.html
├── message.html
├── profile.html
├── profile_detail.html
├── promotion.html
├── signup_userchr.html
├── solution.html
├── solution_collection.html
└── solution_detail.html

```
</div>
</details>

## 사용 기술 
- ### backend
  <img src="https://img.shields.io/badge/python-3.9.10-3776AB?style=for-the-badge&logo=python&logoColor=white"> <img src="https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white">

- ### frontend
  <img src="https://img.shields.io/badge/html5-E34F26?style=for-the-badge&logo=html5&logoColor=white"> <img src="https://img.shields.io/badge/css-1572B6?style=for-the-badge&logo=css3&logoColor=white"> <img src="https://img.shields.io/badge/javascript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black">

- ### deploy
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=Docker&logoColor=white"> <img src="https://img.shields.io/badge/NGINX-009639?style=for-the-badge&logo=NGINX&logoColor=white"> <img src="https://img.shields.io/badge/amazonaws-232F3E?style=for-the-badge&logo=amazonaws&logoColor=white">

## 아키텍쳐
![Architecture](https://user-images.githubusercontent.com/110454344/209760652-a7cb73b2-6c98-44e6-975e-3f69172f0776.png)


 ## ERD
 ![image](https://user-images.githubusercontent.com/109218139/207600367-5ddef6ea-a27c-4dcf-beb7-5ff686d59c97.png)

## API
![api1](https://user-images.githubusercontent.com/110454344/209745638-e2883189-506b-4b88-a727-f89aac9c1856.jpg)
![api2](https://user-images.githubusercontent.com/110454344/209746719-1f939ad7-f55f-4e33-ada9-6ff7448a267c.jpg)
![api3](https://user-images.githubusercontent.com/110454344/209745695-2950ea01-b58c-4884-bdd9-cce100495676.jpg)
![api4](https://user-images.githubusercontent.com/110454344/209745697-ccf4dd3c-1ad4-4bb0-8c39-3f8af1e57025.jpg)
![api5](https://user-images.githubusercontent.com/110454344/209746724-f8745f13-e023-40ed-897e-c214a73eb3db.jpg)

## 트러블슈팅
![트러블_페이지네이션](https://user-images.githubusercontent.com/55372753/207770225-b45f451e-d4e5-4683-9a32-f986f7c37ea5.png)
![트러블_콜드스타트](https://user-images.githubusercontent.com/55372753/207770235-30a4b703-bdc8-40cd-b806-24dd5923a652.png)
![트러블_키에러](https://user-images.githubusercontent.com/55372753/207770247-ac7c1218-1102-403d-81de-91739add5e28.png)
![트러블_인덱스에러_1](https://user-images.githubusercontent.com/55372753/207770259-a0690844-82d1-4ae5-91e5-f7e85ad216e0.png)
![트러블_인덱스에러_2](https://user-images.githubusercontent.com/55372753/207770268-b009f0c5-88b4-44bd-8d25-a3303c24148f.png)
![트러블_소셜로그인](https://user-images.githubusercontent.com/55372753/207770283-5218086c-71c2-47be-8367-045e7dee98d3.png)


# 4. 기타 
 ## Front-end repo
- [깃헙으로 이동](https://github.com/kbm1933/B2_Bee_Solution_Front)

 ## Back-end repo
- [깃헙으로 이동](https://github.com/kbm1933/B2_Bee_Solution_Back)
