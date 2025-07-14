# judgeval_integration/tracer.py

from judgeval.tracer import Tracer, wrap
from openai import OpenAI
from config import OPENAI_API_KEY

# Automatically wrap OpenAI client to capture LLM calls
client = wrap(OpenAI(api_key=OPENAI_API_KEY))

# Create a Tracer for your project
judgment = Tracer(project_name="email-scheduling-agent")