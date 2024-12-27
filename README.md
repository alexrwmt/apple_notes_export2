# Apple Notes Sync

Проект для экспорта заметок из Apple Notes.

## Структура проекта

```
apple-notes-sync/
├── src/
│   ├── main.py              # точка входа в приложение
│   ├── exporters/           # модуль для экспорта
│   ├── templates/           # модуль для HTML шаблонов
│   └── utils/               # вспомогательные функции
├── requirements.txt         # зависимости проекта
└── tests/                  # тесты
```

## Установка

1. Клонируйте репозиторий
2. Установите зависимости: `pip install -r requirements.txt`

## Использование

Запустите `main.py` для экспорта заметок:
```python
python src/main.py
```
