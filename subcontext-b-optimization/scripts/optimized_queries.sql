-- ============================================================================
-- OPTIMIZATION 1: Expression B-Tree Index for JSONB Keys
-- Target: Accelerating Scenario 1 (Unindexed Dynamic Attribute Search)
-- Strategy: Instead of indexing the whole JSON, we index specific extracted keys.
-- ============================================================================

-- Step 1: Create a specialized Expression Index targeting the nested JSONB keys
CREATE INDEX idx_products_attributes_color_size 
ON products ((attributes->>'color'), (attributes->>'size'));

-- Step 2: Validate the optimization (Should switch from Seq Scan to Index Scan)
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
-- OPTIMIZATION 2: Composite & Partial B-Tree Indexing
-- Target: Accelerating Scenario 2 (Heavy Join + Wildcard Search)
-- Strategy: Standard B-Tree cannot do leading wildcard (%hotmail), but we can 
-- optimize the join engine using a Partial Index on orders and B-Tree on users.
-- ============================================================================

-- Step 1: Index users email for exact or trailing matches
CREATE INDEX idx_users_email ON users (email);

-- Step 2: Create a Partial Composite Index on orders (Only index active performance targets)
CREATE INDEX idx_orders_partial_cancelled 
ON orders (user_id, total_amount) 
WHERE order_status = 'Cancelled';

-- Step 3: Validate the optimization (Should transform Hash Join into high-speed Index Scan)
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
-- OPTIMIZATION 3: GIN (Generalized Inverted Index) for JSONB Document Search
-- Target: Accelerating Scenario 3 (JSONB Array Containment & Category Filter)
-- Strategy: GIN index acts like a search engine index, mapping all nested keys/arrays.
-- ============================================================================

-- Step 1: Create a specialized GIN index using jsonb_path_ops for hyper-fast containment matching
CREATE INDEX idx_products_attributes_gin 
ON products USING gin (attributes jsonb_path_ops);

-- Step 2: Create a regular B-Tree on base_price to bypass the Disk/Memory Sort operation
CREATE INDEX idx_products_base_price ON products (base_price DESC);

-- Step 3: Validate the optimization (Should perform Bitmap Index Scan instantly)
EXPLAIN ANALYZE
SELECT 
    product_id, 
    name, 
    base_price,
    attributes->'tags' AS tags
FROM products
WHERE attributes->>'category_group' = 'Electronics'
  AND attributes->'tags' @> '["wireless", "noise-canceling"]'
-- Postgres query planner will now combine the GIN index filter and B-Tree sorting
ORDER BY base_price DESC
LIMIT 100;
