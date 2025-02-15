from fintechagent.agent import Sarvam
from fintechagent.audio import PlayAudio


def test_sarvam_text():
    sarvam = Sarvam.from_env()
    response = sarvam.answer(
        "The questions list is a JSON structure designed to extract specific details from a conversation. Each question includes an id, text, description, type, and properties. The type field defines the expected answer format (e.g., boolean, enum, short answer). The properties field is used for additional details like options in the case of enum type questions. Here's an example request with this structure:",
        "What does this paragraph say ?",
        "Give answer accordingly to context",
    )
    assert response.response != ""


def test_sarvam_tts():
    sarvam = Sarvam.from_env()
    tts = sarvam.tts(
        "The questions list is a JSON structure designed to extract specific details from a conversation"
    )
    assert tts.audio.startswith(b"RIFF")
    PlayAudio().play(tts.audio)


def test_sarvam_stt():
    sarvam = Sarvam.from_env()
    with open("sample.wav", "rb") as file:
        data = file.read()
    response = sarvam.stt(data)
    assert response.text.startswith("This will return")
