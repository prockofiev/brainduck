import matplotlib.pyplot as plt
from compile import Compile
from variables import Variables





def get_bf_code_length(b):
    """Функция-обертка для получения длины Brainfuck-кода."""
    with open('test.bd', 'r', encoding='utf-8') as file:
        code = file.read()
    s = [el.remove() for el in Variables.memory]
    compile = Compile( DEBUG = True, ONLY_RESULT = True, SHOW_MEMORY = 30, b =b )
    return len( compile.compile(code) )


def main():
    b_values = list(range(-40, 20))

    lengths = [get_bf_code_length(b) for b in b_values]

    plt.figure(figsize=(10, 6))
    plt.style.use("seaborn-v0_8-whitegrid")

    plt.plot(
        b_values,
        lengths,
        marker="o",
        linestyle="-",
        color="#1f77b4",
        linewidth=2,
        label="Длина кода",
    )

    # Названия осей и графика
    plt.title(
        "Зависимость длины Brainfuck-кода от параметра b в методе copy",
        fontsize=14,
        pad=15,
    )
    plt.xlabel("Параметр b (входное значение)", fontsize=12)
    plt.ylabel("Длина итоговой программы (кол-во символов)", fontsize=12)

    # Включаем сетку для удобства чтения
    plt.grid(True, linestyle="--", alpha=1.0)

    # Показываем легенду
    plt.legend(fontsize=11)

    # Оптимизация полей, чтобы подписи не влезали за границы
    plt.tight_layout()

    # Отображение графика
    

    print( f"Min: { min( lengths ) }" )
    print( f"Max: { max( lengths ) }" )
    plt.show()
if __name__ == "__main__":
    main()
