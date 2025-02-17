# HydPyHack 2025
## BulBul your fintech Agent
- Generates personalized sales pitch for targeted customer and picks potential creditcard that matches to the interests of the customer.
- Users can have a free flowing audio conversation with bulbul in knowing and understanding more about the product.
- Users have control to end the conversation by voicing out `stop`.

# Development Setup:
- Uses Sarvam AI platform for Text Generation, Text to Speech, Speech to Text
- Install uv and run `uv pip install`.
- Run DB migrations `yoyo apply`.
- Copy `env.example` to `.env` and modify SARVAM_AI_API value.
- Run `export $(cat .env | xargs)`
- Run `.venv/bin/python main.py` to start the agent.

# Hackathon Slides
- Found at [HydPy Hackathon.pdf](./HydPy%20Hackathon.pdf)
