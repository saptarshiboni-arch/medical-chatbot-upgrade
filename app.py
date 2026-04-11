from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from medibot import get_response

app = Flask(__name__)
CORS(app, resources={r"/chat": {"origins": "*"}})

# ✅ Store chat history
chat_history = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    import traceback
    
    try:
        data = request.get_json(force=True)
        print("Incoming data:", data)

        user_msg = data.get("message", "")
        print("User message:", user_msg)

        reply = get_response(user_msg)
        print("Reply:", reply)

        # ✅ Save to history
        chat_history.append({
            "user": user_msg,
            "bot": str(reply)
        })

        return jsonify({"response": str(reply)})

    except Exception as e:
        error = traceback.format_exc()
        print("ERROR OCCURRED:\n", error)

        return jsonify({
            "response": "Backend Error:\n" + error
        })

# ✅ NEW ROUTE for history page
@app.route("/history")
def history():
    return render_template("history.html", chats=chat_history)

@app.route("/clear_history")
def clear_history():
    global chat_history
    chat_history = []
    return "History cleared! <a href='/history'>Go back</a>"

if __name__ == "__main__":
    app.run(debug=False)