import random
from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item

newfile = open("stats.txt", "w+")
# Offensive spells
Fire = Spell("Fire", 30, 30, "Offensive")
Thunder = Spell("Thunder", 150, 120, "Offensive")
Blizzard = Spell("Blizzard", 50, 70, "Offensive")
Meteor = Spell("Meteor", 200, 300, "Offensive")
Quake = Spell("Quake", 100, 100, "Offensive")

# Defensive spells
Heal = Spell("Heal", 12, 100, "Defensive")
Super_Heal = Spell("Super_Heal", 20, 200, "Defensive")

# Create items
Potion = Item("Potion", "HP_potion", "Heals 50 HP", 50)
SuperPotion = Item("SuperPotion", "HP_potion", "Heals 150 HP", 150)
Elixer = Item("Elixer", "elixer", "Fully restores HP/MP", 9999)
ManaPotion = Item("ManaPotion", "MP_potion", "Restore 50 MP", 50)
Sword = Item("Sword", "Weapon", "Deals bonus 50 dmg", 50)
Axe = Item("Axe", "Weapon", "Deals bonus 75 HP", 75)
Bow = Item("Bow", "Weapon", "Deals bonus 50 dmg", 50)
Hammer = Item("Hammer", "Weapon", "Deals bonus 100 dmg", 100)
Dagger = Item("Dagger", "Weapon", "Deals bonus 25 dmg", 20)

# Spells
mage_spells = [Fire, Quake, Blizzard, Meteor, Heal, Super_Heal]
warrior_spells = [Fire, Heal]
assassin_spells = [Fire, Blizzard, Heal]
enemy_spells = [Thunder, Super_Heal, Blizzard]

# Items
warrior_items = [{"item": Hammer, "quantity": 2}, {"item": Axe, "quantity": 5}, {"item": SuperPotion, "quantity": 2}]
mage_items = [{"item": Dagger, "quantity": 5}, {"item": Potion, "quantity": 5}, {"item": ManaPotion, "quantity": 10}]
assassin_items = [{"item": Bow, "quantity": 5}, {"item": Sword, "quantity": 5}, {"item": Potion, "quantity": 5}]

running = True
game = True

while game:
    b = 0
    mageCount = 0
    warriorCount = 0
    AssassinCount = 0
    ForIn = 0
    player = Person("Mage", 300, 200, 10, 34, mage_spells, mage_items)
    players = [player]
    enemy = Person("Imp", 200, 200, 30, 21, enemy_spells, [])
    enemies = [enemy]
    mage = 'Mage '
    warrior = "Warrior "
    Assassin = "Assassin "
# Number of players
    NumberPlayers = input("How many players: ")
    ForIn = int(NumberPlayers)

# Choosing character
    for b in range(ForIn):
        player.choose_character()
        a = input("Choose your character: ")
        ind = int(a) - 1
        if ind == 0:
            mageCount += 1
            c = str(mageCount)
            player = Person(mage + c, 300, 200, 10, 34, mage_spells, mage_items)
            players.append(player)
            print("You choose mage")
            b += 1
        elif ind == 1:
            warriorCount += 1
            c = str(warriorCount)
            player = Person(warrior + c, 500, 100, 50, 34, warrior_spells, warrior_items)
            players.append(player)
            print("You choose warrior")
            b += 1
        elif ind == 2:
            AssassinCount += 1
            c = str(AssassinCount)
            player = Person(Assassin + c, 400, 150, 30, 34, assassin_spells, assassin_items)
            players.append(player)
            print("You choose assassin")
            b += 1

    # Add enemy
    for b in range(ForIn):
        enemy = Person("Imp", 200, 200, 30, 21, enemy_spells, [])
        enemies.append(enemy)
        b += 1

    players.pop(0)
    enemies.pop(0)

    defeated_enemies = 0
    defeated_players = 0
    print(bcolors.FAIL + bcolors.BOLD + "Enemy Attack" + bcolors.ENDC)

    while running:
        LenPl = len(players)
        LenEn = len(enemies)
        print("=======================================")
        print("NAME                  HP                                  MP")
        for player in players:
            player.get_stats()
        print("\n")

        for enemy in enemies:
            enemy.get_enemy_stats()
        print("\n")

        # Player turn
        for player in players:
            if defeated_players == ForIn:
                print(bcolors.FAIL + "You lose!" + bcolors.ENDC)
                string = "You lost! You died from: \n"
                newfile.write(string)
                for enemy in enemies:
                    string2 = str(enemy.name)
                    newfile.write(string2)
                    newfile.write("\n")
                newfile.write("\n")
                newfile.write("\n")
                running = False
                break
            elif defeated_enemies == ForIn:
                print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
                string = "You win! You ended with this players: \n"
                newfile.write(string)
                for player in players:
                    string2 = str(player.name)
                    newfile.write(string2)
                    newfile.write("\n")
                newfile.write("\n")
                newfile.write("\n")
                running = False
                break
            player.choose_action()
            choice = input("Choose action:")
            index = int(choice) - 1

            # Attack
            if index == 0:
                dmg = player.gen_damage()
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(dmg)
                print("\nYou attacked " + enemies[enemy].name + " for ", dmg, " point of damage.")
                print("\n")

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name + " has died.")
                    del enemies[enemy]
                    defeated_enemies += 1

            # Magic
            elif index == 1:
                player.choose_magic()
                magic_choice = int(input("Choose magic: ")) - 1

                if magic_choice == -1:
                    continue

                spell = player.magic[magic_choice]
                magic_dmg = spell.generate_damage()

                current_mp = player.get_mp()
                if spell.cost > current_mp:
                    print(bcolors.FAIL + "Not enough MP " + bcolors.ENDC)
                    continue

                player.reduce_mp(spell.cost)
                if spell.type == "Defensive":
                    player.heal(magic_dmg)
                    print(bcolors.OKBLUE + spell.name + " heal for ", str(magic_dmg), "HP" + bcolors.ENDC)
                elif spell.type == "Offensive":
                    enemy = player.choose_target(enemies)
                    enemies[enemy].take_damage(magic_dmg)
                    print(spell.name + " deals ", str(magic_dmg), " point of damage to " + enemies[enemy].name + ".")
                    if enemies[enemy].get_hp() == 0:
                        print(enemies[enemy].name + " has died.")
                        print("\n")
                        del enemies[enemy]
                        defeated_enemies += 1
            # Item
            elif index == 2:
                player.choose_item()
                item_choice = int(input("Choose item: ")) - 1

                if item_choice == -1:
                    continue

                if player.items[item_choice]["quantity"] == 0:
                    print(bcolors.FAIL + "None left..." + bcolors.ENDC)
                    continue

                item = player.items[item_choice]["item"]
                player.items[item_choice]["quantity"] -= 1

                if item.type == "HP_potion":
                    player.heal(item.prop)
                    print(bcolors.OKBLUE + item.name + " heal for", str(item.prop), "HP" + bcolors.ENDC)
                    print("\n")
                elif item.type == "MP_potion":
                    player.restoreMP(item.prop)
                    print(bcolors.OKBLUE + item.name + " restore for", str(item.prop), "MP" + bcolors.ENDC)
                    print("\n")
                elif item.type == "elixer":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                    else:
                        player.hp = player.maxhp
                        player.mp = player.maxmp
                    print(bcolors.OKBLUE + item.name + " fully restores HP and MP" + bcolors.ENDC)
                    print("\n")
                elif item.type == "Weapon":
                    enemy = player.choose_target(enemies)
                    dmg = player.gen_damage()
                    enemies[enemy].take_damage(dmg)
                    enemies[enemy].take_damage(item.prop)
                    print("\nYou attacked " + enemies[enemy].name + " for ", dmg,
                          " point of damage + " + item.name + " deals " + str(item.prop),
                          " point of damage to " + enemies[enemy].name + ".")
                    if enemies[enemy].get_hp() == 0:
                        print(enemies[enemy].name + " has died.")
                        print("\n")
                        del enemies[enemy]
                        defeated_enemies += 1

        print("\n")

        # Enemy
        b = 0
        for enemy in enemies:
            if defeated_players == ForIn:
                print(bcolors.FAIL + "You lose!" + bcolors.ENDC)
                string = "You lost! You died from: \n"
                newfile.write(string)
                for enemy in enemies:
                    string2 = str(enemy.name)
                    newfile.write(string2)
                    newfile.write("\n")
                newfile.write("\n")
                newfile.write("\n")
                running = False
                break
            elif defeated_enemies == ForIn:
                print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
                string = "You win! You ended with this players: \n"
                newfile.write(string)
                for player in players:
                    string2 = str(player.name)
                    newfile.write(string2)
                    newfile.write("\n")
                newfile.write("\n")
                newfile.write("\n")
                running = False
                break
            enemy_choice = random.randrange(0, 2)
            if enemy_choice == 0:
                a = random.randrange(0, LenPl)
                enemy_dmg = enemy.gen_damage()
                players[a].take_damage(enemy_dmg)
                print(enemies[b].name + " attack for ", enemy_dmg, " point of damage to " + players[a].name + ".")
                if players[a].get_hp() == 0:
                    print(players[a].name + " has died.")
                    del players[a]
                    defeated_players += 1

                b = +1
            elif enemy_choice == 1:
                spell, magic_dmg = enemy.choose_enemy_spell()
                enemy.reduce_mp(spell.cost)
                if spell.type == "Defensive":
                    enemy.heal(magic_dmg)
                    print(enemies[b].name + " uses " + bcolors.OKBLUE + spell.name + " heal for ", str(magic_dmg),
                          "HP" + bcolors.ENDC)

                elif spell.type == "Offensive":
                    a = random.randrange(0, LenPl)
                    players[a].take_damage(magic_dmg)
                    print(enemies[b].name + " uses " + spell.name + " deals", str(magic_dmg),
                          "point of damage to " + players[a].name + ".")
                    if players[a].get_hp() == 0:
                        print(players[a].name + " has died.")
                        del players[a]
                        defeated_players += 1
                b = +1
        # End of turn
    userInput = input("Enter 'R' to restart or 'X' to exit: ").capitalize()

    if userInput == "X":
        print('Goodbye.')
        game = False
    elif userInput == "R":
        running = True
        continue
