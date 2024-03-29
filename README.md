# social-login-flask-lambda
AWS lambda에 배포된 flask social login 프로젝트

## Table of Contents
- [General Information](#General-Information)
- [Technologies Used](#Technologies-Used)
- [Setup](#Setup)
- [Usage](#Usage)
- [Acknowledgements](#Acknowledgements)

## General Information
- Flask blueprint를 활용하여 기능별(login, logout, main)로 함수분리
- static디렉토리의 올바른 경로지정을 위해서 `static_url_path` param 필수
- Python package는 lambda layer에서 호출
- AWS Lambda로 배포는 Serverless framework사용
- Private subnet내에 위치한 DB를 사용하는 경우, NAT gateway 혹은 NAT instance(ec2)를 반드시 설정
- 프로젝트 배포 이후, callback uri 추가 필요

## Technologies Used
- Python: 3.9
- npm: 8.6.0
- Serverless: 3.12.0
- Serverless-wsgi: 3.0.0

## Setup
- 기본 환경 설정
    ```shell
    $ pipenv shell --python 3.9
    $ python -V
    $ pipenv install
    $ pip install -t vendor -r requirements.txt
    $ npm init
    $ npm install -g npx
    ```
- `config.py.default`
    - config값들 수정 후, config.py로 파일명 수정
- `serverless.yml.default`
    - insert-your-value값들을 사용자의 환경에 맞게 수정한 후, serverless.yml로 파일명 수정

## Usage
- Local Test
    ```shell
    $ npx invoke local -f app
    ```
    - 웹브라우저로 http://localhost:5001/ 접속
- Project Deploy
    ```shell
    $ npx sls deploy
    ```
- Service Check
    - shell에 출력된 api gateway url(AWS api gateway console 에서도 확인가능)을 웹브라우저에 입력하여 서비스에 접속

## Acknowledgements
- https://medium.com/thedevproject/flask-blueprints-complete-tutorial-to-fully-understand-how-to-use-it-767f7433a02e
