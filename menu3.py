

def search_stock(conn, product_id):
    query = "SELECT name, price, ex_date, num, time, changes FROM products WHERE name = %s"
    cursor.execute(query, (product_id,))
    result = cursor.fetchall()
        if result:
        for row in result:
            print(f"상품명: {row['name']}, 가격: {row['price']}, 유통기한: {row['ex_date']}, "
                  f"수량: {row['num']}, 변경일시: {row['time']}, 변경내용: {row['changes']}")
    else:
        print("상품이 존재하지 않습니다.")


product_id = input("상품명을 입력하세요: ")
search_stock(product_id)


# 연결 종료
cursor.close()
conn.close()



    elif menu == "3":
        product_id = input("상품명을 입력하세요: ")
        search_stock(product_id)