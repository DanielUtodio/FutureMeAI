from flask import Flask, jsonify, request, render_template
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from uuid import uuid4
load_dotenv()
app = Flask(__name__)

conversations = {}


llm = ChatGoogleGenerativeAI(
    model = "gemini-3.6-flash",
    temperature = 0.7
)


@app.route("/")
def home(): 
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("/dashboard/dash.html")

@app.route("/api/future-chat", methods=["POST"])
def future_chat():
    data = request.get_json()
    message = data.get("message").strip()
    chat_id = data.get("chat_id")

    if not message:
        return jsonify({"error": "Message cannot be empty"}), 400

    if not chat_id or chat_id not in conversations:
        chat_id = str(uuid4())
        conversations[chat_id] = []



    try: 
        messages = [
                SystemMessage(
                    content="""
                    You are FutureMe AI, a friendly and thoughtful career guide
                    for students.

                    Help students:
                    - Explore careers that match their interests.
                    - Discover skills they can learn.
                    - Find beginner-friendly projects.
                    - Understand different career paths.

                    RESPONSE STYLE:
                    - Use simple, natural, conversational English.
                    - Be warm, encouraging, and practical.
                    - Keep answers clear and easy to read.
                    - Avoid long, overwhelming explanations.
                    - Use short paragraphs.
                    - Use headings when they improve readability.
                    - Use bullet points for lists.
                    - Use bold text to highlight important terms.
                    - Avoid unnecessary technical jargon.
                    - Don't repeat the user's question unnecessarily.

                    When suggesting careers, explain:
                    1. What the career involves.
                    2. Why it might suit the student's interests.
                    3. Skills they can start learning.
                    4. A simple project they can try.

                    Make every response feel like helpful guidance from a
                    knowledgeable person, not a textbook.
                    """
                    )
        ]

        for chat in conversations[chat_id]:
            messages.append(HumanMessage(content=chat["user"]))
            messages.append(SystemMessage(content=chat["assistant"]))

        
        messages.append(HumanMessage(content=message))
        response = llm.invoke(messages)
        reply = response.content

        if isinstance(reply, list):
            reply = "\n".join(
                block.get("text", "")
                for block in reply
                if isinstance(block, dict)
            )

        conversations[chat_id].append({
            "user": message,
            "assistant": reply
        })

        return jsonify({
            "chat_id": chat_id,
            "reply": reply
        }), 200

        
    except Exception as e:
        print("Gemini error:", e)

        return jsonify({
            "error": "Something went wrong while getting a response."
        }), 500 
    

@app.route("/api/new-chat", methods=["POST"])
def new_chat():
    chat_id = str(uuid4())
    conversations[chat_id] = []

    return jsonify({
        "chat_id": chat_id,
        "message": "New chat started"
    })


if __name__ == "__main__":
    app.run(debug=True, port=7000)
