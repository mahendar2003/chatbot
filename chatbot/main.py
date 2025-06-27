import openai

# Replace with your actual API key
openai.api_key = "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"  # Your API key

# Test the API key by making a simple request to OpenAI
try:
    response = openai.Completion.create(
        model="gpt-3.5-turbo",
        prompt="Hello, OpenAI!",
        max_tokens=5
    )
    print("API response:", response)
except openai.error.OpenAIError as e:
    print("OpenAI API error:", e)
