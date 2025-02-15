from .cutomer import Customer
from .product import Product
from .defaults import SarvamAIPaths
from dataclasses import dataclass
import requests
import json
import logging
import base64
from .audio import PlayAudio
import os

logger = logging.getLogger(__name__)


class Agent:
    stop_words = ["Close", "Stop"]

    def __init__(self, sarvam: "Sarvam"):
        self.llm = sarvam
        self.pa = PlayAudio()

    def converse(self, customer: Customer, product: Product):
        # Sales Agent Initial Pitch
        question = f"Generate shortest sales pitch text for sales representative to speak to {customer.name} describing about the credit card information shared."
        description = "prepare sales pitch as short as possible and include customer name in the pitch."
        customer_interactions = 0
        logger.info("Generating Initial Sales Pitch")
        while True:
            logger.info("Customer Interactions: %d", customer_interactions)
            answer = self.llm.answer(
                product.content,
                Question(question=question, id=customer_interactions),
                description,
            )
            n_iters = len(answer.response) // 499
            for n in range(n_iters + 1):
                response = self.llm.tts(answer.response[n * 499 : (n + 1) * 499])
                logger.info("Playing %d/%d audio_part", n + 1, n_iters + 1)
                self.pa.play(response.audio)
            logger.info("Expecting input from the customer")
            customer_audio = self.pa.record()
            customer_interactions += 1
            logger.info("Converting customer's speech to text")
            logger.info(
                "Length of Customer Audio in no: of bytes %d", len(customer_audio)
            )
            stt = self.llm.stt(customer_audio)
            question = stt.text
            description = "Answer customer's question with provided context."
            for sp in self.stop_words:
                if sp in question:
                    response = self.llm.tts("Thank you! Hope I served you better")
                    self.pa.play(response.audio)
                    return


@dataclass
class Answer:
    question: "Question"
    response: str
    reasoning: str
    utterance: str


@dataclass
class Question:
    question: str
    id: int


@dataclass
class TTS:
    audio: bytes
    text: str


@dataclass
class STT:
    text: str
    lang_code: str


class Sarvam:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.common_headers = {"api-subscription-key": self.api_key}

    @classmethod
    def from_env(cls):
        return Sarvam(os.environ["SARVAM_AI_API"])

    def answer(self, context: str, question: Question, description: str):
        url = f"{SarvamAIPaths.url}/{SarvamAIPaths.text_analytics}"
        headers = {
            **self.common_headers,
        }
        data = {
            "text": context,
            "questions": json.dumps(
                [
                    {
                        "id": f"{question.id}",
                        "text": question.question,
                        "description": description,
                        "type": "short answer",
                        "properties": {},
                    }
                ]
            ),
        }
        try:
            response = requests.post(url=url, headers=headers, data=data)
            if response.status_code != 200:
                raise ValueError(
                    f"Response from Sarvam Failed with status code: {response.status_code} for {response.text}"
                )
            resp = response.json()["answers"][0]
            return Answer(
                response=resp["response"],
                reasoning=resp["reasoning"],
                utterance=resp["utterance"],
                question=question,
            )
        except Exception as e:
            logger.exception("Sarvam Response Error for text-analytics.")
            raise e

    def tts(self, text: str):
        url = f"{SarvamAIPaths.url}/{SarvamAIPaths.tts}"
        headers = {
            **self.common_headers,
        }
        # THe default params didn't work data = {"inputs": [text], "target_language_code": "hi-IN"}
        data = {
            "inputs": [text],
            "target_language_code": "en-IN",
            "speaker": "meera",
            "pitch": 0,
            "loudness": 1.5,
            "speech_sample_rate": 8000,
            "enable_preprocessing": False,
            "model": "bulbul:v1",
        }
        try:
            response = requests.post(url=url, headers=headers, json=data)
            if response.status_code != 200:
                raise ValueError(
                    f"Response from Sarvam Failed with status code: {response.status_code} for {response.text}"
                )
            resp = response.json()
            return TTS(audio=base64.b64decode(resp["audios"][0]), text=text)
        except Exception as e:
            logger.exception("Sarvam Response Error for tts")
            raise e

    def stt(self, audio: bytes):
        url = f"{SarvamAIPaths.url}/{SarvamAIPaths.stt}"
        headers = {
            **self.common_headers,
        }
        multiform_data = {
            "file": ("fixed.wav", audio, "audio/wav"),
        }
        try:
            response = requests.post(url, headers=headers, files=multiform_data)
            if response.status_code != 200:
                raise ValueError(
                    f"Response from Sarvam Failed with status code: {response.status_code} for {response.text}"
                )
            resp = response.json()

            return STT(text=resp["transcript"], lang_code=resp["language_code"])
        except Exception as e:
            logger.exception("Sarvam Response Error for tts")
            raise e
