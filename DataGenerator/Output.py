from Generator import Generator
from Csv_operator import  CsvOperator


class Output():     # 불필요한 함수 제거하기 , 내가 원하는 시점에 내가 해당하는 함수를 불러서 실행하기
    
    def output():
        csv_operator = CsvOperator()
        lst = Generator().generator()
        printmode = input('원하는 출력모드(csv/screen): ') # input 위치 주의

        if printmode.lower() == 'csv':
            filename = input('파일 이름: ') + '.csv'
            csv_operator.print_csv(lst, filename)
        elif printmode.lower() == 'screen':
            csv_operator.print_screen(lst)
        else:
            print('출력모드에서 유효하지 않은 값이 입력되었습니다.')
            exit()



if __name__ == "__main__":     # 이 파일 내에서만 실행됨!
    # try:
    Output.output()
    # except ValueError as e:
    #     exit()