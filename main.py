import sys

# 메뉴
display = '''
-------------------------------------------------------------
1. 상품 등록      | 2. 현재 재고 보기     | 3. 재고 검색
4. 재고 수정/삭제 | 5. 입출고 기록 관리   | 6. 종료
-------------------------------------------------------------
메뉴를 선택하세요 >>> '''


while True:
    menu = input(display).strip()

    # 도서 등록
    if menu == '1':
       pass


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
        sys.exit()

    # 잘못된 입력 처리
    else:
        print("메뉴 선택을 잘못하셨습니다.")