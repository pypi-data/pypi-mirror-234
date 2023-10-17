### Логгер

#### Совместная работа [loguru](https://loguru.readthedocs.io) & [rich](https://rich.readthedocs.io).

[Screenshot logger](https://disk.yandex.ru/i/JexFefETxnJavA)  
[Screenshot logger2](https://disk.yandex.ru/i/ubvT0kZbfS-Guw)

![Screenshot logger](wiki/logrich_screenshot.png?raw=True "Screenshot")
----
![Screenshot logger too](wiki/logrich_screenshot2.png?raw=True "Screenshot")

Уровень вывода исключений определяется в переменных окружения.
Цвета, ширины и шаблоны вывода также могут быть определены в окружении.

Обработчики записей логов можно определять дополнительно, например запись в файл или отправка в канал.

#### Использование

смотри [тест](tests/test_1.py) 

#### Как развернуть:

```shell
git clone 
cd logrich
poetry shell
poetry install
# создаём окружение
cp template.env .env
```

#### Запустить тест(ы):

```shell
pytest
# монитор тестов
ptw
```
