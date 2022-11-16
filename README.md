## КОЛЛЕКТОР
#### Тестовое задание на позицию разработчика в компанию DataFort
#### Релиз: 16\11 2022
### Какие задачи необходио решить:
1. Напиши Коллектор (сущность, отвечающую за сбор статистики) для https://openweathermap.org/
2. Который должен каждый час собирать информацию о погоде для 50 крупнейших городов мира
3. Сохранять значение в БД. При сборе обрати внимание на побочные данные, которые можно получить.
При написании следует учитывать, что код может часто меняться, поэтому следует подумать о его расширении и дальнейшей поддержке.

### О коллекторе – подробнее:
Опционально:
Описать почему выбрана такая структура БД?

"Выбрал реляционную базу данных, в частности PostgreSQL.
Данные и связи между данными организованы с помощью таблиц. Каждый столбец в таблице имеет имя и тип. Каждая строка представляет отдельную запись или элемент данных в таблице, который содержит значения для каждого из столбцов.
1. Поле в таблице, называемое внешним ключом, может содержать ссылки на столбцы в других таблицах, что позволяет их соединять;
2. Высокоорганизованная структура и гибкость делает реляционные БД мощными и адаптируемыми ко различным типам данных;
3. Для доступа к данным используется язык структурированных запросов (SQL);
4. Надёжный выбор для многих приложений.

Почему выбрана та или иная технология?

```
Для сбора данных по API выбрал стандартную библеотеку requests.
Для приобразования данных с последующей передачей в Базу Данных, выбрал библиотеку Pandas.
Данные библиотеки имеют общераспространенную практику, включают в себя мощные инструменты по работе с данными"
```

Какие технологические ограничения есть на данном этапе?

```
Постарался исключить возможные ограничения. Тем не менее, в случае изменения названия столбцов, в Базе данных они отразятся, но как новые столбцы.
Так же, лучше сделать парсер данных по топ 50 городов (если необходима динамика изменений или увеличить число более 50)
```

В репозитории должен быть файл readme, в котором содержится документация и инструкция по запуску.

Установить виртуальное окружение:
```
python3 -m venv venv
```

Создаем и заполняем файлы .env и config.ini, в шаблонах указано как:
```
config.ini.template
```

Устанавливаем Docker (для развертывания контейнера)
```
# Установка утилиты для скачивания файлов
sudo apt install curl
# Эта команда скачает скрипт для установки докера
curl -fsSL https://get.docker.com -o get-docker.sh
# Эта команда запустит его
sh get-docker.sh
Для начала запустите команду удаления старых версий Docker.
Скорее всего, их на вашем компьютере нет, но подстраховаться не помешает:
sudo apt remove docker docker-engine docker.io containerd runc
Чтобы устанавливать новые версии пакетов и утилит, обновите их список для менеджера пакетов ATP:
# Обновить список пакетов
sudo apt update
Затем установите пакеты для работы через протокол https,
это нужно для получения доступа к репозиторию докера:
# Установить необходимые пакеты для загрузки через https
sudo apt install \
apt-transport-https \
ca-certificates \
curl \
gnupg-agent \
software-properties-common -y
Добавьте ключ GPG для подтверждения подлинности в процессе установки:
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
# В консоли должно вывестись ОК
apt-key добавляет ключ от репозиториев в систему. Ключи защищают репозитории от подделки пакета.
Добавьте репозиторий Docker в пакеты apt:
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
Так как в APT был добавлен новый репозиторий, снова обновите индекс пакетов:
sudo apt update
Установите Docker, а вместе с ним Docker Compose — без него не получится развернуть проект,
а это будет вашей основной задачей в спринте:
sudo apt install docker-ce docker-compose -y
Проверьте, что Docker работает:
sudo systemctl status docker
```
Запускаем контейнеры)

```
docker-compose up -d
```


Обязательно:
При первоначальной настройке и запуске компоуза коллектор начнет работать и собирать данные.

```
работает
```

Результат должен быть размещен на гитхабе, ссылка на который скинута в мой телеграм :) 
