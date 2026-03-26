# =========================
# fde_graph.py
# =========================

import os
import json
import zipfile
import networkx as nx
from pyvis.network import Network

# =========================
# 1. Extract & Locate Dataset
# =========================

def load_data():
    zip_path = "sap-order-to-cash-dataset.zip"
    extract_path = "sap_data"

    if not os.path.exists(extract_path):
        os.makedirs(extract_path)

    # extract only once
    if not os.listdir(extract_path):
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)

    folders = [
        f for f in os.listdir(extract_path)
        if os.path.isdir(os.path.join(extract_path, f)) and not f.startswith('.')
    ]

    return os.path.join(extract_path, folders[0])


# =========================
# 2. Load JSON / JSONL Files
# =========================

def load_sap_data(data_path, folder_name):
    folder_path = os.path.join(data_path, folder_name)
    data = []

    if not os.path.exists(folder_path):
        print(f"❌ Missing folder: {folder_name}")
        return data

    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)

        try:
            # JSONL
            if file.endswith(".jsonl"):
                with open(file_path, "r") as f:
                    for line in f:
                        data.append(json.loads(line))

            # JSON
            else:
                with open(file_path, "r") as f:
                    content = json.load(f)

                    if isinstance(content, list):
                        data.extend(content)
                    else:
                        data.append(content)

        except Exception as e:
            print(f"⚠️ Skipping {file}: {e}")

    return data


# =========================
# 3. Build Graph
# =========================

def build_graph():

    data_path = load_data()

    sales_orders = load_sap_data(data_path, "sales_order_headers")
    deliveries = load_sap_data(data_path, "outbound_delivery_headers")
    billing = load_sap_data(data_path, "billing_document_headers")

    G = nx.MultiDiGraph()

    # -------------------------
    # Customer → Order
    # -------------------------
    for order in sales_orders:
        oid = order.get('salesOrder')
        cust = order.get('soldToParty')

        if oid and cust:
            G.add_node(
                oid,
                label=f"Order {oid}",
                type='Order',
                color='#3498db'
            )

            G.add_node(
                cust,
                label=f"Customer {cust}",
                type='Customer',
                color="#f1d30f"
            )

            G.add_edge(
                cust,
                oid,
                title='PLACED_ORDER',
                label='PLACED_ORDER'
            )

    # -------------------------
    # Delivery Nodes
    # -------------------------
    for dlv in deliveries:
        did = dlv.get('deliveryDocument')

        if did:
            G.add_node(
                did,
                label=f"Delivery {did}",
                type='Delivery',
                color="#35e37d"
            )

    # -------------------------
    # Billing Nodes
    # -------------------------
    for bill in billing:
        bid = bill.get('billingDocument')

        if bid:
            G.add_node(
                bid,
                label=f"Invoice {bid}",
                type='Billing',
                color="#fc7848"
            )

    print(f"✅ Graph Built! Nodes: {G.number_of_nodes()}, Edges: {G.number_of_edges()}")

    return G


# =========================
# 4. Save Graph with Highlighting
# =========================

def save_graph_html(G, highlight_nodes=None):

    net = Network(
    height='100vh',   # 🔥 change this
    width='100%',
    directed=True,
    bgcolor="#EDEDED",
    font_color='gray'
)

    highlight_nodes = highlight_nodes or []

    # -------------------------
    # Add Nodes
    # -------------------------
    for node, data in G.nodes(data=True):

        default_color = data.get("color", "#97c2fc")

        if node in highlight_nodes:
            net.add_node(
                node,
                label=data.get("label", str(node)),
                color="#bc5090",          
                size=35
            )
        else:
            net.add_node(
                node,
                label=data.get("label", str(node)),
                color=default_color,
                size=20
            )

    # -------------------------
    # Add Edges
    # -------------------------
    for u, v, data in G.edges(data=True):
        net.add_edge(
            u,
            v,
            label=data.get("title", "")
        )

    # -------------------------
    # Save HTML
    # -------------------------
    if not os.path.exists("static"):
        os.makedirs("static")

    net.write_html("static/sap_graph.html")