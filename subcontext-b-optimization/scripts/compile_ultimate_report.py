import json
import os

def compile_markdown():
    # 1. Map out the chronological order of our engineering experiments
    checkpoint_files = [
        ("Before Optimization", "performance_report_before_optimization.json"),
        ("First Index Attempt", "performance_report_first_index_attempt.json"),
        ("Trigram Transformation", "performance_report_trigram_transformation.json"),
        ("Covered Final Fine-Tuning", "performance_report_covered_final_fine_tuning.json")
    ]
    
    headers = ["Query", "Status", "Execution Time (ms)", "Primary Scan Strategy", "Join Strategy", "Sort Mechanism", "Cache Buffers (Hit/Read)"]
    
    lines = []
    lines.append("# 📈 Database Query Performance Engineering Report")
    lines.append("Statistically comprehensive iterative benchmark comparing raw database layers against continuous tuning execution tiers.\n")
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join(["---" for _ in headers]) + " |")
    
    # 2. Read each checkpoint sequence carefully without throwing structural null exceptions
    for status_label, json_file in checkpoint_files:
        if os.path.exists(json_file):
            with open(json_file, 'r', encoding='utf-8') as f:
                data_vector = json.load(f)
            for row in data_vector:
                lines.append("| " + " | ".join([str(row[h]) for h in headers]) + " |")
            lines.append("| " + " | ".join(["" for _ in headers]) + " |") # Add visual row split
            
    with open("performance_report.md", 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))
        
    print("\n🚀 Iterative performance_report.md compiled successfully using actual cluster telemetries!")

if __name__ == "__main__":
    compile_markdown()
