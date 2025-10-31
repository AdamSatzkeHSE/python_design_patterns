class QueryBuilder:
    def __init__(self):
        self._table = None
        self._cols = ["*"]
        self._where = None
        self._order = None

    def table(self, name):
        self._table = name
        return self
    
    def select(self, *cols):
        if cols:
            self._cols = list(cols)
            return self
    
    def where(self, clause):
        self._where = clause
        return self
    
    def order(self, clause):
        self._order = clause
        return self
    
    def build(self):
        assert self._table, "table required"
        sql = f"SELECT {','.join(self._cols)} FROM {self._table}"
        if self._where:
            sql += f" WHERE {self._where}"
        if self._order:
            sql += f" ORDER BY {self._order}"
        return sql + ";"
    
if __name__ == "__main__":
    qb = QueryBuilder()
    print(qb.table("users").select("id", "name").where("active=1").order("id DESC").build())
