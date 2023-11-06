import os
import json
import csv
import random
import atexit

SAVE_FOLDER = 'saves'

SAVE_FOLDER = 'C:\\Users\\semen\\Документы\\AssassinsCreedSaves'

def create_save_folder():
    if not os.path.exists(SAVE_FOLDER):
        os.makedirs(SAVE_FOLDER)

character = {
    "name": "",
    "inventory": ['Hidden Blade'],
    "money": 100,
    "health": 100,
    "experience": 0,
    "tribe": "",
    "skills": {}
}

tribes = {
    "Римлянин": {"parkour": 2, "stealth": 1, "combat": 2},
    "Египтянин": {"parkour": 1, "stealth": 3, "combat": 1},
    "Викинг": {"parkour": 1, "stealth": 1, "combat": 4},
    "Грек": {"parkour": 3, "stealth": 2, "combat": 1},
    "Турок": {"parkour": 1, "stealth": 2, "combat": 3},
    "Спартанец": {"parkour": 2, "stealth": 2, "combat": 3}
}

tribes_names = set(tribes.keys())

enemies = ["Enemy Soldier", "Enemy Assassin", "Enemy Spy", "Enemy Gladiator"]
enemy_stats = {
    "Enemy Soldier": {"parkour": 1, "stealth": 1, "combat": 2, "health": 20},
    "Enemy Assassin": {"parkour": 2, "stealth": 2, "combat": 1, "health": 15},
    "Enemy Spy": {"parkour": 1, "stealth": 2, "combat": 1, "health": 15},
    "Enemy Gladiator": {"parkour": 2, "stealth": 2, "combat": 3, "health": 25}
}

locations = {
    "магазин": {
        "предметы_на_продажу": ['Меч', 'Эликсир здоровья', 'Эликсир хитрости', 'Усиление борьбы', 'Щит',
                                'Зелье хитрости', 'Боевое усиление'],
        "стоимости": [50, 25, 40, 30, 75, 50, 60]
    },
    "тренировочная_зона": {
        "навыки_для_прокачки": ["паркур", "хитрость", "борьба"],
        "стоимость_тренировки": [10, 15, 20]
    },
    "храм": {
        "благословение": ["восстановление здоровья", "улучшение навыков"],
        "стоимость_благословения": [30, 50]
    }
}


def introduction_game():
    character["name"] = input("Введите имя вашего персонажа: ")
    print(f"\nДобро пожаловать в мир Assassin's Creed, {character['name']}!\n")


def choose_tribe():
    print("Выберите свое племя.")
    for tribe in tribes:
        skill_set = ', '.join(f"{skill}: {level}" for skill, level in tribes[tribe].items())
        print(f"{tribe} ({skill_set})\n")

    tribe = ""
    while tribe not in tribes_names:
        tribe = input("Введите название вашего племени: ")

    character["tribe"] = tribe
    character["skills"] = tribes[tribe]
    print(f"\nВы выбрали племя {tribe}. А теперь, давайте начнем путешествие!\n")


def experience_bonus():
    if character["experience"] >= 100:
        character["experience"] = 0  # Обнуляем опыт
        print("\nПоздравляем! Вы получили бонус за достижение 100 очков опыта.")
        for skill in character['skills'].keys():
            if character['skills'][skill] < 5:
                character['skills'][skill] += 1
        print("Ваши умения улучшены благодаря вашему опыту.\n")


def game_loop():
    while True:
        print(f"\nCharacter skills: {character['skills']}")
        random_encounter = random.choice([False, True])
        if random_encounter:
            enemy_encounter()

        experience_bonus()

        print("What would you like to do?\n")
        actions = ["Обзор окружения", "Улучшить навыки", "Сдвиг", "Отдых", "Посетить место", "Проверить инвентарь", "Выйти из игры"] # добавлен пункт "Выйти из игры"
        for i, action in enumerate(actions, 1):
            print(f"{i}. {action}\n")

        action = int(input("Выберите действие: "))
        if action == 1:
            observation()
        elif action == 2:
            skill_enhancement()
        elif action == 3:
            move_on()
        elif action == 4:
            rest()
        elif action == 5:
            location_visit()
        elif action == 6:
            check_inventory()
        elif action == 7:  # Добавлено условие для выхода
            exit_game()
        else:
            print("Неизвестная опция. Попробуйте еще раз.")


def observation():
    print("Наблюдение: Вы проходите через великий город Рим, полный суеты.\n")


def skill_enhancement():
    print(f"Ваши текущие навыки: {character['skills']}")
    skills = list(character['skills'].keys())
    for i, skill in enumerate(skills, 1):
        print(f"{i}. Усилите {skill}\n")
    skill_choice = int(input("Какой навык улучшить? "))
    skill_training(skills[skill_choice - 1])


def skill_training(skill):
    if character['money'] >= 10:
        character['money'] -= 10
        character['skills'][skill] += 1
        print(f"\nВы улучшили {skill} навык!\n")
    else:
        print("У вас не достаточно денег для тренировки этого навыка.\n")


def enemy_encounter():
    enemy = random.choice(enemies)
    enemy_skills = enemy_stats[enemy]
    print(f"Враг {enemy} появляется!\n")

    if character['skills']['stealth'] > enemy_skills['stealth']:
        print(f"Вы успешно пробрались мимо {enemy}.\n")
    elif character['skills']['combat'] >= enemy_skills['combat']:
        print(f"Вы вступаете в бой с {enemy}!")
        fight_loop(enemy, enemy_skills)


def fight_loop(enemy, enemy_skills):
    enemy_health = enemy_skills['health']
    while enemy_health > 0 and character['health'] > 0:
        player_attack = character['skills']['combat']
        enemy_health -= player_attack
        print(f"Вы нанесли удар {character['inventory']}, нанеся {player_attack} урона {enemy}!\n")
        if enemy_health <= 0:
            print(f"Вы победили {enemy}!")
            if character['health'] > 0:
                character["experience"] += 10
        else:
            enemy_attack = enemy_skills['combat']
            character['health'] -= enemy_attack
            if character['health'] <= 0:
                print(f"{enemy} победил вас. Игра окончена.")
                exit()
            else:
                print(f"{enemy} наносит ответный удар, нанося {enemy_attack} урона вам!")


def move_on():
    print("Вы двигаетесь дальше, исследуя город.\n")


def rest():
    if character["health"] < 75:
        character["health"] += 25
        print(f"Вы нашли спокойный уголок и восстановили свои силы. Ваше здоровье теперь {character['health']}\n")
    else:
        print("У вас уже максимальное здоровье, продолжайте искать приключения!\n")


def location_visit():
    print("\nКуда бы вы хотели отправиться?\n")
    for location in locations.keys():
        print(f"{location}\n")

    chosen_location = input("Войти в: ")

    if chosen_location in locations.keys():
        if chosen_location == "магазин":
            visit_market()
        elif chosen_location == "тренировочная_зона":
            skill_enhancement()
        elif chosen_location == "храм":
            visit_temple()
    else:
        print("Нет такой локации. Попробуйте еще раз.\n")

def exit_handler():
    save_name = input("Введите имя для сохранения перед выходом: ")
    save_game(character, save_name)
    save_to_csv(character)
    print("Игра завершена. Данные сохранены.")
    atexit.register(exit_handler)
def check_inventory():
    print(f"\nВаш инвентарь: {character['inventory']}")
    print(f"Ваши деньги: {character['money']}\n")


def visit_market():
    print("\nПродавец предлагает вам следующие товары:\n")
    for item, price in zip(locations['магазин']['предметы_на_продажу'], locations['магазин']['стоимости']):
        print(f"{item}: {price}\n")

    chosen_item = input("Выберите товар: ")

    if chosen_item in locations['магазин']['предметы_на_продажу']:
        purchase_item(chosen_item)
    else:
        print("Продавец не может вам это предоставить.\n")


def purchase_item(item):
    item_index = locations['магазин']['предметы_на_продажу'].index(item)
    item_price = locations['магазин']['стоимости'][item_index]

    if character['money'] >= item_price:
        character['money'] -= item_price

        if item not in character['inventory']:
            character['inventory'].append(item)
        print(f"\nВы купили {item}!\n")
    else:
        print("\nУ вас недостаточно денег.\n")


def visit_temple():
    print("Жрец предлагает вам следующие услуги:\n")
    for service, price in zip(locations['храм']['благословение'], locations['храм']['стоимость_благословения']):
        print(f"{service}: {price}\n")

    chosen_service = input("Выберите услугу: ")

    if chosen_service in locations['храм']['благословение']:
        grant_blessing(chosen_service)
    else:
        print("Жрец не может вам это предоставить.\n")


def grant_blessing(blessing):
    blessing_index = locations['храм']['благословение'].index(blessing)
    blessing_price = locations['храм']['стоимость_благословения'][blessing_index]

    if character['money'] >= blessing_price:
        character['money'] -= blessing_price
        print("\nЖрец вручает вам благословение!\n")

        if blessing == 'восстановление здоровья':
            character['health'] = 100
            print("Здоровье восстановлено до максимума.\n")
        elif blessing == 'улучшение навыков':
            for skill in character['skills'].keys():
                character['skills'][skill] += 1
            print("Все навыки были улучшены!\n")
    else:
        print("\nУ вас недостаточно денег.\n")


def save_game(character_data, save_name):
    save_path = os.path.join(SAVE_FOLDER, save_name + '.json')
    with open(save_path, 'w') as file:
        json.dump(character_data, file)

def load_game(save_name):
    save_path = os.path.join(SAVE_FOLDER, save_name + '.json')
    try:
        with open(save_path, 'r') as file:
            character_data = json.load(file)
        return character_data
    except FileNotFoundError:
        return None

def list_saves():
    saves = [f.replace('.json', '') for f in os.listdir(SAVE_FOLDER) if f.endswith('.json')]
    return saves


def save_to_csv(character_data):
    with open('character_data.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            [character_data["name"], character_data["tribe"], character_data["experience"], character_data["money"],
             character_data["health"]])


def delete_save():
    try:
        os.remove('saved_game.json')
        print("Сохранение удалено.")
    except FileNotFoundError:
        print("Нет сохранения для удаления.")


def save_game(character_data, save_name):
    save_path = os.path.join(SAVE_FOLDER, save_name + '.json')
    with open(save_path, 'w') as file:
        json.dump(character_data, file)


def load_game(save_name):
    save_path = os.path.join(SAVE_FOLDER, save_name + '.json')
    try:
        with open(save_path, 'r') as file:
            character_data = json.load(file)
        return character_data
    except FileNotFoundError:
        return None


def list_saves():
    saves = [f.replace('.json', '') for f in os.listdir(SAVE_FOLDER) if f.endswith('.json')]
    return saves

def exit_game():
    save_name = input("Введите имя для сохранения перед выходом: ")
    save_game(character, save_name)
    save_to_csv(character)
    print("Игра завершена. Данные сохранены.")
    exit()

def main():
    create_save_folder()
    atexit.register(exit_handler)
    print("Доступные сохранения:")
    saves = list_saves()
    if saves:
        for i, save in enumerate(saves, 1):
            print(f"{i}. {save}")
    else:
        print("Нет доступных сохранений.")

    load_existing = False
    while not load_existing:
        choice = input("Введите номер сохранения для загрузки или 'новая' для начала новой игры: ")
        if choice.lower() == 'новая':
            introduction_game()
            choose_tribe()
            load_existing = True
        elif choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(saves):
                save_name = saves[choice - 1]
                character_data = load_game(save_name)
                if character_data:
                    print(f"Загружено сохранение '{save_name}'")
                    load_existing = True
                else:
                    print("Ошибка загрузки сохранения.")
            else:
                print("Неправильный номер сохранения.")
        else:
            print("Неправильный ввод.")

    game_loop()
    save_name = input("Введите имя для сохранения: ")
    save_game(character, save_name)
    save_to_csv(character)


if __name__ == "__main__":
    main()