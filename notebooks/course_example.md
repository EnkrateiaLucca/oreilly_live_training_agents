# Introduction to AI and Large Language Models

This course is about understanding fundamental concepts behind Artificial Intelligence and the use of large language models  

## 1 - Creating Simple Prompts with Python

In this lesson, you'll learn how to interact with a language model by writing prompts in Python.

**Example:**

```python
# Example using OpenAI's API (requires openai package)
import openai

openai.api_key = "YOUR_API_KEY"

prompt = "What are three benefits of learning Artificial Intelligence?"

response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=prompt,
    max_tokens=100
)

print(response.choices[0].text.strip())
```

**Exercise:**  
- Change the `prompt` variable to ask your own question.
- Observe how the language model responds!