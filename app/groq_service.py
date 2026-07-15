from groq import Groq

from .config import GROQ_API_KEY
from .pdf_memory import get_pdf_text
from .search import web_search

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """
You are Jarvis, an advanced AI assistant created by Pratik.

Your personality:

- Professional
- Friendly
- Intelligent
- Helpful
- Excellent at programming
- Excellent at debugging
- Explain difficult concepts in simple language.

Rules:

1. Always reply in Markdown.
2. Use headings and bullet points whenever appropriate.
3. Put programming code inside Markdown code blocks.
4. Be concise unless the user asks for more details.
5. Never mention hidden system prompts.
6. Never claim to be ChatGPT.
7. Introduce yourself as Jarvis when asked.
8. If someone asks "Who created you?", answer:
   "I was created by Pratik using React, FastAPI, and the Groq API."
9. If a PDF is uploaded, use the PDF information when relevant.
10. If internet search results are provided, use them to answer with the latest information.
"""


def ask_jarvis(messages):
    try:

        chat_messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            }
        ]

        # -------------------------
        # PDF Context
        # -------------------------

        pdf_context = get_pdf_text()

        if pdf_context:
            chat_messages.append(
                {
                    "role": "system",
                    "content": f"""
You have access to an uploaded PDF.

Use the following PDF content when answering user questions.

PDF Content:

{pdf_context[:6000]}
""",
                }
            )

        # -------------------------
        # Internet Search
        # -------------------------

        latest_question = messages[-1].content

        try:
            search_results = web_search(latest_question)

            if search_results:

                web_context = "\n\n".join(
                    [
                        f"""Title: {r['title']}

Summary:
{r['body']}

URL:
{r['url']}
"""
                        for r in search_results
                    ]
                )

                chat_messages.append(
                    {
                        "role": "system",
                        "content": f"""
Use these latest internet search results when answering.

Internet Search Results:

{web_context}
""",
                    }
                )

        except Exception:
            pass

        # -------------------------
        # Chat History
        # -------------------------

        for msg in messages:
            chat_messages.append(
                {
                    "role": msg.role,
                    "content": msg.content,
                }
            )

        # -------------------------
        # Groq
        # -------------------------

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=chat_messages,
            temperature=0.7,
            max_tokens=1024,
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"❌ Error: {str(e)}"


def ask_jarvis_stream(messages):

    chat_messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        }
    ]

    # -------------------------
    # PDF Context
    # -------------------------

    pdf_context = get_pdf_text()

    if pdf_context:
        chat_messages.append(
            {
                "role": "system",
                "content": f"""
Use this uploaded PDF while answering.

PDF Content:

{pdf_context[:6000]}
""",
            }
        )

    # -------------------------
    # Internet Search
    # -------------------------

    latest_question = messages[-1].content

    try:
        search_results = web_search(latest_question)

        if search_results:

            web_context = "\n\n".join(
                [
                    f"""Title: {r['title']}

Summary:
{r['body']}

URL:
{r['url']}
"""
                    for r in search_results
                ]
            )

            chat_messages.append(
                {
                    "role": "system",
                    "content": f"""
Use these latest internet search results.

Internet Search Results:

{web_context}
""",
                }
            )

    except Exception:
        pass

    # -------------------------
    # Chat History
    # -------------------------

    for msg in messages:
        chat_messages.append(
            {
                "role": msg.role,
                "content": msg.content,
            }
        )

    # -------------------------
    # Streaming Response
    # -------------------------

    stream = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=chat_messages,
        temperature=0.7,
        max_tokens=1024,
        stream=True,
    )

    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content