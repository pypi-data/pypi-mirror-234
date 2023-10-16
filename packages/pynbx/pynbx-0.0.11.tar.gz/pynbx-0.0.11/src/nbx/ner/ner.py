from pathlib import Path
from typing import List, Tuple

from bs4 import BeautifulSoup
import openai


def extract_predefined_entities_text(input_html: str, remove_entity: bool = False):
    input_html = BeautifulSoup(input_html, features="html.parser")
    # extract predefined entities
    predefined_enities = []
    for entity in input_html.find_all("mark"):
        predefined_enities.append(entity.get_text())
        if remove_entity:
            entity.decompose()
    # extract text
    text = ""
    for paragraph in input_html.find_all("p"):
        text += paragraph.get_text() + "\n"
    return predefined_enities, text.strip()


def get_html_entity_dummy(input_html: str, prompt: str = "") -> Tuple[List[str], List[List[str]]]:
    predefined_entities, text = extract_predefined_entities_text(input_html, remove_entity=True)
    words = text.split(" ")
    entities = predefined_entities
    relations = []
    for word in words:
        entity = word.strip()
        if entity == "":
            continue
        entities.append(entity)
    for idx, entity in enumerate(entities):
        if idx == 0:
            continue
        relations.append([entities[idx-1], entity])
    return entities, relations


def get_html_entity_gpt3(input_html: str, prompt: str = "") -> Tuple[List[str], List[List[str]]]:
    input = BeautifulSoup(input_html, features="html.parser").get_text()
    token_file = Path(Path.home(), ".nbx/openai_token")
    # @TODO Add warning if token not configured
    with open(token_file, 'r') as f:
        openai.api_key = f.read()

    if prompt == "":
        prompt = f"""
Extract the entities of the input in the appearance order and separate by comma.

Input: "The stock market is in an recession now"
Entities: stock market, recession

Input: "{input}"
Entities:
"""
    prompt = prompt.strip()

    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt,
        temperature=0,
        max_tokens=60,
        top_p=1,
        frequency_penalty=0.5,
        presence_penalty=0
    )
    texts = response["choices"][0]["text"].split(",")
    entities = []
    for text in texts:
        if text.strip() == "":
            continue
        entities.append(text.strip())
    relations = []
    for idx, entity in enumerate(entities):
        if idx == 0:
            continue
        relations.append([entities[idx-1], entity])
    return entities, relations
