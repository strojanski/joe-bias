import requests


prompt = "Write Haiku about Dragonhack"
model = "gpt-3.5-turbo"
token = open("gpt4_token", "r").read().strip()


response = requests.post(
   "https://openai-api.meetings.bio/api/openai/chat/completions",
   headers={"Authorization": f"Bearer {token}"},
   json={
       # specification of all options: https://platform.openai.com/docs/api-reference/chat/create
       "model": model,
       "messages": [{"role": "user", "content": prompt}],
   },
)

print(response)

if response.ok:
   print(response.json()["choices"][0]["message"]["content"])
