# FOODGRAM

[51.250.29.190](https://github.com/Skakovsku/foodgram-project-react/actions/workflows/main.yml/badge.svg?event=push)

### Краткое описание проекта

Проект представляет собой приложение [foodgram-project-react](https://github.com/Skakovsku/foodgram-project-react). Может быть использован при ведении домашнего хозяйства. Проект имеет возможность описания и хранения рецептов приготовления раличных блюд, а также формирования списка планируемых покупок для реализации выбранных наборов рецептов.
В проект встроена функция автоматического обновления образа на сервисе DockerHub при обновлении кода на GitHub командой "PUSH". Образ backend-части проекта на DockerHub - skakovsku/foodgram.

### Технологии

- Python
- Django
- rest-framework
- docker
- nginx

### Образец заполнения .env файла

В корневой папке создайте файл .env со следующим содержимым:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db
DB_PORT=5432
```

### Установка проекта на локальном компьютере

- В терминале перейдите в директорию infra_sp2/infra/;
- Для сборки и запуска контейнеров из папки foodgram-project-react/infra/ выполните команду:
```
sudo docker-compose up -d
```
- Создайте и выполните миграции:
```
sudo docker-compose exec backend python manage.py makemigrations
sudo docker-compose exec backend python manage.py migrate
```
- Создайте суперпользователя:
```
sudo docker-compose exec backend python manage.py createsuperuser
```
- Соберите статические файлы:
```
sudo docker-compose exec backend python manage.py collectstatic --no-input
```

### База данных

Для ручного заполнения базы данных перейдите в браузере по адресу:
```
http://localhost/admin/
```
Ведите данные суперпользователя и работайте на сайте администратора.

### Автор:

Евгений Скаковский, кагорта 26

Сервер: product_server
IP: 51.250.29.190

### Админ:

username: admin
password: Test1976