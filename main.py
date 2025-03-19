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


def insert_or_update_product(conn, name, price, ex_date, num):
    with conn.cursor() as cursor:
        # 1. 동일한 상품이 있는지 확인
        check_query = """
        SELECT num FROM Product
        WHERE name = %s AND price = %s AND ex_date = %s
        """
        cursor.execute(check_query, (name, price, ex_date))
        result = cursor.fetchone()

        if result:
            # 2. 존재하면 수량 업데이트
            update_query = """
            UPDATE Product
            SET num = num + %s, time = NOW(), changes = '수량 추가'
            WHERE name = %s AND price = %s AND ex_date = %s
            """
            cursor.execute(update_query, (num, name, price, ex_date))
        else:
            # 3. 없으면 새로 삽입
            insert_query = """
            INSERT INTO Product(name, price, ex_date, num, time, changes)
            VALUES (%s, %s, %s, %s, NOW(), '상품 등록')
            """
            cursor.execute(insert_query, (name, price, ex_date, num))

    conn.commit()


def update_Product(conn, name, num):
    # 준비된 쿼리: 수량 업데이트, 변경 시간과 로그 추가
    query = """ 
    UPDATE Product
    SET num = %s, time = NOW(), changes = '수량 변경'
    WHERE name = %s
    """

    data = (num, name)

    affected_rows = 0  # 영향을 받은 행의 수를 저장할 변수 초기화

    # 데이터베이스에 쿼리 실행
    with conn.cursor() as cursor:
        cursor.execute(query, data)
        affected_rows = cursor.rowcount  # 변경된 행 수를 가져옴

    # 커밋하여 변경 사항 저장
    conn.commit()

    return affected_rows  # 변경된 행의 수 반환

def delete_Product(conn, name):
    query = "DELETE FROM product WHERE name = %s"
    data = (name,)
    affected_rows = 0  # Initialize the variable to store the number of affected rows
    with conn.cursor() as cursor:
        cursor.execute(query, data)
        affected_rows = cursor.rowcount
    conn.commit()

    return affected_rows  # Return the number of affected rows


def show_product_logs(conn):
    cursor = conn.cursor()
    # 시간 순으로 정렬해서 가져오기
    cursor.execute("SELECT name, changes, time FROM Product ORDER BY time ASC")
    rows = cursor.fetchall()

    print("📦 입출고 내역 (시간 순):")
    print()

    for idx, row in enumerate(rows, start=1):
        name, changes, time = row
        print(f"[{idx}] 상품명: {name}")
        print(f"    변경 내용: {changes}")
        print(f"    시간: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 40)

    return rows


def get_product_info(conn, name):
    query = "SELECT name, price, ex_date, num FROM Product WHERE name = %s"
    with conn.cursor() as cursor:
        cursor.execute(query, (name,))
        result = cursor.fetchall()
    
    if result:
        return result
    else:
        return "상품을 찾을 수 없습니다."



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

        insert_or_update_product(conn, name, price, ex_date, num)

    elif menu == "2":
        query_with_fetchall(conn)

    elif menu == "3":
        product_name = input("조회하고 싶은 상품명을 입력하세요: ")
        product_infos = get_product_info(conn, product_name)

        if product_infos:
            for idx, info in enumerate(product_infos, start=1):
                print(f"\n[{idx}]")
                print(f"상품명: {info[0]}")
                print(f"가격: {info[1]}원")
                print(f"유통기한: {info[2]}")
                print(f"수량: {info[3]}개")
        else:
            print(f"{product_name} 상품은 존재하지 않습니다.")

    elif menu == "4":
        action = input("수정하려면 1을, 삭제하려면 2를 입력하세요: ").strip()

        if action == "1":  # 수량 수정
            name = input("수정할 상품명을 입력하세요: ")
            num = input("새로운 수량을 입력하세요: ")

            updated_rows = update_Product(conn, name, num)
            if updated_rows > 0:
                print(f"'{name}'의 수량이 {num}으로 변경되었습니다.")
            else:
                print("해당 상품을 찾을 수 없습니다.")

        elif action == "2":  # 삭제 기능 추가
            name = input("삭제할 상품명을 입력하세요: ")
            deleted_rows = delete_Product(conn, name)

            if deleted_rows > 0:
                print(f"'{name}' 상품이 삭제되었습니다.")
            else:
                print("해당 상품을 찾을 수 없습니다.")

        else:
            print("잘못된 입력입니다. 다시 시도하세요.")

    elif menu == "5":
        show_product_logs(conn)

    elif menu == "6":
        print("프로그램 종료")
        conn.close()
        sys.exit()

    # 잘못된 입력 처리
    else:
        print("메뉴 선택을 잘못하셨습니다.")
