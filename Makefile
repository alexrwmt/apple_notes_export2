.PHONY: run clean install lint format dev-install

# Помощь по доступным командам
help:
	@echo "Доступные команды:"
	@echo "  make run        - Запуск приложения"
	@echo "  make clean      - Удаление директории notes"
	@echo "  make install    - Установка зависимостей"
	@echo "  make dev-install - Установка пакета в режиме разработки"
	@echo "  make clean-py   - Очистка Python кэша"
	@echo "  make lint       - Проверка кода линтером"
	@echo "  make format     - Форматирование кода"
	@echo "  make help       - Показать это сообщение"


# Установка зависимостей
install:
	pip install -r requirements.txt

# Установка в режиме разработки
dev-install:
	pip install -e .

# Запуск основного приложения
run:
	python src/main.py

# Запуск линтера
lint:
	black --check src/
	isort --check src/
	pylint src/

# Форматирование кода
format:
	black src/
	isort src/

# Очистка директории notes
clean:
	rm -rf notes/
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
