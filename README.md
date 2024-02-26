[실행파일 다운로드 - 압축 해제후 바로 사용 가능 (바탕화면에 바로가기 추가, main.exe파일 연결해 사용)](http://naver.me/583f6jlO)


# 🔥프로젝트 요약

**Project name:** 모션트랙킹 마우스 & 음성인식 키보드

**Project goal:** 이 프로젝트의 목표는 사용자의 `편의성`과 `접근성`을 향상시키는 것입니다. 모션과 음성을 활용함으로써 기존의 마우스와 키보드 조작 방식에 비해 더 자연스럽고 효율적인 컴퓨터 조작 경험을 제공하는 것이 목적입니다.

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)![TensorFlow](https://img.shields.io/badge/TensorFlow-%23FF6F00.svg?style=for-the-badge&logo=TensorFlow&logoColor=white)![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white)![Google Assistant](https://img.shields.io/badge/google%20assistant-4285F4?style=for-the-badge&logo=google%20assistant&logoColor=white)![ChatGPT](https://img.shields.io/badge/chatGPT-74aa9c?style=for-the-badge&logo=openai&logoColor=white)![Media Pipe](https://img.shields.io/badge/MediaPipe-0F79AF?style=for-the-badge&logo=scrollreveal&logoColor=white)![PyQT](https://img.shields.io/badge/PyQT-41CD52?style=for-the-badge&logo=Qt&logoColor=white)

## 팀구성

|이름|메인임무|
|---|---|
|김승환|음성처리 Speech to Text 구현|
|김용철|영상처리, 모션 인식을 통한 마우스 제어|
|임선웅|소프트웨어 QC, 현황 관리|

## Objectives:

- **사용자 경험 향상**: 프로젝트의 주요 목표 중 하나는 사용자의 컴퓨터 조작을 보다 자연스럽고 편리하게 만드는 것 입니다. 
- **액세스 가능성 향상**: 음성인식 기술을 통해 장애인이나 신체적 제약이 있는 사용자들도 키보드와 마우스를 사용하지 않고도 컴퓨터를 조작할 수 있는 가능성을 제시합니다. 
- **효율성 향상**:  키보드를 타이핑하는 것보다 음성 명령을 사용하여 빠르고 정확하게 텍스트를 입력할 수 있으며, 마우스를 움직이는 대신 손의 제스처를 사용하여 컴퓨터를 조작할 수 있습니다.
- **기술 혁신**: 이 프로젝트는 새로운 인터페이스 기술을 개발하고 적용함으로써 기존의 키보드와 마우스 조작 방식을 넘어선다는 기술적 도전을 제공합니다.

## Constraints:

- 프로젝트를 완료하는 데 할당된 시간이 제한되어 있습니다. 
- 하드웨어 사양에 따른 구동환경 제어와 최적화 과정에서 높은 난이도가 요구되었습니다.
- 음성처리 네트워크 환경이 필수적으로 구축되어 있어야 합니다.

## Assumptions:

- 음성인식 기술을 사용하는 부분에서 인터넷 속도에 제한을 받는 경우가 있습니다.
- 모션인식 알고리즘 최적화에 따라 performance의 편차가 클 수 있습니다.
- Python을 사용함에 따라 C/C++ 언어의 사용 대비 상대적 딜레이가 발생 할 수 있습니다. 

<br>

# 🛰️프로젝트 범위 및 계획

## In Scope:

- Mediapipe를 통한 모션 마킹 구현
- 모션을 통한 마우스 제어 구현
- 음성 인식을 통한 Speech to text 구현
- 하드웨어 제어 최적화
- 실행파일(.exe) 생성

## Out of Scope:

- 복잡한 모션을 통한 제어 구현
- 라즈베리파이에 구현
- C/C++ 사용해서 구현
- 모바일 카메라를 사용할 수 있게 구현
- 작업 표시줄에 실행 아이콘 생성
- 마우스 클릭 드래그 구현

## Gantt Chart

```mermaid
gantt
    dateFormat  MM-DD-YYYY
    title       모션인식 마우스& 음성인식 키보드 프로젝트 Gantt Chart
	
	section 음성인식 Speech to Text 코드 구현
		자료 조사 및 코드 해석 :2024-02-18, 1d
                코드 작성 및 STT구현 완료  :crit, 2024-02-19, 2d
	
	section 손동작 인식 마우스 제어
		자료조사 및 코드 해석	: 2024-02-20, 1d
		영상에 모션 마킹  :crit, 2024-02-21, 1d
		모션 인식 마우스 이동 및 마우스 좌클릭 코드 작성 : 2024-02-21, 3d
		모션 인식 마우스, 스크롤 업& 다운 코드 작성 : 2024-02-21, 2d
		마우스 우클릭 및 음성인식 트리거 코드 작성  : 2024-02-21, 2d
		손 인식 알고리즘 최적화 : 2024-02-22, 2d

	section 디버깅 및 병합 과정
		모션 인식 카메라와 디스플레이 맵핑 최적화 : crit, 2024-02-22, 2d
		해당 코드 영상처리 코드랑 합치기 :2024-02-23, 2d

	section 실행 파일 제작
		자료조사 및 코드 해석 : 2024-02-23, 1d
		로딩 및 엔딩 페이지 제작 : 2024-02-23, 2d
		실행파일 제작 : crit, 2024-02-23, 3d
		프로세스 점검 : cirt, 2024-02-25, 2d

```

## Kanban

|BACKLOG  |TO-DO    |IN-PROGRESS        |COMPLETED       |
|---------|---------|-------------------|----------------|
|Speech to text 코딩|         |               |`completed`|
|영상 마킹           |        |               |`completed`|
|모션 인식           |        |               |`completed`|
|코드 병합           |        |               |`completed`|
|실행 파일 생성      |        |               |`completed`|

<br>

# 🔍회의록 

### 1차 프로젝트 계획 회의 | 2024-02-20 | 참석자: 김승환, 김용철

| 안건        | 내용                                       | 결정사항                             |
|------------|--------------------------------------------|--------------------------------------|
| 프로젝트 일정 조정 | - 금일 계획 및 일정을 확인하고 이행할 필요가 있음 | - 프로젝트 방향성 고정 |
| 역할 분담   | - 각 팀원들의 역할을 재확인, 임선웅 팀원의 역할에 대한 논의 필요 <br> - 중요한 임무에 대한 책임자를 지정해야 함. | - 음성인식: 김승환 <br> - 영상처리: 김용철  <br> - 미정: 임선웅 |
| 기타 사항   | - 주말 제외 매일 회의가 진행됩니다. <br> - 추가 안건이 있으면 미리 공유해주시기 바랍니다. | - 다음 회의 일정을 확정합니다.    |

### 2차 프로젝트 회의 | 2024-02-21 | 참석자: 김승환, 김용철, 임선웅

| 안건        | 내용                                       | 결정사항                             |
|------------|--------------------------------------------|--------------------------------------|
| 프로젝트 회의 추가 사항 | Assumptions, In out scope 사항 추가 | |
| 역할 분담 | 임선웅 팀원의 역할 지정 | 소프트웨어 QC, 현황 관리|
| 코드 분석 | 음성처리, 영상처리에 대한 코드 설명 | 팀원들에게 코드에 대한 내용 교육|

### 3차 프로젝트 회의 | 2024-02-22 | 참석자: 김승환, 김용철, 임선웅

| 안건        | 내용                                       | 결정사항                             |
|------------|--------------------------------------------|--------------------------------------|
| 프로젝트 회의 추가 사항 | Out scope 사항 추가  | 작업 표시줄에 실행 아이콘 생성 |
| 향후 목표 제시 | 날짜별 진행 목표에 대한 논의 | 금요일 - 최종적 코딩 완료 <br> 토요일, 일요일 - 진행 상황 검토 <br> 월요일, 화요일 - 최적화, Document 정리 |
| 최종 목표 제시 | 최종적인 목표에 대한 논의 | 프로세스를 백그라운드로 실행 구현 |
| 개선 사항 | 진행 현황 중 개선 사항 논의 | 스크린 화면 프레임, 정확도, 민감도 향상 |

### 4차 프로젝트 회의 | 2024-02-22 | 참석자: 김승환, 김용철, 임선웅

| 안건        | 내용                                       | 결정사항                             |
|------------|--------------------------------------------|--------------------------------------|
| 개선 방안 | 동작인식 오류에 대한 방안 제시 | 다양한 시뮬레이션을 통해 방안 모색 |
| 프로세스 계획 | 로딩창, UI, 아이콘 이미지에 대한 논의 | 적합한 디자인 색출 |
| 프로세스 시연 | 음성인식, 모션인식, 실행파일 코드 병합 | 1차 프로세스 시연 |

### 5차 프로젝트 회의 | 2024-02-26 | 참석자: 김승환, 김용철, 임선웅

| 안건        | 내용                                       | 결정사항                             |
|------------|--------------------------------------------|--------------------------------------|
| 기술 요약 페이지 추가 내용 검토 |  |  |
| 최종 시연영상 제작 시나리오 회의 |  |  |

### 마지막 프로젝트 회의 | 2024-02-27 | 참석자: 김승환, 김용철, 임선웅

| 안건        | 내용                                       | 결정사항                             |
|------------|--------------------------------------------|--------------------------------------|
| 시연 |  |  |

<br>

# 💡프로젝트 일지



|날짜|이름|프로젝트 활동 사항|
|---|---|---|
|2024-02-20|김승환|- 깃허브 README 레이아웃 작성 <br> - 음성인식 코드 완료|
|2024-02-21|김승환|- 모션 인식 마우스, 스크롤 업& 다운 코드 작성 드래프트 완료  <br> - 실행파일 생성에 관한 프로그램 구동 방식 결정|
|2024-02-21|임선웅|- badge 생성 <br> - 제약, 추정 사항 추가 <br> - 모션 사용법 .gif 파일 수정|
|2024-02-21|김용철|- mediapipe 라이브러리 활용하여 모션 인식 방법 고안 <br> - 모션 인식 마우스 이동 및 마우스 좌클릭 코드 작성 드래프트 완료|
|2024-02-22|임선웅|- Gantt Chart 작성 <br> - 3차 회의록 안건 작성 <br> - 발견된 문제점, 해결 방안과 여부 등록 <br> - 모션 사용법 (scroll up, down, exit) 추가 <br> - 프로세스 퀄리티 검토|
|2024-02-22|김승환|- 구글 어시스턴트 음성인식 스레드 작업 완료  <br> - 모션 인식 카메라와 디스플레이 맵핑 최적화 완료|
|2024-02-22|김용철|- 모션 인식 마우스 우클릭 코드 작성 드래프트 완료 <br> - 모션인식 카메라와 디스플레이 맴핑 최적화 완료 <br> - 모션 인식 알고리즘 최적화 완료|
|2024-02-23|김승환|- PyQT사용 로딩페이지, 엔딩페이지 구현|
|2024-02-23|임선웅|- 4차 회의록 안건 작성 <br> - badge 생성 <br> - 실사용 테스트를 통해 문제점 색출 <br> - 발견된 문제점에 대한 수정 작업 완료 <br> - 모션 사용법 (Backspace, Enter) 추가, (Double_Click) 수정 <br> - 프로세스 퀄리티 검토|
|2024-02-23|김용철|- 마우스 움직임 민감도 조절 완료 <br> - 추가된 모션에 대한 알고리즘 최적화 <br> -  발견된 문제점에 대한 수정 작업 완료 
|2024-02-23|김승환|- main코드 최종 검토 및 실행파일 생성<br> - 배포를 위해 드라이브에 업로드|


<br>

# 🔨실사용에 발견된 문제점 | 문제발견 담당자: 임선웅

|날짜|문제점|해결 방안|해결 여부|
|---|---|---|---|
|2024-02-22| - 손동작으로 인한 손가락 마커의 각도 인식 오류 <br> - 스크린 화면에 출력되는 HandMouse 이동의 불편함 | - 손가락 마카의 기준점을 변경하여 각도 수정 <br> - 모션인식 카메라와 디스플레이 맵핑 최적화 | 해결 <br> (김용철) |
|2024-02-23| - 마우스 커서의 높은 딜레이 | - 스레드 구현 | 해결 <br> (김승환) | 
|2024-02-23| - 마우스 스크롤의 현저히 느린 속도 | - scr_speed 코드 수정 | 해결 <br> (임선웅) |
|2024-02-23| - Backspace, Enter 기능의 부재 <br> - 프로세스 엔딩 출력 화면의 후순위 | - finger==1 (Backspace), finger==4 (Enter) 코드 구현 <br> - WindowStatysOnTop 코드 구현 | 해결 <br> (김승환) |

<br>

# 🚀핵심 기술 요약

## 손가락 인식

![After](proofvideo/finger_angle.png)
- 손가락을 인식하는 방법으로 손가락 각 마디에 대한 좌표를 이용해서 각도를 측정하였다.


|모션|음성인식 트리거|Backspace|마우스의 움직임, 좌클릭, 우클릭|마우스의 스크롤 업&다운|Enter|프로그램 종료|
|---|---|---|---|---|---|---|


## 마우스 움직임

 <div style="display:flex; flex-direction:row;">
    <img src="proofvideo/mouse_move_before.gif" style="width:150%;">
    <img src="proofvideo/mouse_move_after.gif" style="width:150%;">
</div>

`before`     &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;              `After`

마우스 움직임은 끊김없이 부드럽게 움직이게 하였다.


	
## 사용자 친화적인 마우스 컨트롤

![After](proofvideo/mouse_move_friendly.gif)

해당 프로그램 장기간 사용시 손과 어깨에 통증을 최소화시키고자 프레임 창에서 활동범위에 대한 알고리즘을 작성하였다. 

## 모션 사용법

### 마우스 클릭 (좌)
![마우스 클릭](proofvideo/mouseclick.gif)

### 마우스 더블클릭 (좌)
![마우스 더블클릭](proofvideo/mouse_double_click.gif)

### 마우스 클릭 (우)
![마우스 더블클릭](proofvideo/mouserightclick.gif)

### 마우스 이동
![마우스 드래그](proofvideo/mousedrag.gif)

### 마우스 스크롤 업
![마우스 스크롤 업](proofvideo/mouse_scroll_up.gif)

### 마우스 스크롤 다운
![마우스 스크롤 다운](proofvideo/mouse_scroll_down.gif)

### 키보드로 변경, 음성인식 시작
![마우스 클릭&드래그](proofvideo/mouse_to_keyboard.gif)

### Backspace
![Backspace](proofvideo/Backspace.gif)

### Enter
![Enter](proofvideo/Enter.gif)

### 나가기
![나가기](proofvideo/mouse_exit.gif)
