# main.py

import os
import logging
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from agent import EnhancedResearchAgent, get_anthropic_version

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Initialize EnhancedResearchAgent
try:
    agent = EnhancedResearchAgent(memory_size=10)  # Increased memory size for API use
    logger.info(f"EnhancedResearchAgent initialized successfully. Anthropic library version: {get_anthropic_version()}")
except Exception as e:
    logger.error(f"Failed to initialize EnhancedResearchAgent: {str(e)}")
    agent = None

@app.route('/', methods=['GET'])
def home():
    return "LLM Agent is running!"

@app.route('/research', methods=['POST'])
def research():
    if agent is None:
        return jsonify({"error": "EnhancedResearchAgent is not initialized"}), 500

    data = request.json
    query = data.get('query')
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    try:
        result = agent.research(query)
        return jsonify({"result": result})
    except Exception as e:
        logger.error(f"An error occurred during research: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/memory', methods=['GET'])
def get_memory():
    if agent is None:
        return jsonify({"error": "EnhancedResearchAgent is not initialized"}), 500
    return jsonify({"memory": agent.memory.get_context()})

@app.route('/memory/clear', methods=['POST'])
def clear_memory():
    if agent is None:
        return jsonify({"error": "EnhancedResearchAgent is not initialized"}), 500
    agent.memory.clear()
    return jsonify({"message": "Memory cleared"})

@app.route('/memory/status', methods=['GET'])
def memory_status():
    if agent is None:
        return jsonify({"error": "EnhancedResearchAgent is not initialized"}), 500
    return jsonify({"status": agent.memory.status()})

@app.route('/memory/last/<int:n>', methods=['GET'])
def get_last_n(n):
    if agent is None:
        return jsonify({"error": "EnhancedResearchAgent is not initialized"}), 500
    try:
        return jsonify({"last_n": agent.get_last_n_interactions(n)})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/version', methods=['GET'])
def get_version():
    return jsonify({
        "anthropic_version": get_anthropic_version(),
        "agent_model": agent.model if agent else "N/A"
    })

@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"Unhandled exception: {str(e)}")
    return jsonify({"error": "An unexpected error occurred"}), 500

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)