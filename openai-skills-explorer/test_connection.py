from config import client,MODEL

response = client.responses.create(
    model = MODEL,
    input= "Reply with exactly: Connection successful!"
)
print(response.output_text)