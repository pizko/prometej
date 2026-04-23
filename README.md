# Prometej

Статическая версия сайта для публикации через GitHub Pages.

## Что работает на GitHub Pages

- HTML-страницы
- CSS
- JavaScript
- изображения и документы

## Что не будет работать на GitHub Pages

- `send.php`
- `captcha.php`

GitHub Pages не исполняет PHP, поэтому визуальную часть сайта здесь можно
показывать и править, но рабочую форму заявки потом нужно будет подключать на
PHP-хостинге или заменить на внешний обработчик.

## Локальный просмотр

Можно просто открыть `index.html` в браузере.

## Города

В проекте есть заготовка под локальные страницы городов:

- данные лежат в `data/cities.json`
- генератор лежит в `scripts/generate_cities.py`
- готовые страницы попадают в `cities/<slug>/index.html`

Запуск генератора:

```bash
python3 scripts/generate_cities.py
```

После этого обновляется:

- `cities/index.html`
- страницы конкретных городов

Стартовые примеры уже добавлены:

- `cities/krasnodar/`
- `cities/sochi/`
- `cities/murmansk/`
- `cities/sankt-peterburg/`

## Галерея

Фотографии лежат в папке `photo/`.

Как это работает:

- если файл просто лежит в `photo/`, он автоматически подтянется в галерею
- если нужна красивая подпись или ручной порядок, используй `photo/photos.json`

## Публикация

После пуша в ветку `main` можно включить GitHub Pages:

- `Settings`
- `Pages`
- `Build and deployment`
- `Source: Deploy from a branch`
- `Branch: main`
- `Folder: /(root)`
