from google import genai

client = genai.Client(api_key="AIzaSyBU-gZkzsQ9TNB5ea67ITKnTYkVrL1nlWM")

models = client.models.list()

for m in models:
    print(m.name)