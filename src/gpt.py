from openai import OpenAI
import os

client = OpenAI(
  api_key= os.environ['GPT_KEY'],
  base_url= os.environ['GPT_URL'],
)

def perform_request_chatGPT(history, current_user_message):
  messages = []
  for elem in history:
    messages.append({"role": "assistant", "content": elem[0]})
    messages.append({"role": "user", "content": elem[1]})
  messages.append({"role": "user", "content":current_user_message})

  completion = client.chat.completions.create(
    model="gpt-4o",
    store=True,
    messages=messages
  )
  return completion.choices[0].message.content