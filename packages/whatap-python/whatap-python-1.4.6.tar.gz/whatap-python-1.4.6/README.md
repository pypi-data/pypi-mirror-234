[![WhaTap Logo](https://www.whatap.io/img/common/whatap_logo_re.svg)](https://www.whatap.io/)
# WhaTap for python

Whatap allows for application performance monitoring.


# 개발 환경 : python 3.3.0 / go 1.8.3 (osX)
# git branch : proto(개발환경) / master(배포)

MacOS 환경에서 Python Agent 개발 환경 구성

Python Agent 샘플 구성 : php-apm + python-apm + python-sample

# 디렉토리 구성

```
python-agent-test
- php-apm # git repository clone
- python-apm # git repository clone
- python-sample # git repository clone
- env # pyen + pyvenv
```

# 개발 환경 구성

## 테스트 디렉토리 생성

```
$ mkdir python-agent-test
```

## git repository clone
WORDING_DIR: python-agent-test

```
$ git clone http://gitlab.whatap.io:8888/whatap-inc/php-apm.git
$ git clone http://gitlab.whatap.io:8888/whatap-inc/python-apm.git
$ git clone http://gitlab.whatap.io:8888/whatap-inc/python-sample.git
```

### git pull 시 에러 해결

Failed with error: RPC failed; curl 18 transfer closed with outstanding read data remaining The remote end hung up unexpectedly The remote end hung up unexpectedly

- git clone depth 옵션 사용
git clone –depth [숫자] [주소] : 프로젝트가 많은 커밋들을 가지고 있을 경우 내려받는데 오래 걸리므로 depth 옵션을 사용하면 해당 숫자만큼의 최신 커밋들만 가지고 프로젝트를 내려받는다.

```
$ git clone http://gitlab.whatap.io:8888/whatap-inc/python-apm.git  --depth 1
```

- git Http postBuffer size 변경
Http postBuffer size를 늘려준다.

```
$ git config --global http.postBuffer 524288000
```

## brew를 통해 의존성 패키지 설치

### brew(mac용 패키지 관리자) 설치

```
$ ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

### brew 업데이트

```
$  brew update
```


### brew를 통해 의존성 패키지 설치

```
$ brew install readline xz mysql-client postgresql
$ echo 'export PATH="/usr/local/opt/mysql-client/bin:$PATH"' >> ~/.bash_profile
$ source ~/.bash_profile
```

설치가 되지 않으면 다음으로 재시도

```
$ brew reinstall readline xz mysql-client postgresql
$ sudo installer -pkg /Library/Developer/CommandLineTools/Packages/macOS_SDK_headers_for_macOS_10.14.pkg -target /
```


## go 설치
```
$ brew search go # go 설치 가능한 목록 확인
$ brew install go@1.8 # go 설치
$ go env # go 설치 환경 확인
```

### go 버전이 맞지 않는 경우

```
$ echo 'export PATH="/usr/local/opt/go@1.8/bin:$PATH"' >> ~/.bash_profile
$ source ~/.bash_profile
$ go env
```

### go path 설정 및 의존성 패키지 설치
WORDING_DIR: php-apm/php.agent.go

```
$ echo 'export GOPATH='$(pwd) >> ~/.bash_profile
$ source ~/.bash_profile
$ cd src/whatap
$ go get #의존성 패키지 설치
```

### go compile 테스트
WORDING_DIR: python-apm

컴파일 후 agent디렉토리에 생성되는 내용을 확인한다.
디렉토리가 비어있는 경우는 컴파일이 제대로 되지 않았음을 의미한다.

```
$ ./compile_goagent.sh $GOPATH
---------------------------------------------------------------
[RESULT]
---------------------------------------------------------------
~/python-sample/whatap/agent/darwin:
total 0
drwxr-xr-x  4 kimjihye  staff  136 Dec 14 17:42 .
drwxr-xr-x  4 kimjihye  staff  136 Dec 14 17:42 ..
drwxr-xr-x  3 kimjihye  staff  102 Dec 14 17:42 amd64
drwxr-xr-x  3 kimjihye  staff  102 Dec 14 17:42 arm64

~/python-sample/whatap/agent/linux:
total 0
drwxr-xr-x  4 kimjihye  staff  136 Dec 14 17:42 .
drwxr-xr-x  4 kimjihye  staff  136 Dec 14 17:42 ..
drwxr-xr-x  3 kimjihye  staff  102 Dec 14 17:42 amd64
drwxr-xr-x  3 kimjihye  staff  102 Dec 14 17:42 arm64

```

## pyenv 설치 및 파이썬 버전 설치
파이썬 버전을 관리하는 툴.
하나의 컴퓨터에 다양한 파이썬 버전을 설치하고 관리.
```
$ brew install pyenv

$ pyenv —version # 버전 확인

$ pyenv install -list # 설치 가능한 파이썬 목록 확인.x
$ pyenv install 3.3.0 # 개발 환경에 필요한 파이썬 버전을 설치
$ pyenv versions # 설치되어 있는 파이썬 버전들 확인
$ pyenv version # 현재 설정되어 있는 파이썬 버전
$ pyenv global 3.3.0 # 설치되어 있는 파이썬 버전을 현재 사용할 파이썬 버전으로 설정
$ python -V # 파이썬 버전 확인
```

## 특정 버전의 python으로 alias설정
WORDING_DIR: HOME (cd)

파이선 버전이 변경되지 않는 경우 수동으로 alias 를 등록해준다.

```
$ .pyenv/shims/python -V #pyenv의 파이썬 버전 확인

$ echo 'export PATH="[ABSOLUTE_PATH]/.pyenv/shims/python"' >> ~/.bash_profile

$ source ~/.bash_profile

$ python -V
Python 3.3.0
```

## 가상 환경 생성 (python3에 내장되어 있는 pyvenv 를 이용)
WORDING_DIR: python-agent-test

```
$ python -m venv env # 가상 환경 디렉토리 만들기
$ . env/bin/activate # 가상 환경 사용
(env) $ python -V # 가상환경 파이썬 버전 확인
$ deactivate # 가상 환경 빠져나오기
```

# pip 설치 및 버전 확인
이때 pip와 연결된 python버전을 꼭 확인한다.

```
$ . env/bin/activate # 가상 환경 사용
(env) $ easy_install pip


(env) $ pip -V
pip 18.1 from /Library/Python/2.7/site-packages/pip-18.1-py2.7.egg/pip (python 2.7)
```

## python 버전이 맞지 않는 경우 다음으로 버전을 확인한다.

```
$ python -V # 먼저 파이썬 버전 확인
(env) $ python -m pip -V # 해당 파이썬 버전에 한한 pip 버전 확인
```

## 필수 패키지 설치
python-apm 과 python-sample 디렉토리에 각각 설치 한다.

```
(env) $ python -m pip install -r requirements.txt
```


# 에이전트와 샘플 애플리케이션 실행

## 에이전트 실행 명령어 제공을 위한 스크립트 생성(create pip script)
WORDING_DIR: python-apm

```shell
(env) $ python setup.py build
(env) $ python setup.py develop
...

whatap-python 0.1.73 is already the active version in easy-install.pth
Installing whatap-stop-agent script to /Users/mk/.pyenv/versions/3.3.0/bin
Installing whatap-setting-config script to /Users/mk/.pyenv/versions/3.3.0/bin
Installing whatap-start-batch-agent script to /Users/mk/.pyenv/versions/3.3.0/bin
Installing whatap-start-agent script to /Users/mk/.pyenv/versions/3.3.0/bin
...

(env) $ whatap-start-agent # pip script 확인
```

## 에이전트 실행 명령어를 찾지 못하는경우
다음 경로를 추가 합니다.

```shell
(env) $ echo 'export PATH="[ABSOLUTE_PATH]/.pyenv/versions/3.3.0/bin:$PATH"' >> ~/.bash_profile

(env) $ source ~/.bash_profile
(env) $ whatap-start-agent # command 확인
```

## 샘플 애플리케이션 시작
WORDING_DIR: python-sample

start.sh 스크립트를 열어 workspace의 경로를 변경해주어야 한다. (dir path: python-agent-test)

```shell
(env) $ ./start.sh
```

## 샘플 애플리케이션 동작 확인
브라우저에서 다음 페이지가 정상적으로 열리는지 확인한다.

```shell
http://127.0.0.1:8000/test
```

## 샘플 애플리케이션에 트랜잭션 발생
curl 명령어를 통해 트랜잭션을 발생 시킬 수 있다.

```shell
curl http://127.0.0.1:8000/test
```

shell script를 실행하여 트랜잭션을 발생시킬 수 있다.
단, 테스트 url이 localhost.whatap.io로 지정되어 있기 때문에
다음 처럼 hosts 파일에 localhost.whatap.io가 등록되어 있어야 한다.

```shell
$ sudo vi /etc/hosts # hosts 에 등록
127.0.0.1       localhost.whatap.io

$ sh test-shellscript/ab-test.sh
```

## log 확인
로그 파일 종류: whatap-hook.log(데이터 추적-hooing) & whatap-boot-[DATE].log(데이터 전송)

```shell
$ ls local_test/logs
```


# Deploy

## 버전 정책
실제 배포 되는 버전 정책은 Test Pypi(dev환경)과 Pypi(production환경)을 분리하여 다음 파일로 관리한다.
파일명: ~/python-apm/whatap/build.py

### Test Pypi(dev환경)

* https://testpypi.python.org/pypi
* 접속정보는 위키 및 .pypirc 파일 참고
* 배포 전 whatap/build.py 버전을 올려야 합니다.
```shell
version = '0.1.dev[xxx]'
```

### Pypi(production환경
* https://pypi.python.org/pypi
* 접속정보는 위키 및 .pypirc 파일 참고
* 배포 전 whatap/build.py 버전을 올려야 합니다.

```shell
version = '0.1.[xxx]'
```


### 최초 등록

```shell
$ python setup.py register -r pypi 혹은 testpypi # 최초 패키지 등록. 필요에 따라 testpypi 등록
```

## python 명령어 사용

#### 빌드

```shell
$ python setup.py build
```

## update go agent
* 스크립트 실행 위치는 python-apm/이어야 합니다.
* 최신으로 컴파일을 원하는 경우 php-apm(branch: master) 코드를 최신으로 유지하여야 합니다.
* go_path는 php.agent.go 경로를 지정한다.

```shell
$ ./compile_goagent.sh [go_path]

ex) ./compile_goagent.sh $GOPATH
```


## packaging & distribution
* 스크립트 실행 위치는 python-apm/이어야 합니다.

```shell
$ ./deploy_pypi.sh [target version is_compile_goagent is_upload]

ex) ./deploy_pypi.sh testpypi `date +%s` true true
ex) ./deploy_pypi.sh pypi `date +%s`  true true
```
### 사용 예
ex)

```shell
./compile_goagent.sh $GOPATH
./deploy_pypi.sh testpypi 0.0.1dev231 true
```

# Dir Structure

## TOP Dir Structure

- whatap	# 에이전트 디렉토리 (only Hooking + UDP)
- whatap_dev	# 에이전트 디렉토리 (Hooking + TCP 수집서버로 전송) => 이전 버전으로 현재 사용 안됨. 
- README.md	# 개발 환경에 대한 설명
- compile_goagent.sh	# Go Agent 크로스 컴파일 쉘 스크립트
- deploy_pypi.sh # pypi 서버 배포 쉘 스크립트
- requirements.txt	# 파이썬 의존성 패키지 설치 목록
- setup.cfg	# 설정 값 관리
- setup.py	# whatap dir 패키징을 위한 정의
- setup_dev.py	# whatap_dev dir 패키징을 위한 정의


## whatap Dir Structure

- agent	 # 크로스 컴파일된 GO Agent
- bootstrap # Python Agent start point (Hook)
- conf # Python Agent 설정
- control # Python Agent 제어
- io # byte 변환
- net # UDP 통신 (packet 전송)
- pack # UDP 통신에 전송되는 Pack byte 변환 & type
- scripts # Python console scripts start point (setup.py 파일 참고)
- trace # 트랜잭션 추적
- util # 유틸리티
- value # 데이터 타입
- LICENSE
- README.rst
- __init__.py
- __main__.py
- build.py # 빌드 버전
- whatap.conf # 기본 설정 파일