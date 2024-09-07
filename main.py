import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from agent import EnhancedResearchAgent

load_dotenv()

app = Flask(__name__)
agent = EnhancedResearchAgent(memory_size=10)  # Increased memory size for API use

@app.route('/', methods=['GET'])
def home():
    return "LLM Agent is running!"

@app.route('/research', methods=['POST'])
def research():
    data = request.json
    query = data.get('query')
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    result = agent.research(query)
    if result.startswith("An error occurred"):
        return jsonify({"error": result}), 500
    return jsonify({"result": result})

@app.route('/memory', methods=['GET'])
def get_memory():
    return jsonify({"memory": agent.memory.get_context()})

@app.route('/memory/clear', methods=['POST'])
def clear_memory():
    agent.memory.clear()
    return jsonify({"message": "Memory cleared"})

@app.route('/memory/status', methods=['GET'])
def memory_status():
    return jsonify({"status": str(agent.memory)})

@app.route('/memory/last/<int:n>', methods=['GET'])
def get_last_n(n):
    return jsonify({"last_n": agent.get_last_n_interactions(n)})

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)