import os

from dotenv import load_dotenv

from groq import Groq

load_dotenv(override=True)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

char = input("What character do you want? (or quit): ")

messages = [{"role": "system", "content": f"You are {char}. Stay in character at all times."}]
while True:
    user_input = input("You: ")

    if user_input.lower() == "quit":
        print(f"{char}: Goodbye!")
        break

    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )
    reply = response.choices[0].message.content.strip()

    messages.append({"role": "assistant", "content": reply})

    print(f"{char}: {reply}")
