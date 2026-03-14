# Источники задач и контракты
## Описание проекта
Программа, принимающая обрабатывающая задачи из различных источников: ручной ввод, чтение из файла и API-запрос

## Архитектура
<pre>
src/
├── __main__.py              # Точка входа
├── cli.py                    # Интерфейс командной строки
├── contracts/                
│   ├── message.py            # Модель данных (Message)
│   └── message_source.py     # Контракт (MessageSource Protocol)
├── inbox/
│   └── core.py               # Ядро с проверкой контракта
├── sources/
│   ├── repository.py
│   ├── stdin.py               # Чтение из STDIN
│   ├── json.py                # Чтение из JSONL файлов
│   └── api.py                 # API-заглушка
└── common/
    └── config.py              # Логирование
<pre>

<h1> Поддерживаемые команды: <h1>
<ul>
<li>`python -m src plugins` - Показать доступные источники<li>
<li>`python -m src read --api 3` - Прочитать 3 сообщения из API-заглушки<li>
<li>`python -m src read --jsonl data.jsonl` - Прочитать из JSONL файла<li>
<li>`echo "1:Title:Author:Message" | python -m src read --stdin` - Прочитать из STDIN<li>
<li>`python -m src read --api 10 --contains "5"` - Фильтрация<li>
<ul>

<h1> 1. API-заглушка (api.py) <h1>
*   Имитирует внешний API
*   Параметры: count (количество), delay (задержка)
*   Генерирует уникальные UUID

<h1> 2. JSONL источник (json.py) <h1>
*   Читает файлы в формате JSON Lines
*   Каждая строка - отдельный JSON объект
*   Автоопределение ID из поля "id"

<h1> 3. STDIN источник (stdin.py) <h1>
*   Читает данные из стандартного ввода
*   Формат: id:title:author:content
*   Построчная обработка
