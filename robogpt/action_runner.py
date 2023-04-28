import io
import os
import subprocess

import actions
import gpt
from bs4 import BeautifulSoup
from googlesearch import search
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from spinner import Spinner


def run(action: actions.Action) -> str:
    try:
        if isinstance(action, actions.TellUserAction):
            print(f"Response: {action.message}")
            return action.message
        if isinstance(action, actions.ReadFileAction):
            if not os.path.exists(action.path):
                print(f"RESULT: File `{action.path}` does not exist.")
                return f"File `{action.path}` does not exist."
            with io.open(action.path, mode="r", encoding="utf-8") as file:
                contents = file.read()
                print(f"RESULT: Read file `{action.path}`.")
                return contents
        if isinstance(action, actions.WriteFileAction):
            with io.open(action.path, mode="w", encoding="utf-8") as file:
                file.write(action.content)
                print(f"RESULT: Wrote file `{action.path}`.")
                return "File successfully written."
        if isinstance(action, actions.RunPythonAction):
            with subprocess.Popen(
                f"python {action.path}",
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
            ) as process:
                process.wait()
                output = process.stdout.read() if process.stdout else ""
                print(f"RESULT: Ran Python file `{action.path}`.")
                return output
        if isinstance(action, actions.SearchOnlineAction):
            # TODO: This call sometimes stalls. Improve.
            response = search(term=action.query, num_results=10)
            if response is None:
                return f"RESULT: The online search for `{action.query}` appears to have failed."
            result = "\n".join([str(url) for url in response])
            print(f"RESULT: The online search for `{action.query}` returned the following URLs:\n{result}")
            return result
        if isinstance(action, actions.ExtractInfoAction):
            with Spinner("Reading website..."):
                html = get_html(action.url)
            text = extract_text(html)
            print(f"RESULT: The webpage at `{action.url}` was read successfully.")
            user_message_content = f"{action.instructions}\n\n```\n{text[:10000]}\n```"
            messages = [
                {
                    "role": "system",
                    "content": "You are a helpful assistant. You will be given instructions to extract some information from the contents of a website. Do your best to follow the instructions and extract the info.",
                },
                {"role": "user", "content": user_message_content},
            ]
            request_token_count = gpt.count_tokens(messages)
            max_response_token_count = gpt.COMBINED_TOKEN_LIMIT - request_token_count
            with Spinner("Extracting info..."):
                extracted_info = gpt.send_message(messages, max_response_token_count)
            print("RESULT: The info was extracted successfully.")
            return extracted_info
        raise NotImplementedError(f"Failed to run action: {action}")
    except Exception as exception:
        print(f"Failed to complete the action: {exception}")
        return f"Error: {exception}"


def get_html(url: str) -> str:
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options)
    browser.get(url)
    html = browser.find_element(By.TAG_NAME, "body").get_attribute("innerHTML")
    browser.quit()
    return html


def extract_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for script in soup(["script", "style"]):
        script.extract()
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = "\n".join(chunk for chunk in chunks if chunk)
    return text
