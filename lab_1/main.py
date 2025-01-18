def combinations(signs: list, repeat: int) -> list:
    """ Функция генерирует все комбинации последовательностей операторов """
    all_combinations = [[]]
    for _ in range(repeat):
        buff = []
        for combination in all_combinations:
            for sign in signs:
                buff.append(combination+[sign])
        all_combinations = buff
    return all_combinations

def solve(index: int = 0) -> str:
    """ Функция перебирает комбинации операторов """
    result = get_result(all_operators[index])
    if result == S:
        return render_result_string(all_operators[index])
    elif all_operators[index] == all_operators[-1]:
        return "no solution"
    else:
        return solve(index+1)


def get_result(operators: list) -> int:    
    """ Функция высчитывает числовой ответ учитывая переданную последовательность операторов """
    result = NUMBERS[0]
    for i in range(len(NUMBERS)-1):
        # В зависимости от оператора выполняет действие с числами
        if operators[i] == "+":
            result += NUMBERS[i+1]
        else:
            result -= NUMBERS[i+1]
            
    return result


def render_result_string(operators: list) -> str:
    """ Функция создаёт результирующую строку из чисел и операторов между ними """
    result_string = str(NUMBERS[0])
    for i in range(len(NUMBERS)-1):
        # Соединяет оператор и число
        result_string += str(operators[i]) + str(NUMBERS[i+1])
    result_string += f"={S}"
    
    return result_string


if __name__ == "__main__":
    with open('input.txt', 'r', encoding='UTF-8') as f:
        input_data = f.readline().strip().split()
    
    N = int(input_data[0])
    NUMBERS = list(map(int, input_data[1:-1]))
    S = int(input_data[-1])
    all_operators = combinations("+-", N-1)
    
    result = solve()
    with open("output.txt", "w", encoding="UTF-8") as f:
        f.write(result)
