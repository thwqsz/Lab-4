length = 3
width = 3
full_volume = length * width - 1
initial_points = 15
mandatory_item = 'i'

items = {
    'r': {'points': 25, 'volume': 3},
    'p': {'points': 15, 'volume': 2},
    'a': {'points': 15, 'volume': 2},
    'm': {'points': 20, 'volume': 2},
    'i': {'points': 5, 'volume': 1},
    'k': {'points': 15, 'volume': 1},
    'x': {'points': 20, 'volume': 3},
    't': {'points': 25, 'volume': 1},
    'f': {'points': 15, 'volume': 1},
    'd': {'points': 10, 'volume': 1},
    's': {'points': 20, 'volume': 2},
    'c': {'points': 20, 'volume': 2},
}

item_values = list(items.values())
item_keys = list(items.keys())


def generate_table(items, max_capacity=full_volume):
    dp_table = [[0] * (max_capacity + 1) for _ in range(len(items))]
    for idx, (_, properties) in enumerate(items.items()):
        value = properties['points']
        size = properties['volume']

        for current_capacity in range(max_capacity + 1):
            if idx == 0:
                dp_table[idx][current_capacity] = value if size <= current_capacity else 0
            else:
                without_item = dp_table[idx - 1][current_capacity]
                with_item = (
                    dp_table[idx - 1][current_capacity - size] + value
                    if size <= current_capacity
                    else 0
                )
                dp_table[idx][current_capacity] = max(without_item, with_item)
    return dp_table


def determine_selected_items(dp_table):
    max_points = dp_table[-1][full_volume]
    selected_items = []
    column = full_volume
    row = len(dp_table) - 1

    while row >= 0 and column > 0:
        if row == 0 or dp_table[row][column] != dp_table[row - 1][column]:
            selected_items.append(row)
            column -= item_values[row]['volume']
        row -= 1

    # Проверяем наличие обязательного предмета
    if mandatory_item not in [item_keys[i] for i in selected_items]:
        selected_items.append(item_keys.index(mandatory_item))
    return selected_items, max_points


def calculate_final_score(selected_items):
    selected_points = sum(items[item_keys[i]]['points'] for i in selected_items)
    total_points = sum(item['points'] for item in items.values())
    penalty = total_points - selected_points
    return initial_points + selected_points - penalty


def arrange_items(selected_items):
    backpack = [[0] * length for _ in range(width)]
    remaining_items = []

    for idx in selected_items:
        item = item_keys[idx]
        size = items[item]['volume']
        symbol = f"[{item}]"

        placed = False
        if size == 1:
            for row in range(width):
                for col in range(length):
                    if backpack[row][col] == 0:
                        backpack[row][col] = symbol
                        placed = True
                        break
                if placed:
                    break
        elif size == 2:
            for row in range(width):
                for col in range(length - 1):
                    if backpack[row][col] == 0 and backpack[row][col + 1] == 0:
                        backpack[row][col] = symbol
                        backpack[row][col + 1] = symbol
                        placed = True
                        break
                if placed:
                    break
        elif size == 3:
            for row in range(width):
                for col in range(length - 2):
                    if (
                        backpack[row][col] == 0
                        and backpack[row][col + 1] == 0
                        and backpack[row][col + 2] == 0
                    ):
                        backpack[row][col] = symbol
                        backpack[row][col + 1] = symbol
                        backpack[row][col + 2] = symbol
                        placed = True
                        break
                if placed:
                    break

        if not placed:
            remaining_items.append(item)

    return backpack, remaining_items


if __name__ == "__main__":
    dp_table = generate_table(items)
    selected_indices, max_points = determine_selected_items(dp_table)
    final_score = calculate_final_score(selected_indices)
    backpack, leftovers = arrange_items(selected_indices)

    print("Инвентарь:")
    for row in backpack:
        print(", ".join(map(str, row)))
    print("Итоговые очки выживания:", final_score)


