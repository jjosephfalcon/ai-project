# AI Chatbot HW

## First Task(fix)

Look at my comments and make the corresponding changes. The main issues in the code is you are manually printing to many lines
telling what Spongebon should say or do, it makes the code look clunky, the whole point of the app is to have the AI do your job,
every AI model knows what Spongebon is and how he reacts. 

## Second Task(fix)

You are not using any messages array to store the conversation history in your code. This is the biggest issue. 

## Your previous submission also hardcoded Spongebob as the character, the program was supposed to prompt the user to see what character they want to be

### What you had earlier for example was better


"

from openai import OpenAI
client = OpenAI()
character = input("What is your favorite cartoon character? ")
messages = [
    {"role": "system", "content": f"You are {character}. Stay in character for the entire conversation. Talk and act exactly like {character} would."}
]
print(f"\nNow chatting with {character}! Type 'quit' to exit.\n")
while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        print("Goodbye!")
        break
    messages.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})
    print(f"\n{character}: {reply}\n")


"

### Try to make your current code closer to that^, your earlier solution was almost perfect. Do not think more lines of code = better, 

More lines of code is usually worse to accomplish any project or goal in coding, you want your code to be as clean and efficient as possible. 

You can also get rid of the function. There's no reason to use a function right now to make it complicated.