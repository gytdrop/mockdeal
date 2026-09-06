import xmlrpc.client

url = "http://localhost:8069"
db = "vantage_db"
username = "admin"
password = "admin"

common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

print("=== 1. EXECUTING TURNKEY DEMO DATA PROVISIONING ===")
res_seed = models.execute_kw(db, uid, password, "vantage.sales.dashboard", "action_load_turnkey_seed_data", [[1]])
print("Turnkey Seed Load Status:", res_seed.get("params", {}).get("title"))

print("\n=== 2. VERIFYING BLENDED RISK SCORE ENGINE ===")
partner = models.execute_kw(db, uid, password, "res.partner", "search_read", [[['name', '=', 'Acme Corp (Bronze Tier)']]], {'fields': ["id", "name", "customer_tier_id"]})
product = models.execute_kw(db, uid, password, "product.product", "search_read", [[['name', '=', 'DealFlow Enterprise Server']]], {'fields': ["id", "name", "list_price"]})

partner_id = partner[0]["id"] if partner else 1
product_id = product[0]["id"] if product else 1

order_id = models.execute_kw(db, uid, password, "sale.order", "create", [{
    "partner_id": partner_id,
    "order_line": [(0, 0, {
        "product_id": product_id,
        "product_uom_qty": 5,
        "price_unit": 2500.0,
        "discount": 40.0
    })]
}])

order = models.execute_kw(db, uid, password, "sale.order", "read", [[order_id]], {'fields': ["name", "blended_risk_score", "risk_approval_state", "tier_discount_ceiling", "manager_risk_ceiling"]})
print("Created Quotation Risk Assessment:", order[0])

print("\n=== 3. VERIFYING AUTO-SPLIT WAREHOUSE ALLOCATION ENGINE ===")
warehouses = models.execute_kw(db, uid, password, "stock.warehouse", "search_read", [[]], {'fields': ["id", "name", "code", "base_shipping_cost", "shipping_cost_weight"]})
for w in warehouses:
    print("Warehouse:", w["name"], "| Code:", w["code"], "| Base Freight: $", w.get("base_shipping_cost"), "| Weight:", w.get("shipping_cost_weight"))

order_lines = models.execute_kw(db, uid, password, "sale.order", "read", [[order_id]], {'fields': ["order_line"]})[0]["order_line"]
line_id = order_lines[0]
models.execute_kw(db, uid, password, "sale.order.line", "write", [[line_id], {"product_uom_qty": 100}])

split_res = models.execute_kw(db, uid, password, "sale.order", "action_split_fulfillments", [[order_id]])
print("Auto-Split Action Response:", split_res.get("params", {}).get("title") if isinstance(split_res, dict) else split_res)

order_after_split = models.execute_kw(db, uid, password, "sale.order", "read", [[order_id]], {'fields': ["name", "estimated_shipment_count", "estimated_shipping_cost", "fulfillment_shortfall_qty", "has_split_children"]})
print("Fulfillment Metrics After Auto-Split:", order_after_split[0])
