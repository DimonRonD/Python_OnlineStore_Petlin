Проект: Сайт интернет-магазина

Имя Фамилия Петлин Дмитрий / Petlin Dmitry

логин на GitHub — DimonRonD

e-mail — DimonRonD@gmail.com

#Для запуска контейнеров в Docker использую команды:

docker-compose up db - для запуска контейнера с базой

docker-compose up web - для запуска web-сервера

Если запускаю одновременно, то БД стартует позже web-части и это может приводить к ошибкам.

#Экспорт и импорт данных

Команды export_product_residue.py и load_goods.py работают с файлом residue_data.json
Остатки загружаются в Warehouse.

#Первоначальная загрузка данных для тестирования

В файле data.json лежат тестовые данные, загружать командой python manage.py loaddata data.json
Созданы пользователи ivan@iv.an, petr@iv.an с паролем 1 (единица).

