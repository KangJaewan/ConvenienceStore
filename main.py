import sys
from mysql.connector import MySQLConnection, Error
from configparser import ConfigParser
import datetime


def read_config(filename="app.ini", section="mysql"):
    # Create a ConfigParser object to handle INI file parsing
    config = ConfigParser()

    # Read the specified INI configuration file
    config.read(filename)

    # Initialize an empty dictionary to store configuration data
    data = {}

    # Check if the specified section exists in the INI file
    if config.has_section(section):
        # Retrieve all key-value pairs within the specified section
        items = config.items(section)

        # Populate the data dictionary with the key-value pairs
        for item in items:
            data[item[0]] = item[1]
    else:
        # Raise an exception if the specified section is not found
        raise Exception(f"{section} section not found in the {filename} file")

    # Return the populated data dictionary
    return data


def connect():
    conn = None
    try:
        print("Connecting to MySQL database...")
        config = read_config()
        conn = MySQLConnection(**config)
    except Error as error:
        print(error)
    return conn


# def query_with_fetchall(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM product")
    rows = cursor.fetchall()
    print("Total Row(s):", cursor.rowcount)

    for row in rows:
        print(row)

    return rows

    # def insert_book(conn, name, price, ex_date, num):
    query = "INSERT INTO Product(name, price, ex_date, num) " "VALUES(%s,%s)"

    args = (name, price, ex_date, num)
    book_id = None
    with conn.cursor() as cursor:
        cursor.execute(query, args)
        book_id = cursor.lastrowid
    conn.commit()
    return book_id
def query_with_fetchall(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Product")
    rows = cursor.fetchall()
    print("총 상품 개수:", cursor.rowcount)
    print()

    for idx, row in enumerate(rows, start=1):
        name, price, ex_date, num, *_ = row  # time, changes는 무시
        print(f"[{idx}] 상품명: {name}")
        print(f"    가격: {price}원")
        print(f"    유통기한: {ex_date}")
        print(f"    수량: {num}개")
        print("-" * 40)

    return rows



def insert_Product(conn, name, price, ex_date, num, changes):
    # SQL 쿼리: 'time'을 NOW() 함수로 자동 설정
    query = """
    INSERT INTO Product(name, price, ex_date, num, time, changes)
    VALUES (%s, %s, %s, %s, NOW(), %s)
    """

    # 입력받은 값들을 args로 묶어 전달 (time은 NOW()로 자동 처리)
    args = (name, price, ex_date, num, changes)

    # Product_id를 None으로 초기화
    Product_id = None

    # 데이터베이스에 쿼리 실행
    with conn.cursor() as cursor:
        cursor.execute(query, args)
        Product_id = cursor.lastrowid  # 마지막 삽입된 행의 ID를 가져옴

    # 커밋하여 변경사항 저장
    conn.commit()

    return Product_id

def update_book(Product_id, name):
    # prepare query and data
    query = """ UPDATE books
                SET title = %s
                WHERE id = %s """

    data = (title, book_id)

    affected_rows = 0  # Initialize the variable to store the number of affected rows

    with conn.cursor() as cursor:
        cursor.execute(query, data)
        affected_rows = cursor.rowcount
    conn.commit()

    return affected_rows  # Return the number of affected rows


def delete_book(conn, book_id):
    query = "DELETE FROM books WHERE id = %s"
    data = (book_id,)
    affected_rows = 0  # Initialize the variable to store the number of affected rows
    with conn.cursor() as cursor:
        cursor.execute(query, data)
        affected_rows = cursor.rowcount
    conn.commit()

    return affected_rows  # Return the number of affected rows



# 메뉴
display = """
-------------------------------------------------------------
1. 상품 정보 등록           | 2. 전체 재고 현황 조회
3. 개별 재고 검색           | 4. 재고 정보 수정 및 삭제
5. 입출고 내역 기록 및 조회 | 6. 프로그램 종료
-------------------------------------------------------------
메뉴를 선택하세요 >>> """

conn = connect()

while True:
    menu = input(display).strip()

    # 상품 정보 등록
    if menu == "1":
        name = input("상품명을 입력하세요: ")
        price = input("가격을 입력하세요: ")
        ex_date = input("유통기한을 입력하세요 (YYYY-MM-DD 형식): ")
        num = input("수량을 입력하세요: ")
        changes = "상품 등록"

        insert_Product(conn, name, price, ex_date, num, changes)

    elif menu == "2":
        query_with_fetchall(conn)

    elif menu == "3":
        pass

    elif menu == "4":
        pass

    elif menu == "5":
        pass

    elif menu == "6":
        print("프로그램 종료")
        conn.close()
        sys.exit()

    # 잘못된 입력 처리
    else:
        print("메뉴 선택을 잘못하셨습니다.")
