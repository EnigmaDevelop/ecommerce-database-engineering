import os
import json
import psycopg2
from psycopg2.extras import RealDictCursor

DB_HOST = "localhost"
DB_PORT = 5433  
DB_NAME = "ecommerce_db"
DB_USER = "data_engineer"       
DB_PASSWORD = "de_password123"   

QUERIES = {
    "Q1_JSONB_Key_Search": """
        EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)
        SELECT product_id, sku, name, attributes->>'color' AS color, attributes->>'size' AS size
        FROM products
        WHERE attributes->>'color' = 'Red' AND attributes->>'size' = 'XL';
    """,
            "Q2_Heavy_Join_Wildcard": """
        EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)
        SELECT u.user_id, u.first_name, u.email, o.order_id, o.total_amount, o.order_status
        FROM orders o
        JOIN users u ON u.user_id = o.user_id
        WHERE o.order_status = 'Cancelled' 
          AND o.total_amount > 5000.00
          AND u.email LIKE '%hotmail.com';
    """,
    "Q3_JSONB_Array_Containment": """
        EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)
        SELECT product_id, name, base_price, attributes->'tags' AS tags
        FROM products
        WHERE attributes @> '{"category_group": "Electronics", "tags": ["wireless", "noise-canceling"]}'
        ORDER BY base_price DESC LIMIT 100;
    """
}

def get_db_connection():
    return psycopg2.connect(host=DB_HOST, port=DB_PORT, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)

def extract_plan_metrics(plan_node):
    metrics = {
        "scan_methods": [],
        "join_methods": [],
        "sort_method": "N/A",
        "shared_hit_blocks": 0,
        "shared_read_blocks": 0
    }
    
    def walk_node(node):
        node_type = node.get("Node Type", "")
        if "Scan" in node_type:
            metrics["scan_methods"].append(node_type)
        if "Join" in node_type:
            metrics["join_methods"].append(node_type)
        if "Sort" in node_type and "Sort Method" in node:
            metrics["sort_method"] = node.get("Sort Method")
            
        metrics["shared_hit_blocks"] += node.get("Shared Hit Blocks", 0)
        metrics["shared_read_blocks"] += node.get("Shared Read Blocks", 0)
        
        for child in node.get("Plans", []):
            walk_node(child)
            
    walk_node(plan_node)
    return metrics

def run_benchmark(status_label):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    results = []

    print(f"📊 Running benchmarks for: {status_label}...")
    for query_name, query_sql in QUERIES.items():
        cursor.execute(query_sql)
        raw_plan = cursor.fetchone()
        
        # FIXED: Extracting the first element of the Postgres JSON array correctly
        plan_list = raw_plan['QUERY PLAN']
        plan_json = plan_list[0] if isinstance(plan_list, list) else plan_list
        
        plan_details = plan_json['Plan']
        execution_time = plan_json['Execution Time']
        
        metrics = extract_plan_metrics(plan_details)
        
        results.append({
            "Query": query_name,
            "Status": status_label,
            "Execution Time (ms)": round(execution_time, 3),
            "Primary Scan Strategy": ", ".join(set(metrics["scan_methods"])) if metrics["scan_methods"] else "N/A",
            "Join Strategy": ", ".join(set(metrics["join_methods"])) if metrics["join_methods"] else "N/A",
            "Sort Mechanism": metrics["sort_method"],
            "Cache Buffers (Hit/Read)": f"{metrics['shared_hit_blocks']} / {metrics['shared_read_blocks']}"
        })
        
    cursor.close()
    conn.close()
    return results

def generate_combined_markdown_table(before_data, after_data, output_filename):
    if not before_data or not after_data:
        return
        
    headers = ["Query", "Status", "Execution Time (ms)", "Primary Scan Strategy", "Join Strategy", "Sort Mechanism", "Cache Buffers (Hit/Read)"]
    
    lines = []
    lines.append("# 📈 Database Query Performance Engineering Report")
    lines.append(f"Statistically comprehensive benchmark comparing unindexed raw tables versus optimized fine-tuning structures.\n")
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join(["---" for _ in headers]) + " |")
    
    for b_row, a_row in zip(before_data, after_data):
        lines.append("| " + " | ".join([str(b_row[h]) for h in headers]) + " |")
        lines.append("| " + " | ".join([str(a_row[h]) for h in headers]) + " |")
        lines.append("| " + " | ".join(["" for _ in headers]) + " |") 
        
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))
    print(f"\n🚀 Ultimate performance report compiled successfully at: {output_filename}")

if __name__ == "__main__":
    import sys
    
    # 1. Capture execution arguments dynamically from terminal inputs
    # Expected options: "Before Optimization", "First Index Attempt", "Trigram Transformation", "Covered Final Fine-Tuning"
    execution_status = sys.argv[1] if len(sys.argv) > 1 else "Before Optimization"
    
    # 2. Run the dynamic real-time database benchmark loop against the live cluster
    live_results = run_benchmark(execution_status)
    
    # 3. Dynamic token mapping to create isolated checkpoint files on disk
    # This prevents newer experiments from overwriting previous telemetries
    sanitized_label = execution_status.lower().replace(" ", "_").replace("-", "_")
    report_filename = f"performance_report_{sanitized_label}.json"
    
    # 4. Serialize raw telemetry vectors safely onto its specific target file
    with open(report_filename, 'w', encoding='utf-8') as f:
        json.dump(live_results, f, indent=4)
        
    print(f"\n✅ Live benchmark telemetry securely locked into: {report_filename}")
    print(f"State Recorded: [{execution_status}]")
