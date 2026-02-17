from dotenv import load_dotenv
from openai import OpenAI
import discord
import os
import textwrap

# Load environment variables from .env file (or Codespaces env vars)
load_dotenv()

# Prefer standard env var names used in most examples / Codespaces labs
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_KEY")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN") or os.getenv("TOKEN")

if not DISCORD_TOKEN:
    raise RuntimeError("Missing DISCORD_TOKEN (or TOKEN). Add it to env/.env or Codespaces Secrets.")
if not OPENAI_API_KEY:
    raise RuntimeError("Missing OPENAI_API_KEY (or OPENAI_KEY). Add it to env/.env or Codespaces Secrets.")

# Initialize the OpenAI client
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Scrum Master persona
SYSTEM_STYLE = """You are ScrumMaster, a professional Agile/Scrum coach.

Your job: answer questions clearly and confidently using Agile/Scrum vernacular.
Tone: professional, calm, concise, supportive.

When helpful, structure responses as:
- Quick answer
- Scrum perspective (roles/events/artifacts)
- Next steps (actionable)
- Risks/anti-patterns

Avoid fluff. Explain terms briefly if the user seems new."""

def chunk_for_discord(text: str, limit: int = 1900):
    """Discord message limit is 2000; keep buffer for safety."""
    chunks = []
    for paragraph in (text or "").split("\n"):
        if not chunks:
            chunks.append(paragraph)
        elif len(chunks[-1]) + 1 + len(paragraph) <= limit:
            chunks[-1] += "\n" + paragraph
        else:
            chunks.append(paragraph)

    final = []
    for c in chunks:
        if len(c) <= limit:
            final.append(c)
        else:
            final.extend(textwrap.wrap(c, width=limit))
    return [c for c in final if c.strip()]

def call_openai(question: str) -> str:
    question = (question or "").strip()
    if not question:
        return "Please provide a question after `$question`."

    try:
        completion = openai_client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": SYSTEM_STYLE},
                {"role": "user", "content": question},
            ],
            temperature=0.4,
            max_tokens=500,
        )

        response = (completion.choices[0].message.content or "").strip()
        return response or "I couldn't generate a response. Could you rephrase your question?"

    except Exception as e:
        msg = str(e)
        if "insufficient_quota" in msg or "Error code: 429" in msg:
            return (
                "⚠️ OpenAI API error (429): **insufficient_quota**.\n"
                "Your API key has no available credits or billing is not enabled.\n"
                "Fix: enable billing / add credits / increase monthly limit, then update `OPENAI_API_KEY` "
                "in Codespaces Secrets and restart the Codespace."
            )
        return f"⚠️ OpenAI error: {type(e).__name__}. Please try again."

# Set up Discord
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello! 👋 I\'m ScrumMasterBot. Try: `$question How do we reduce sprint spillover?`')
        return

    if message.content.startswith('$question'):
        question = message.content.split("$question", 1)[1].strip()
        response = call_openai(question)

        for chunk in chunk_for_discord(response):
            await message.channel.send(chunk)

client.run(DISCORD_TOKEN)