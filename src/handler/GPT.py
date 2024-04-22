import requests

def chatbot_response(msg):
	url = "https://custom-chatbot-api.p.rapidapi.com/chatbotapi"

	payload = {
		"bot_id": "OEXJ8qFp5E5AwRwymfPts90vrHnmr8yZgNE171101852010w2S0bCtN3THp448W7kDSfyTf3OpW5TUVefz",
		"messages": [
			{
				"role": "user",
				"content": msg
			}
		],
		"user_id": "",
		"temperature": 0.9,
		"top_k": 5,
		"top_p": 0.9,
		"max_tokens": 256,
		"model": "matag2.0"
	}
	headers = {
		"content-type": "application/json",
		"X-RapidAPI-Key": "2805b67089msh0dbcb3365d5c76ep101da6jsnf8c6f46f7889",
		"X-RapidAPI-Host": "custom-chatbot-api.p.rapidapi.com"
	}

	response = requests.post(url, json=payload, headers=headers)
	result = response.json()
	return result['result']


# url = "https://ai-api-textgen.p.rapidapi.com/completions"

# payload = {
# 	"init_character": "you are scientist",
# 	"user_name": "",
# 	"character_name": "Albert Einstein",
# 	"text": "Bạn có thể nói một chút về thuyết tương đối rộng"
# }
# headers = {
# 	"content-type": "application/json",
# 	"X-RapidAPI-Key": "2805b67089msh0dbcb3365d5c76ep101da6jsnf8c6f46f7889",
# 	"X-RapidAPI-Host": "ai-api-textgen.p.rapidapi.com"
# }

# response = requests.post(url, json=payload, headers=headers)

# print(response.json())