# 📈 Database Query Performance Engineering Report
Statistically comprehensive iterative benchmark comparing raw database layers against continuous tuning execution tiers.

| Query | Status | Execution Time (ms) | Primary Scan Strategy | Join Strategy | Sort Mechanism | Cache Buffers (Hit/Read) |
| --- | --- | --- | --- | --- | --- | --- |
| Q1_JSONB_Key_Search | Before Optimization | 10.14 | Seq Scan | N/A | N/A | 1672 / 0 |
| Q2_Heavy_Join_Wildcard | Before Optimization | 266.772 | Seq Scan | Hash Join | N/A | 16574 / 73858 |
| Q3_JSONB_Array_Containment | Before Optimization | 12.404 | Seq Scan | N/A | top-N heapsort | 5022 / 0 |
|  |  |  |  |  |  |  |
| Q1_JSONB_Key_Search | First Index Attempt | 3.088 | Bitmap Index Scan, Bitmap Heap Scan | N/A | N/A | 1173 / 8 |
| Q2_Heavy_Join_Wildcard | First Index Attempt | 412.678 | Seq Scan | Hash Join | N/A | 32813 / 102171 |
| Q3_JSONB_Array_Containment | First Index Attempt | 5.262 | Bitmap Index Scan, Bitmap Heap Scan | N/A | top-N heapsort | 4793 / 0 |
|  |  |  |  |  |  |  |
| Q1_JSONB_Key_Search | Trigram Transformation | 3.212 | Bitmap Index Scan, Bitmap Heap Scan | N/A | N/A | 1181 / 0 |
| Q2_Heavy_Join_Wildcard | Trigram Transformation | 243.478 | Bitmap Heap Scan, Bitmap Index Scan, Seq Scan | Hash Join | N/A | 23213 / 67922 |
| Q3_JSONB_Array_Containment | Trigram Transformation | 5.157 | Bitmap Index Scan, Bitmap Heap Scan | N/A | top-N heapsort | 4793 / 0 |
|  |  |  |  |  |  |  |
| Q1_JSONB_Key_Search | Covered Final Fine Tuning | 2.527 | Bitmap Heap Scan, Bitmap Index Scan | N/A | N/A | 1181 / 0 |
| Q2_Heavy_Join_Wildcard | Covered Final Fine Tuning | 82.543 | Bitmap Heap Scan, Bitmap Index Scan, Index Only Scan | Hash Join | N/A | 138023 / 2280 |
| Q3_JSONB_Array_Containment | Covered Final Fine Tuning | 5.217 | Bitmap Heap Scan, Bitmap Index Scan | N/A | top-N heapsort | 4793 / 0 |
|  |  |  |  |  |  |  |