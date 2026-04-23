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

## Публикация

После пуша в ветку `main` можно включить GitHub Pages:

- `Settings`
- `Pages`
- `Build and deployment`
- `Source: Deploy from a branch`
- `Branch: main`
- `Folder: /(root)`
