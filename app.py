from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from medibot import get_response
import traceback
import os

print("App file started")

app = Flask(__name__)
# Updated CORS to be more flexible for the live environment
CORS(app)

# Store chat history
chat_history = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        # force=True ensures it tries to parse JSON even if content-type header is missing
        data = request.get_json(force=True)
        print("Incoming Data:", data)

        user_msg = data.get("message", "")
        
        if not user_msg:
            return jsonify({"response": "I didn't receive a message. Please try again."})

        # Calling your medibot logic
        reply = get_response(user_msg)
        print("RAW REPLY FROM MEDIBOT:", reply)

        if not reply:
            reply = "The assistant is currently unavailable. Please try again later."

        # Add to history (optional logic improvement)
        chat_history.append({"user": user_msg, "bot": reply})

        return jsonify({
            "response": str(reply)
        })

    except Exception as e:
        error_details = traceback.format_exc()
        print("CRITICAL ERROR IN /CHAT ROUTE:")
        print(error_details)

        return jsonify({
            "response": "Sorry, the server encountered an error.",
            "debug_info": str(e) # This helps you see the error in the UI
        })

@app.route("/history")
def history():
    return render_template("history.html", chats=chat_history)

@app.route("/clear_history")
def clear_history():
    global chat_history
    chat_history = []
    return "History cleared! <a href='/history'>Go back</a>"

# --- UPDATED FOR RENDER ---
if __name__ == "__main__":
    # Render uses the $PORT environment variable. If it doesn't exist, we use 10000.
    port = int(os.environ.get("PORT", 10000))
    print(f"Starting Flask app on port {port}...")
    app.run(host="0.0.0.0", port=port)