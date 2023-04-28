from dataclasses import dataclass
import os
import io
import subprocess
from googlesearch import search
from spinner import Spinner
import gpt
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options


@dataclass(frozen=True)
class Action:
    def key(self) -> str:
        raise NotImplementedError

    def short_string(self) -> str:
        raise NotImplementedError

    def run(self) -> str:
        """Returns what RoboGPT should learn from running the action."""
        raise NotImplementedError


@dataclass(frozen=True)
class TellUserAction(Action):
    message: str

    def key(self) -> str:
        return "TELL_USER"

    def short_string(self) -> str:
        return f'Tell user "{self.message}".'

    def run(self) -> str:
        return f"Told user the following: {self.message}"


@dataclass(frozen=True)
class ReadFileAction(Action):
    path: str

    def key(self) -> str:
        return "READ_FILE"

    def short_string(self) -> str:
        return f"Read file `{self.path}`."

    def run(self) -> str:
        if not os.path.exists(self.path):
            print(f"RESULT: File `{self.path}` does not exist.")
            return f"File `{self.path}` does not exist."
        with io.open(self.path, mode="r", encoding="utf-8") as file:
            contents = file.read()
            print(f"RESULT: Read file `{self.path}`.")
            return contents


@dataclass(frozen=True)
class WriteFileAction(Action):
    path: str
    content: str

    def key(self) -> str:
        return "WRITE_FILE"

    def short_string(self) -> str:
        return f"Write file `{self.path}`."

    def run(self) -> str:
        with io.open(self.path, mode="w", encoding="utf-8") as file:
            file.write(self.content)
            print(f"RESULT: Wrote file `{self.path}`.")
            return "File successfully written."


@dataclass(frozen=True)
class RunPythonAction(Action):
    path: str

    def key(self) -> str:
        return "RUN_PYTHON"

    def short_string(self) -> str:
        return f"Run Python file `{self.path}`."

    def run(self) -> str:
        with subprocess.Popen(
            f"python {self.path}",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
        ) as process:
            process.wait()
            output = process.stdout.read() if process.stdout else ""
            print(f"RESULT: Ran Python file `{self.path}`.")
            return output


@dataclass(frozen=True)
class SearchOnlineAction(Action):
    query: str

    def key(self) -> str:
        return "SEARCH_ONLINE"

    def short_string(self) -> str:
        return f"Search online for `{self.query}`."

    def run(self) -> str:
        # TODO: This call sometimes stalls. Improve.
        response = search(term=self.query, num_results=10)
        if response is None:
            return f"RESULT: The online search for `{self.query}` appears to have failed."
        result = "\n".join([str(url) for url in response])
        print(f"RESULT: The online search for `{self.query}` returned the following URLs:\n{result}")
        return result


@dataclass(frozen=True)
class ExtractInfoAction(Action):
    url: str
    instructions: str

    def key(self) -> str:
        return "EXTRACT_INFO"

    def short_string(self) -> str:
        return f"Extract info from `{self.url}`: {self.instructions}."

    def run(self) -> str:
        with Spinner("Reading website..."):
            html = self.get_html(self.url)
        text = self.extract_text(html)
        print(f"RESULT: The webpage at `{self.url}` was read successfully.")
        user_message_content = f"{self.instructions}\n\n```\n{text[:10000]}\n```"
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

    def get_html(self, url: str) -> str:
        options = Options()
        options.headless = True
        browser = webdriver.Firefox(options=options)
        browser.get(url)
        html = browser.find_element(By.TAG_NAME, "body").get_attribute("innerHTML")
        browser.quit()
        return html

    def extract_text(self, html: str) -> str:
        soup = BeautifulSoup(html, "html.parser")
        for script in soup(["script", "style"]):
            script.extract()
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = "\n".join(chunk for chunk in chunks if chunk)
        return text


@dataclass(frozen=True)
class ShutdownAction(Action):
    def key(self):
        return "SHUTDOWN"

    def short_string(self) -> str:
        return "Shutdown."

    def run(self) -> str:
        # This action is treated specially, so this can remain unimplemented.
        raise NotImplementedError
