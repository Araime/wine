# Новое русское вино

Сайт магазина авторского вина "Новое русское вино".

### Как установить?

#### Скачать

Python3 должен быть уже установлен. Скачать этот репозиторий себе на компьютер.

Рекомендуется использовать [virtualenv/venv](https://docs.python.org/3/library/venv.html)
для изоляции проекта.

#### Быстрая настройка venv

Начниая с Python версии 3.3 виртуальное окружение идёт в комплекте в виде модуля
venv. Чтобы его установить и активировать нужно выполнить следующие действия в
командной строке:  

Указать скачанный репозиторий в качестве каталога.
```
cd C:\Users\ваш_пользователь\Downloads\папка_репозитория
```
Установить виртуальное окружение в выбраном каталоге.
```
Python -m venv env
```
В репозитории появится папка виртуального окружения env
<a href="https://imgbb.com/"><img src="https://i.ibb.co/Hn4C6PD/image.png" alt="image" border="0"></a>

Активировать виртуальное окружение.
```
env\scripts\activate
```
Если всё сделано правильно, вы увидите в командной строке (env) слева от пути 
каталога.
<a href="https://imgbb.com/"><img src="https://i.ibb.co/MZ72r22/2.png" alt="2" border="0"></a>

#### Установить зависимости

Используйте `pip` (или `pip3`, есть конфликт с Python2) для установки 
зависимостей:

```python
pip install -r requirements.txt
```

### Использование

Скрипт принимает данные в виде таблицы в формате xlsx следующего вида:

| **Категория**| **Название**      | **Сорт**      | **Цена**| **Картинка**           | **Акция**          |
|:-------------|:------------------|:--------------|:--------|:-----------------------|:-------------------|
|Белые вина    |Белая леди         |Дамский пальчик|399      |belaya_ledi.png         |Выгодное предложение|
|Напитки       |Коньяк классический|               |350      |konyak_klassicheskyi.png|                    |
|Красные вина  |Ркацители          |Ркацители      |499      |rkaciteli.png           |                    |

Разделяет данные из таблицы на количество категорий. С помощью цикла создаёт
ячейки товаров, подставляя в них значения из колонок: "название", "сорт", "цена".
Если в колонке "сорт" нет значения, оно не отображается у товара. Изображения
товаров берутся из папки images, нужно лишь добавить их туда и указать имя файла 
в колонке "картинка". Колонка "акция" используется для отображения ярлыка "выгдное 
предложение" для вин, помеченных в ней.

Примеры отображения позиций:  
<a href="https://imgbb.com/"><img src="https://i.ibb.co/L9kKxzd/image.png" alt="image" border="0"></a><br />

Если ячейка в колонке "сорт" пустая:  
<a href="https://imgbb.com/"><img src="https://i.ibb.co/P69nSch/2.png" alt="2" border="0"></a>

Использование колонки "акция":  
<a href="https://imgbb.com/"><img src="https://i.ibb.co/kJBVmCQ/8.png" alt="8" border="0"></a>

При запуске скрипта необходимо указать в качестве аргумента абсолютный путь до 
вашего файла с таблицей. Можно использовать тестовый файл wines, в репозитории.
```
python main.py C:\Users\Имя_пользователя\Downloads\projects\wine\wines.xlsx
```
Скрипт запущен, сайт доступен по локальному адресу [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков 
[dvmn.org](https://dvmn.org).