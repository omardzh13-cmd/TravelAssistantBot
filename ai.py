from openai import OpenAI
from config import DEEPSEEK_API_KEY

client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com"
)


def get_ai_advice(city, temperature, wind):

    prompt = f"""
Ты опытный помощник путешественника.

Город: {city}
Температура: {temperature}°C
Ветер: {wind} км/ч

Дай краткий совет путешественнику (2–3 предложения).
"""

    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=[
            {
                "role": "system",
                "content": "Ты опытный туристический помощник."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content