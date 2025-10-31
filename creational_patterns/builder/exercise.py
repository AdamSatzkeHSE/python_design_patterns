# Write a Query-Builder to build simple SELECT statements in SQL
#   qb.table("users").select("id","name").where("active=1").order("id DESC").build()
# -> "SELECT id,name FROM users WHERE active=1 ORDER BY id DESC;"

class QueryBuilder:
    pass

# --- Try it ---
if __name__ == "__main__":
    qb = QueryBuilder()
    print(qb.table("users").select("id","name").where("active=1").order("id DESC").build())