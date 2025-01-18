def get_all_moves(princesses_coords: list) -> set:
    """ Функция возвращает ходы всех фигур, переданных в списке """
    def get_moves(princess_coords: tuple) -> set:
        """ Функция возвращает ходы переданной фигуры """
        moves = set()
        y = princess_coords[0]
        x = princess_coords[1]

        def get_vertical_moves() -> set:
            vertical_moves = set()
            for move in range(1,4):
                if y-move >= 0:
                    vertical_moves.add((y-move,x))
                if y+move < N:
                    vertical_moves.add((y+move,x))
            return vertical_moves

        def get_horizontal_moves() -> set:
            horizontal_moves = set()
            for move in range(1,4):
                if x-move >= 0:
                    horizontal_moves.add((y,x-move))
                if x+move < N:
                    horizontal_moves.add((y,x+move))
            return horizontal_moves
        
        def get_diagonal_moves() -> set:
            diagonal_moves = set()
            for move in range(1,4):
                # Диагональные ходы "\": с левого верхнего угла к правому нижнему
                if x-move >= 0 and y-move >= 0:
                    diagonal_moves.add((y-move,x-move))
                if x+move < N and y+move < N:
                    diagonal_moves.add((y+move,x+move))
                # Диагональные ходы "/": с левого нижнего угла к правому верхнему
                if x-move >= 0 and y+move < N:
                    diagonal_moves.add((y+move,x-move))
                if x+move < N and y-move >= 0:
                    diagonal_moves.add((y-move,x+move))
            return diagonal_moves

        moves = get_vertical_moves() | get_horizontal_moves() | get_diagonal_moves()
        return moves
    
    all_moves = set()
    for princess_coords in princesses_coords:
        all_moves |= get_moves(princess_coords)
    return all_moves

def solve() -> list:
    def is_result(princesses_coords: list) -> bool:
        """ Функция проверяет количество расставленных фигур с требуемым количеством """
        if len(princesses_coords) == K+L:
            return True
        return False
    
    def get_childs(princesses_coords: list, current_princess_coords: tuple, moves: set) -> list:
        """ Функция возвращает координаты клеток, в которые можно поставить последующие фигуры """
        childs = []
        y = current_princess_coords[0]

        # Начинаем с чётвертой по счёту клетки, так как принцесса ходит на три
        x = current_princess_coords[1]+4

        # Перебираем координаты на наличие свободных клеток, не находящихся под боем других фигур
        while y < N:
            if x >= N:
                x = 0
                y += 1
                continue
            if is_safe((y,x), princesses_coords, moves):
                childs.append(princesses_coords + [(y,x)])
            x+=1
        return childs

    def is_safe(cell: tuple, princesses_coords: list, moves: set) -> bool:
        """ Функция проверяет, находится ли клетка под боем других фигур и не занята ли она """
        if (cell in princesses_coords) or (cell in moves):
            return False
        return True

    def solve_childs(current_princesses: list, parent_moves: set) -> None:
        """ Функция расставляет фигуры по безопасным клеткам """
        nonlocal result
        current_moves = get_all_moves([current_princesses[-1]]) | parent_moves
        childs = get_childs(current_princesses, current_princesses[-1], current_moves)

        for child in childs:
            if is_result(child):
                # Если один из "детей" является решением, значит и все остальные являются решением
                # Так как за один раз выставляется только одна фигура
                result += childs
                break
            else:
                # Если "ребёнок" не является решением, то расставляем фигуры дальше
                solve_childs(child, current_moves)

    
    INITIAL_MOVES = get_all_moves(INITIAL_PRINCESSES_COORDS)
    all_first_princesses = get_childs(INITIAL_PRINCESSES_COORDS, (0,-4), INITIAL_MOVES)
    
    result = []
    for princesses in all_first_princesses:
        solve_childs(princesses, INITIAL_MOVES)
    
    return result

def render_result(result: list) -> None:
    """ Функция выводит на консоль все доски с расставленными фигурами и отрисованными ходами """
    def render_board(princesses_coords: list) -> None:
        """ Функция отрисовывает конкретную доску """
        moves = get_all_moves(princesses_coords)
        for y in range(N):
            for x in range(N):
                if (y,x) in princesses_coords:
                    print("#", end="")
                elif (y,x) in moves:
                    print("*", end="")
                else:
                    print("0", end="")
            print("\n", end="")
        print("\n", end="")

    for princesses_coords in result:
        render_board(princesses_coords)

if __name__ == "__main__":
    # Читаем входные данные
    with open("input.txt", "r", encoding="UTF-8") as f:
        params = list(map(int, f.readline().strip().split()))
        INITIAL_PRINCESSES_COORDS = [tuple(map(int, line.strip().split())) for line in f.readlines()]
    
    N = params[0] # Размерность доски
    L = params[1] # Количество фигур, которые нужно расставить
    K = params[2] # Количество уже расставленных фигур
    
    result = solve()

    # Записываем результат в файл
    with open("output.txt", "w", encoding="UTF-8") as f:
        if not result:
            f.write("no solutions")
        else:
            for princesses in result:
                f.write(str(princesses) + "\n") 

    #render_result(result) # Отрисовать все результаты
