import anthropic

client = anthropic.Anthropic()  # automatically uses ANTHROPIC_API_KEY env var

response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=32,
    messages=[{"role": "user", "content": "Say 'API connection successful!'"}]
)

print(response.content[0].text)