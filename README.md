# 1 Начало:
## Установите git если его ещё нет:
Перейдите на [оффициальный сайт](https://git-scm.com/) и скачайте нужную версию git для вашего устройства.

### Скачивание проекта к себе на устройство
```
git clone https://github.com/Sskame1/School-Control.git
```
### Создания виртуального окружение
```
python -m venv venv
```
### Войдите в виртуальное окружение
Windows:
```
.\venv\Scripts\activate
```
Linux/MacOs:
```
source venv/bin/activate
```
### Установка всех зависимостей для проекта
```
pip install -r requirements.txt
```
# 2 Установка и запуск Docker для БД
## Установите Docker
Перейдите на [оффициальный сайт](https://www.docker.com/products/docker-desktop) docker-desktop для Windows.
Для Linux и MacOS когда-нибудь напишу
## Запуск Docker
Выполните команду для запуска:
```
docker-compose up -d
```  
Для выключение docker выполните команду:
```
docker-compose down
```

# 3 Запуск проекта
## Миграции БД
```
python manage.py makemigrations
```
и
```
python manage.py migrate
```
## Запуск проекта 
Если вы уже в виртуальном окружение venv то используйте эту команду для запуска django:
```
python manage.py runserver
```