from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/api/v2/webhook/fetch', methods=['POST'])
def fetch_webhook():
    # Feature to fetch payload previews from registered webhooks
    data = request.json
    target_url = data.get('url')
    
    if not target_url:
        return jsonify({"error": "Missing URL parameter"}), 400
        
    try:
        # VULNERABILITY: No sanitization of target_url. SSRF possible.
        # Developer note: Need to restrict this to external domains only later.
        response = requests.get(target_url, timeout=5)
        return jsonify({"preview": response.text[:2000]}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
