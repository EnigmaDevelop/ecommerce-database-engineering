-- ============================================================================
-- SCENARIO 1: Unindexed Dynamic Attribute Search inside JSONB (Schema-on-Read)
-- Target: Deep filtering inside JSONB attributes without index constraints.
-- Objective: Force a heavy Sequential Scan on the products table.
-- ============================================================================

-- Business Case: Fetch all products with 'Red' color and 'XL' size specs.
-- Bottleneck: The 'attributes' field is JSONB and has NO index. 
-- Postgres must extract and parse the JSON string for every single row.

EXPLAIN ANALYZE
SELECT 
    product_id, 
    sku,
    name, 
    attributes->>'color' AS color, 
    attributes->>'size' AS size
FROM products
WHERE attributes->>'color' = 'Red' 
  AND attributes->>'size' = 'XL';


-- ============================================================================
-- SCENARIO 2: Heavy Join with Relational Tables + Non-Indexed Wildcard Search
-- Target: Joining large tables on unindexed text and enum-like fields.
-- Objective: Trigger a high-cost Hash Join and sequential wildcard scan.
-- ============================================================================

-- Business Case: Find users with hotmail accounts who cancelled orders with total amount > $5000.
-- Bottleneck: No B-Tree index on 'users.email' or 'orders.order_status'.
-- The leading wildcard '%hotmail.com' invalidates standard B-Tree indexing anyway, forcing a scan.

EXPLAIN ANALYZE
SELECT 
    u.user_id, 
    u.first_name, 
    u.email, 
    o.order_id, 
    o.total_amount, 
    o.order_status
FROM users u
JOIN orders o ON u.user_id = o.user_id
WHERE u.email LIKE '%hotmail.com'
  AND o.order_status = 'Cancelled'
  AND o.total_amount > 5000.00;


-- ============================================================================
-- SCENARIO 3: JSONB Array Containment Search & Sorting Without Index
-- Target: Searching nested JSONB arrays and sorting by unindexed column.
-- Objective: Maximize internal work memory (work_mem) boundaries, leading to Disk Sort.
-- ============================================================================

-- Business Case: Get top 100 most expensive Electronics with 'wireless' and 'noise-canceling' tags.
-- Bottleneck: Using the containment operator '@>' on JSONB array without a GIN index.
-- Ordering the unindexed 'base_price' column forces a high-cost External Merge Disk Sort.

EXPLAIN ANALYZE
SELECT 
    product_id, 
    name, 
    base_price,
    attributes->'tags' AS tags
FROM products
WHERE attributes->>'category_group' = 'Electronics'
  AND attributes->'tags' @> '["wireless", "noise-canceling"]'
ORDER BY base_price DESC
LIMIT 100;
