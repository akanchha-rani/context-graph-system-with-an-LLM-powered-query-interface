from flask import Flask, render_template, request, jsonify
import os
import json
from dotenv import load_dotenv
from groq import Groq
from fde_graph import build_graph, save_graph_html

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

app = Flask(__name__)

G = build_graph()
save_graph_html(G)

def get_orders_by_customer(customer_id):
    return [
        v for u, v, k in G.edges(keys=True)
        if u == customer_id and G[u][v][k]['title'] == 'PLACED_ORDER'
    ]

def get_customer_orders_count(customer_id):
    return len(get_orders_by_customer(customer_id))

def interpret_query(query):
    prompt = f"""
    You MUST return ONLY valid JSON.
    Do NOT include any explanation.

    Available functions:
    - get_orders_by_customer(customer_id)
    - get_customer_orders_count(customer_id)

    Query: {query}

    Format:
    {{
        "function": "...",
        "customer_id": "..."
    }}
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

def parse_llm_response(response_text):
    try:
        start = response_text.find("{")
        end = response_text.rfind("}") + 1
        clean_json = response_text[start:end]
        return json.loads(clean_json)
    except Exception as e:
        print("Parsing Error:", e)
        return None


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    user_query = request.json.get("query")

    try:
        
        response_text = interpret_query(user_query)
        intent = parse_llm_response(response_text)

        if not intent:
            return jsonify({
                "response": "⚠️ Could not understand query. Try again.",
                "reload_graph": False
            })

        func = intent.get("function")
        cid = intent.get("customer_id")

        highlight_nodes = []


        if func == "get_orders_by_customer" and cid:
            result = get_orders_by_customer(cid)
            highlight_nodes = [cid] + result

        elif func == "get_customer_orders_count" and cid:
            result = get_customer_orders_count(cid)
            highlight_nodes = [cid]

        else:
            result = " Unknown query"

        save_graph_html(G, highlight_nodes)

        return jsonify({
            "response": str(result),
            "reload_graph": True
        })

    except Exception as e:
        return jsonify({
            "response": f"Error: {str(e)}",
            "reload_graph": False
        })


if __name__ == "__main__":
    app.run(debug=True, port=5050)