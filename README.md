# FastAPI를 사용한 간단한 게시판 프로젝 ![python Badge](https://img.shields.io/github/pipenv/locked/python-version/seoyun75/post-fastapi)


FastAPI와 SqlModel을 사용하여 만든 게시판API입니다.

## 기능
    1. 게시글
       1. 게시글 생성
       2. 게시글 조회
       3. 게시글 목록 조회
       4. 게시글 수정
       5. 게시글 삭제
    2. 유저
       1. 회원가입
       2. 로그인
       3. 유저 정보 수정
       4. 유저 삭제
       5.  유저 작성 게시글 조회
       6.  유저 작성 댓글 조회
    3. 댓글
       1. 댓글 작성
       2. 댓글 수정
       3. 특정게시글의 댓글 조회
       4. 댓글 수정
       5. 댓글 삭제

## 다운로드
---

*아래의 내용은 window 사용자를 위한 가이드입니다.*

 0. [poetry](https://python-poetry.org/docs/#installation) 와 [pyenv](https://github.com/pyenv-win/pyenv-win)를 사용하여 구성한 프로젝트입니다. install 후 가이드에 따라주세요
    ```
    <!-- Powershell -->

    <!-- poetry -->
    (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -

    <!-- pyenv -->
    Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"
    ```

 1. git clone
    ```git clone https://github.com/seoyun75/post-fastapi.git ```
 2. post-fastapi 디렉토리로 이동
    ``` cd .\post-fastapi ```
 3. 설치된 Potry를 사용해 Install 하기
    ``` poetry install```
 4. 디렉토리의 post_fastapi로 이동
    ```cd .\post_fastapi```
 5. 실행
    ```poetry run uvicorn main:app```


## API Diagram
---
![캡처](/diagram.png)
<!-- <img src="/uploads/1848994ad25765da30fa8ef3684c67bc/캡처.PNG"  width="700" height="370"> -->
