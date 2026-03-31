from flask import Flask, jsonify, request
from flask_cors import CORS
from config import Config
from models import db, Message
from telegram_service import set_telegram_webhook, get_telegram_webhook_info
from classifier import MessageClassifier


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    db.init_app(app)

    classifier = None
    if app.config.get("OPENAI_API_KEY"):
        classifier = MessageClassifier(
            api_key=app.config["OPENAI_API_KEY"],
            model=app.config["OPENAI_MODEL"]
        )

    with app.app_context():
        db.create_all()

    @app.route("/")
    def home():
        return jsonify({
            "message": "Telegram AI Monitor backend is running"
        })

    @app.route("/messages", methods=["GET"])
    def get_messages():
        category = request.args.get("category")
        limit = request.args.get("limit", default=20, type=int)

        query = Message.query.order_by(Message.created_at.desc())

        if category and category.lower() != "all":
            query = query.filter(Message.category.ilike(category))

        messages = query.limit(limit).all()
        return jsonify([message.to_dict() for message in messages])

    @app.route("/messages", methods=["POST"])
    def create_message():
        data = request.get_json()

        if not data or not data.get("message_text"):
            return jsonify({"error": "message_text is required"}), 400

        category = data.get("category", "Normal")
        reason = data.get("reason")
        confidence = data.get("confidence")

        if classifier and not data.get("category"):
            try:
                result = classifier.classify(data["message_text"])
                category = result["category"]
                reason = result["reason"]
                confidence = result["confidence"]
            except Exception as e:
                category = "Normal"
                reason = f"Fallback classification: {str(e)}"
                confidence = 0.5

        message = Message(
            telegram_message_id=data.get("telegram_message_id"),
            chat_id=data.get("chat_id"),
            sender_name=data.get("sender_name"),
            message_text=data["message_text"],
            category=category,
            reason=reason,
            confidence=confidence,
        )

        db.session.add(message)
        db.session.commit()

        return jsonify(message.to_dict()), 201

    @app.route("/stats", methods=["GET"])
    def get_stats():
        messages = Message.query.all()

        stats = {
            "total": len(messages),
            "spam": 0,
            "important": 0,
            "question": 0,
            "normal": 0,
        }

        for message in messages:
            category = (message.category or "Normal").strip().lower()

            if category == "spam":
                stats["spam"] += 1
            elif category == "important":
                stats["important"] += 1
            elif category == "question":
                stats["question"] += 1
            else:
                stats["normal"] += 1

        return jsonify(stats)

    @app.route("/telegram/webhook", methods=["POST"])
    def telegram_webhook():
        update = request.get_json(silent=True)

        if not update:
            return jsonify({"error": "Invalid Telegram payload"}), 400

        message_data = update.get("message")

        if not message_data:
            return jsonify({
                "status": "ignored",
                "reason": "No message object in update"
            }), 200

        text = message_data.get("text")
        if not text:
            return jsonify({
                "status": "ignored",
                "reason": "Message has no text"
            }), 200

        telegram_message_id = str(message_data.get("message_id"))
        chat = message_data.get("chat", {})
        from_user = message_data.get("from", {})

        sender_name = (
            from_user.get("full_name")
            or " ".join(filter(None, [
                from_user.get("first_name"),
                from_user.get("last_name")
            ])).strip()
            or from_user.get("username")
            or "Unknown"
        )

        category = "Normal"
        reason = "Awaiting AI classification"
        confidence = 0.5

        if classifier:
            try:
                result = classifier.classify(text)
                category = result["category"]
                reason = result["reason"]
                confidence = result["confidence"]
            except Exception as e:
                category = "Normal"
                reason = f"Fallback classification: {str(e)}"
                confidence = 0.5

        new_message = Message(
            telegram_message_id=telegram_message_id,
            chat_id=str(chat.get("id")) if chat.get("id") is not None else None,
            sender_name=sender_name,
            message_text=text,
            category=category,
            reason=reason,
            confidence=confidence,
        )

        db.session.add(new_message)
        db.session.commit()

        return jsonify({
            "status": "saved",
            "message_id": new_message.id,
            "classification": {
                "category": category,
                "reason": reason,
                "confidence": confidence
            }
        }), 200

    @app.route("/telegram/set-webhook", methods=["POST"])
    def telegram_set_webhook():
        bot_token = app.config.get("TELEGRAM_BOT_TOKEN")
        base_url = app.config.get("WEBHOOK_BASE_URL")

        if not bot_token:
            return jsonify({"error": "TELEGRAM_BOT_TOKEN is not configured"}), 500

        if not base_url:
            return jsonify({"error": "WEBHOOK_BASE_URL is not configured"}), 500

        webhook_url = f"{base_url}/telegram/webhook"
        result = set_telegram_webhook(bot_token, webhook_url)

        return jsonify({
            "webhook_url": webhook_url,
            "telegram_response": result
        })

    @app.route("/telegram/webhook-info", methods=["GET"])
    def telegram_webhook_info():
        bot_token = app.config.get("TELEGRAM_BOT_TOKEN")

        if not bot_token:
            return jsonify({"error": "TELEGRAM_BOT_TOKEN is not configured"}), 500

        result = get_telegram_webhook_info(bot_token)
        return jsonify(result)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)