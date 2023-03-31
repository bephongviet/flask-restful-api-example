# Giới thiệu 

base code cho các dự án dùng Flask, Flask RESTful và Flask SQL-Alchemy để phát triển RESTful API cho app của mình.

# Các RESTful API 

1. Authentication bằng social login (Google và Facebook). Xem cách sử dụng với next.js tại đây.

# Thiết lập 

## 1. Cấu hình 

- Python 3.8 trở lên 
- Flask 2.2 (https://flask.palletsprojects.com)
- Flask RESTful: 1 framework hữu ích của flask để viết REST APIs (https://flask-restful.readthedocs.io/en/latest/)
- Flask SQL-Alchemy: ORM để truy vấn database (https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/)
- Flask Migrate: để tạo migration cho cơ sở dữ liệu (https://flask-migrate.readthedocs.io/en/latest/)
- Flask JWT Extended: để tạo jwt token và các hàm kiểm tra giá trị token được cung cấp bởi frontend (https://flask-jwt-extended.readthedocs.io/en/stable/)
- Flask Login: quản lý user và user session (https://flask-login.readthedocs.io/en/latest/)
- Flask RBAC: quản lý vai trò user. Phần lớn các ứng dụng doanh nghiệp đều cần có khả năng này. (https://flask-rbac.readthedocs.io/en/latest/)
- Flask CORS: CORS cho phép frontend nào call api của app (https://flask-cors.readthedocs.io/en/latest/)

## 2. Cài đặt base code

### 1. Clone git:

```bash
git clone ...
```

### 2. Tạo virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Cài đặt thư viện 

Sau khi đã bật virtual environment, thực hiện cài các thư viện:

```bash
pip install Flask Flask-RESTful Flask-Login Flask-SQLAlchemy mysql-connector-python flask-cors python-dotenv pytest Flask-Migrate flask-jwt-extended flask-rbac
```

### 4. Tạo file `.env`

Tạo file `/instance/.env` và cập nhật nội dung phù hợp cho môi trường và database của bạn:

```bash
MYSQL_DB_HOST='127.0.0.1'
MYSQL_DB_PORT=3306
MYSQL_DB_USER='root'
MYSQL_DB_PASS='root'
MYSQL_DB_NAME='db_name'
SECRET_KEY='eate'
JWT_SECRET_KEY='NHp;#%arntd*DJg-stsABmiw5m'
TESTING=True
DEBUG=True
FLASK_ENV='development'
SQLALCHEMY_ECHO=False
UPLOAD_FOLDER='/path/to//uploads/'
```

### 5. Chạy thử app

Kích hoạt virtual environment và chạy migrate

```bash
export FLASK_APP=kernelapp
flask db init
flask db migrate
flask db upgrade
```

Sau đó chạy flask:

```bash
flask run --port=5005
```

Chạy thử authenticate api:

```bash
curl --location 'http://localhost:5006/api/authenticate' \
--header 'Content-Type: application/json' \
--data-raw '{"id":"109351424427926100773","name":"Social User","email":"social@linxhq.com","image":"https://lh3.googleusercontent.com/a/AGNmyxZI","provider":"google","type":"oauth","providerAccountId":"109351424427926100788","access_token":"ya29.a0Ael9sCNQrBwop8gmHNHIAmti4IEjx7_iOBgjj0QUnTulQ6NHceobyhSOz-2ocadR4XDdz1s9guj3EErLepHYZOCvXw8URuFJH6QSjJqc96mMUNAAqORjW9PJl282Nfrnf0Vt_2KS8ORCzNAul2msHBkkCjh-aCgYKASISARASFQF4udJhrO-BOqi24_8OLY7AYfJmCg0163","expires_at":1679911181,"scope":"https://www.googleapis.com/auth/userinfo.email openid https://www.googleapis.com/auth/userinfo.profile","token_type":"Bearer","id_token":"..."}'
```

API call này giả định rằng user đã login ở frontend qua google social login, sau đó app tiếp tục gọi backend authenticate để lấy access_token của kernelapp. 

Test call này sẽ tạo 1 record trong bảng users và bảng social_profiles. Bạn nhớ delete record sau khi test thành công.

# Triển khai dự án trên production với `gunicorn`

### 1. Tạo `requirements.txt` nếu cần 

```commandline
pip freeze > requirements.txt
pip install < requirements.txt
```

### 2. Cài `gunicorn` và cấu hình `nginx`

Kích hoạt virtual environment và chạy lệnh sau:

```bash
pip install gunicorn
```

Cài đặt nginx và cấu hình nginx như sau:

```bash
server {
    listen 80;
    server_name <domain của dự án>.com;

    location / {
        proxy_pass http://localhost:5005;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### 3. Bật `unicorn` server

```commandline
screen -S kernalapp-api
gunicorn --workers 4 --timeout 180 --bind localhost:5005 "kernelapp:create_app()"

# press Ctrl + a + d to exit screen
screen -ls # to list screens
screen -r <screen id> # to go back to a screen
```
