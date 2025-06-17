import pytest
from unittest.mock import patch, AsyncMock
from app.services.openai_service import summarize_text
from app.utils import SummaryLength

@pytest.mark.asyncio
async def test_summarize_text_calls_openai_correctly():
    fake_response = AsyncMock()
    fake_response.choices = [type("obj", (object,), {"message": type("msg", (object,), {"content": "Summary!"})})]
    
    with patch("openai.ChatCompletion.acreate", return_value=fake_response):
        result = await summarize_text("some text", SummaryLength.SHORT)
        assert result == "Summary!"
