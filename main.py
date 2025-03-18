import sys
from mysql.connector import MySQLConnection, Error
from configparser import ConfigParser


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


def query_with_fetchall(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    rows = cursor.fetchall()
    print("Total Row(s):", cursor.rowcount)

    for row in rows:
        print(row)

    return rows


def insert_book(conn, title, isbn):
    query = "INSERT INTO books(title,isbn) " "VALUES(%s,%s)"

    args = (title, isbn)
    book_id = None
    with conn.cursor() as cursor:
        cursor.execute(query, args)
        book_id = cursor.lastrowid
    conn.commit()
    return book_id


def update_book(book_id, title):
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
display = '''
-------------------------------------------------------------
1. 상품 정보 등록           | 2. 전체 재고 현황 조회
3. 개별 재고 검색           | 4. 재고 정보 수정 및 삭제
5. 입출고 내역 기록 및 조회 | 6. 프로그램 종료
-------------------------------------------------------------
메뉴를 선택하세요 >>> '''

conn = connect()

while True:
    menu = input(display).strip()

    # 상품 정보 등록
    if menu == '1':
       


    elif menu == '2':
       pass

    elif menu == '3':
       pass
       
        
    elif menu == '4':
       pass
        

    elif menu == '5':
       pass
        

    elif menu == '6':
        print('프로그램 종료')
        conn.close()
        sys.exit()

    # 잘못된 입력 처리
    else:
        print("메뉴 선택을 잘못하셨습니다.")