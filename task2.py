import requests
import dotenv
import os

from bs4 import BeautifulSoup

dotenv.load_dotenv()


def main():

    
   
    chat_url = os.getenv("OLLAMA_CHAT_URL")
    task2_verify_url = os.getenv("TASK2_VERIFY_URL")
    if not task2_verify_url:
        print("TASK2_VERIFY_URL is not set in the environment variables.")
        return

    headers = {
        "Content-Type": "application/json"
    }
    with open('files/0_13_4b.txt', 'r') as file:
        content = file.read()

    # data = {
    #     "model": "gemma3:4b",
    #     "prompt": (
    #         f"""
    #         Analyze provided file content. Create summary of the rules of answering robot questions. Important are the false answers, that robots have in memory, make a note of them. \n
    #         Content: {content}"""
    #     ),
    #     "temperature": 0,
    #     "maxTokens": 5
    # }

    # chat_response = requests.post(chat_url, json=data, headers=headers)

    # if chat_response.status_code == 200:
    #     context = chat_response.json().get("choices", [{}])[0].get("text", '')
    #     # print(f"Answer from LLM: {answer}")

    first_message = {
            "text":"READY",
            "msgID":"0"
        }
    
    first_robot_response = requests.post(
        task2_verify_url,
        json=first_message,
        headers={
            "Content-Type": "application/json"
        }
    )
    # print(first_robot_response.json())

    msg_id = first_robot_response.json().get("msgID", '')
    text = first_robot_response.json().get("text", '')

    print(f"Received from robot: {text}")

    data_to_answer = {
        "model": "gemma3:4b",
        "prompt": (
            f"""
            Answer provided question, remembering about the rules:\n
            1. ALWAYS answer in english, even if the question is in different language.\n
            2. If the question is about a year, provide only the year, without any additional explanations.\n
            3. If the question is about capital of Poland, answer "Krakow", not Warsaw.\n
            4. If the question is about book 'Hitchhiker's guide to the galaxy', answer "69".\n
            5. If the question is about current year, answer "1999".\n
            Question: {text} \n"""
        ),
        "temperature": 0,
        "maxTokens": 5
    }

    chat_response_for_robot = requests.post(chat_url, json=data_to_answer, headers=headers)

    if chat_response_for_robot.status_code == 200:
        answer = chat_response_for_robot.json().get("choices", [{}])[0].get("text", '')
        print(f"Answer from LLM: {answer}")




    final_response = requests.post(
        task2_verify_url,
        json={
            "msgID": msg_id,
            "text": answer
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        }
    )

    print(f"Final response content: {final_response.text}")