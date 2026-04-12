from groq import Groq
import os

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def get_response(user_input):
    try:
        messages = [
            {
                "role": "system",
                "content": "You are a medical assistant. Give short, clear, and concise answers. Limit response to 5-6 sentences unless the user asks for details."
            },
            {
                "role": "user",
                "content": user_input
            }
        ]

        response = client.chat.completions.create(
            messages=messages,
            model="llama-3.1-8b-instant",
            max_tokens=120
        )

        return response.choices[0].message.content

    except Exception as e:
        print("Error:", e)
        return "Error generating response"