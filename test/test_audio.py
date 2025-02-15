from fintechagent.audio import PlayAudio


def test_record():
    pa = PlayAudio()
    recorded_audio = pa.record()
    assert recorded_audio.startswith(b"RIFF")
