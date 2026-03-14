from pathlib import Path
from typing import List, Any, Optional
from collections.abc import Iterable

import typer
from typer import Typer


from src.inbox.core import InboxApp
import tempfile
from src.sources.repository import REGISTRY
from src.contracts.message_source import MessageSource
from src.contracts.message import Message






def test_build_stdin_source():
    source = (REGISTRY["stdin"]())
    
    assert isinstance(source, MessageSource)
    
    assert hasattr(source, 'name')
    assert hasattr(source, 'fetch')



def test_build_jsonl_source():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
        f.write('{"id": "1", "title": "Test", "author": "Author", "content": "Message"}\n')
        temp_path = Path(f.name)
    
    try:
        source = REGISTRY["file-jsonl"](path=temp_path)
        
        assert isinstance(source, MessageSource)
        
        messages = list(source.fetch())
        assert len(messages) == 1
        assert messages[0].id == "1"
        
        
    finally:
        temp_path.unlink()


def test_build_api_source():
    api_count = 5
    source = REGISTRY["api"](count=api_count, delay=0.1)
    
    assert isinstance(source, MessageSource)
    
    assert hasattr(source, 'name')
    assert hasattr(source, 'fetch')


    messages = list(source.fetch())
    assert len(messages) == api_count