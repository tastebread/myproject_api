# MyProject - 게시판 및 마이페이지 기능 구현
## 🚀 프로젝트 개요
MyProject는 **Django REST Framework(DRF)와 Next.js를 기반으로 한 게시판 시스템**입니다.  
사용자는 **게시글을 작성, 수정, 삭제**할 수 있으며, **댓글, 좋아요, 북마크** 등의 기능을 제공합니다.  
또한, **마이페이지에서 내가 작성한 게시글과 댓글을 확인**할 수 있습니다.

## 📌 주요 기능
###  **회원 관련 기능**
- JWT 기반 회원가입 및 로그인 (Django REST Framework + Simple JWT)
- 소셜 로그인 (추후 추가 예정)
- 프로필 관리 (이메일, 프로필 사진 업데이트)

###  **게시판 기능**
- 게시글 작성, 조회, 수정, 삭제
- 게시글 목록에서 **검색, 태그, 카테고리별 필터링, 정렬**
- **무한 스크롤 (추후 추가 예정)**

###  **댓글 및 좋아요**
- 댓글 작성, 조회, 삭제
- **게시글 좋아요 / 좋아요 취소**
- **댓글 좋아요 (추후 추가 예정)**

###  **마이페이지**
- **내가 작성한 게시글 목록**
- **내가 작성한 댓글 목록**
- **내가 좋아요 누른 게시글, 댓글 보기 (추후 추가 예정)**
- **내가 북마크한 게시글 보기 (추후 추가 예정)**

---

## 🛠️ 기술 스택
###  **백엔드 (Django REST Framework)**
- Python 3
- Django 4
- Django REST Framework (DRF)
- JWT 인증 (Simple JWT)
- PostgreSQL (or SQLite for development)
- Docker + Gunicorn (배포 시 사용)

###  **프론트엔드 (Next.js + TypeScript)**
- Next.js (App Router)
- TypeScript
- Tailwind CSS
- Axios (API 요청)
- Context API (사용자 인증 관리)

## 📌 실행 방법 (로컬 개발)   
### 1️⃣ **백엔드 실행**   
```bash
# 프로젝트 클론 및 이동
git clone https://github.com/yourusername/myproject.git
cd myproject

# 가상환경 생성 및 활성화 (선택)
python3 -m venv venv
source venv/bin/activate  # macOS / Linux
venv\Scripts\activate  # Windows

# 패키지 설치 및 실행
pip3 install -r requirements.txt
python3 manage.py migrate
python3 manage.py runserver

### ✅ **개발 및 배포**
- Docker (로컬 개발 환경 및 배포)
- GitHub Actions (CI/CD - 추후 추가 예정)
- Vercel or AWS 배포 (프론트엔드)

---
