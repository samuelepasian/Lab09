from database.DB_connect import DBConnect
from model.airport import Airport

class DAO():
    def __init__(self):
        pass

    @staticmethod
    def get_allAirports():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """SELECT * from airports"""
        cursor.execute(query)
        result=[]
        for row in cursor:
            result.append(Airport(row["ID"],
                                    row["IATA_CODE"],
                                    row["AIRPORT"],
                                    row["CITY"],
                                    row["STATE"],
                                    row["COUNTRY"],
                                    row["LATITUDE"],
                                    row["LONGITUDE"],
                                    row["TIMEZONE_OFFSET"]))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_allFlights():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """SELECT ORIGIN_AIRPORT_ID, DESTINATION_AIRPORT_ID, SUM(DISTANCE), count(*) as count
        from flights group by  ORIGIN_AIRPORT_ID, DESTINATION_AIRPORT_ID order by ORIGIN_AIRPORT_ID"""
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append((row["ORIGIN_AIRPORT_ID"],row["DESTINATION_AIRPORT_ID"],row["SUM(DISTANCE)"],row["count"]))
        cursor.close()
        conn.close()
        return result

if __name__=="__main__":
    lista=DAO.get_allFlights()
    for i in lista:
        print(i)