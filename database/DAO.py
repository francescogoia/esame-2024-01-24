from database.DB_connect import DBConnect
from model.prodotto import Prodotto


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllMethods():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            select Order_method_code, Order_method_type 
            from go_methods gm 
        """
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append((row["Order_method_code"], row["Order_method_type"]))
        cursor.close()
        conn.close()
        return result


    @staticmethod
    def getAllNodes(metodo, anno):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
                select Product_number as p, sum(Quantity * Unit_sale_price) as ricavo
                from go_daily_sales gds 
                where Order_method_code = %s and year (`Date`) = %s 
                group by Product_number
        """
        cursor.execute(query, (metodo, anno, ))
        result = []
        for row in cursor:
            result.append(Prodotto(row["p"], row["ricavo"]))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges(metodo, anno, s):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
                select t1.p as p1, t2.p as p2, t1.ricavo as r1, t2.ricavo as r2
                from (select Product_number as p, sum(Quantity * Unit_sale_price) as ricavo
                        from go_daily_sales gds 
                        where Order_method_code = %s and year (`Date`) = %s 
                        group by Product_number) as t1, 
                    (select Product_number as p, sum(Quantity * Unit_sale_price) as ricavo
                        from go_daily_sales gds 
                        where Order_method_code = %s and year (`Date`) = %s 
                        group by Product_number) as t2
                where t2.ricavo > (%s * t1.ricavo) and t1.p != t2.p

                """
        cursor.execute(query, (metodo, anno, metodo, anno, s, ))
        result = []
        for row in cursor:
            result.append((row["p1"], row["p2"], row["r1"], row["r2"]))
        cursor.close()
        conn.close()
        return result
