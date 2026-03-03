import requests
import dotenv
import os

from bs4 import BeautifulSoup

dotenv.load_dotenv()

def main():
    target_url = os.getenv("TASK1_URL")
    if not target_url:
        print("TASK1_URL is not set in the environment variables.")
        return
    
    response = requests.get(target_url)
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        question_line = soup.find(id='human-question')
        if not question_line:
            print("Could not find the question in the HTML content.")
            return
        question = question_line.text.split(":")[1].strip()
        print(f"Extracted question: {question}")
        chat_url = os.getenv("OLLAMA_CHAT_URL")

        headers = {
            "Content-Type": "application/json"
        }

        data = {
            "model": "qwen3.5:9b",
            "prompt": (
                f"""
                Answer provided question. Provide simple answer, without any explanations. If it is a question about a year, provide only the year.\n
                Question:  {question}"""
            ),
            "temperature": 0.2,
            "maxTokens": 10
        }
        print(f"Sending request to LLM with data: {data}")
        chat_response = requests.post(chat_url, json=data, headers=headers)
        print(chat_response.json())
        if chat_response.status_code == 200:
            answer = chat_response.json().get("choices", [{}])[0].get("text", '')
            print(f"Answer from LLM: {answer}")


    # TODO: send POST request adres: dotenv.get("TASK1_URL")
        final_response = requests.post(
            target_url,
            data={
                "username": os.getenv("TASK1_USERNAME"),
                "password": os.getenv("TASK1_PASSWORD"),
                "answer": answer
            },
            headers={
                "Content-Type": "application/x-www-form-urlencoded"
            }
        )
        print(f"Final response status code: {final_response.status_code}")
        print(f"Final response content: {final_response.text}")
    
main()