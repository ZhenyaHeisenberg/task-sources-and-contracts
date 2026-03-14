#!/usr/bin/env python3
"""
Тестирование соблюдения контракта MessageSource
"""

import sys
from src.contracts.message_source import MessageSource
from src.contracts.message import Message
from src.sources.json import JsonlSource
from src.sources.stdin import StdinLineSource
from src.sources.api import ApiSource
from src.inbox.core import InboxApp
from pathlib import Path

def setup_windows_encoding():
    """Настройка кодировки для Windows"""
    if sys.platform == "win32":
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def test_contract_compliance():
    """Тест 1: Проверка соответствия контракту"""
    print("\n1. ПРОВЕРКА СООТВЕТСТВИЯ КОНТРАКТУ")
    print("-" * 40)
    
    sources = [
        ("JSON Lines", JsonlSource(Path("test.jsonl"))),
        ("STDIN", StdinLineSource()),
        ("API Stub", ApiSource(count=3))
    ]
    
    for name, source in sources:
        is_compliant = isinstance(source, MessageSource)
        status = "+" if is_compliant else "-"  # Заменили юникод на ASCII
        print(f"{status} {name}: {type(source).__name__}")
        
        if not is_compliant:
            print(f"   Требуется: атрибут 'name' и метод 'fetch()'")
            print(f"   Имеет: name={hasattr(source, 'name')}, fetch={hasattr(source, 'fetch')}")

def test_inbox_app():
    """Тест 2: Проверка InboxApp с разными источниками"""
    print("\n2. ПРОВЕРКА InboxApp")
    print("-" * 40)
    
    try:
        app = InboxApp([
            ApiSource(count=2),
            StdinLineSource()
        ])
        print("+ InboxApp успешно создан")
        
        # Проверяем получение сообщений
        messages = list(app.iter_messages())
        print(f"+ Получено сообщений: {len(messages)}")
        
    except TypeError as e:
        print(f"- Ошибка: {e}")

def test_extensibility():
    """Тест 3: Проверка расширяемости"""
    print("\n3. ПРОВЕРКА РАСШИРЯЕМОСТИ")
    print("-" * 40)
    
    # Создаем новый источник "на лету"
    class CustomSource:
        def __init__(self):
            self.name = "custom"
        
        def fetch(self):
            yield Message(
                id="custom-1",
                title="Custom Source",
                author="Test",
                message="Легко добавляется!"
            )
    
    source = CustomSource()
    print(f"CustomSource соответствует контракту? {isinstance(source, MessageSource)}")
    
    try:
        app = InboxApp([source])
        msg = list(app.iter_messages())[0]
        print(f"+ CustomSource работает: {msg.title}")
    except TypeError as e:
        print(f"- Ошибка: {e}")

def test_runtime_check():
    """Тест 4: Демонстрация runtime проверки"""
    print("\n4. RUNTIME ПРОВЕРКА")
    print("-" * 40)
    
    # Неправильный источник (нет fetch)
    class BadSource:
        name = "bad"
        # нет метода fetch!
    
    try:
        app = InboxApp([BadSource()])
        print("- Должно было упасть!")
    except TypeError as e:
        print(f"+ Правильно упало: {e}")

if __name__ == "__main__":
    setup_windows_encoding()
    
    print("=" * 50)
    print("ТЕСТИРОВАНИЕ КОНТРАКТА MESSAGESOURCE")
    print("=" * 50)
    
    test_contract_compliance()
    test_inbox_app()
    test_extensibility()
    test_runtime_check()
    
    print("\n" + "=" * 50)
    print("Все тесты завершены")