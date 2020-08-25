import random
from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item

#Offensive spells
Fire = Spell("Fire", 30, 30, "Offensive")
Thunder = Spell("Thunder", 35, 120, "Offensive")
Blizzard = Spell("Blizzard", 5, 70, "Offensive")
Meteor = Spell("Meteor", 30, 300, "Offensive")
Quake = Spell("Quake", 100, 100, "Offensive")
Water = Spell("Water", 110, 101, "Offensive")

#Defensive spells
Cure = Spell("Cure", 12, 120, "Defensive")
Cura = Spell("Cura", 17, 200, "Defensive")

# Creat items
Potion = Item("Potion", "potion", "Heals 50 HP", 50)
SuperPotion = Item("SuperPotion", "potion", "Heals 150 HP", 150)
Elixer = Item("Elixer","potion", "Fully restores HP/MP",9999)
Sword = Item("Sword", "Weapon", "Deals bonus 50 dmg", 50)
Axe = Item("Axe", "Weapon", "Deals 75 HP", 75)

#Player
player_spells = [Fire,Quake,Cura]
enemy_spells = [Thunder,Cura,Blizzard]
player_items = [{"item":Sword, "quantity":5},{"item":Potion, "quantity":10}, {"item":Elixer, "quantity":5}]
player1 = Person("Valos",300, 200, 10 ,34, player_spells, player_items)
player2 = Person("Talos",500, 100, 50 ,34, player_spells, player_items)
player3 = Person("Malos",300, 100, 70 ,34, player_spells, player_items)
enemy1 = Person("Imp-1",200, 200, 70, 21, enemy_spells,[])
enemy2 = Person("Imp-2",200, 200, 70, 31, enemy_spells,[])
enemy3 = Person("Imp-3",200, 200, 70, 31, enemy_spells,[])

players = [player1, player2, player3]
enemies = [enemy1,enemy2, enemy3]

running = True
defeated_enemies = 0;
defeated_players = 0;
print(bcolors.FAIL + bcolors.BOLD + "Enemy Attack" + bcolors.ENDC)

#Fight
while running:

       print("=======================================")
       print("NAME                  HP                                  MP")
       for player in players:
              player.get_stats()
       print("\n")

       for enemy in enemies:
              enemy.get_enemy_stats()
       print("\n")

       #Player turn
       for player in players:
              if defeated_players == 3:
                     print(bcolors.FAIL + "You lose!" + bcolors.ENDC)
                     running = False
                     break
              elif defeated_enemies == 3:
                     print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
                     running = False
                     break
              player.choose_action()
              choice = input("Choose action:")
              index = int(choice) - 1

              #Attack
              if index == 0:
                     dmg = player.gen_damage()
                     enemy = player.choose_target(enemies)
                     enemies[enemy].take_damage(dmg)
                     print("\nYou attacked "+enemies[enemy].name+" for ", dmg, " point of damage.")
                     print("\n")

                     if enemies[enemy].get_hp() == 0:
                            print(enemies[enemy].name+" has died.")
                            del enemies[enemy]
                            defeated_enemies += 1

              #Magic
              elif index == 1:
                     player.choose_magic()
                     magic_choice = int(input("Choose magic: "))-1

                     if magic_choice == -1:
                            continue

                     spell = player.magic[magic_choice]
                     magic_dmg= spell.generate_damage()

                     current_mp = player.get_mp()
                     if spell.cost > current_mp:
                            print(bcolors.FAIL + "Not enought MP " + bcolors.ENDC)
                            continue

                     player.reduce_mp(spell.cost)
                     if spell.type == "Defensive":
                            player.heal(magic_dmg)
                            print(bcolors.OKBLUE + spell.name + " heal for ", str(magic_dmg), "HP" + bcolors.ENDC)
                     elif spell.type == "Offensive":
                            enemy = player.choose_target(enemies)
                            enemies[enemy].take_damage(magic_dmg)
                            print(spell.name+" deals ",str(magic_dmg)," point of damage to "+enemies[enemy].name+".")
                            if enemies[enemy].get_hp() == 0:
                                   print(enemies[enemy].name + " has died.")
                                   print("\n")
                                   del enemies[enemy]
                                   defeated_enemies += 1
              #Item
              elif index == 2:
                     player.choose_item()
                     item_choice = int(input("Choose item: "))-1

                     if item_choice == -1:
                            continue

                     if player.items[item_choice]["quantity"] == 0:
                            print(bcolors.FAIL + "None left..." + bcolors.ENDC)
                            continue

                     item = player.items[item_choice]["item"]
                     player.items[item_choice]["quantity"] -= 1

                     if item.type == "potion":
                            player.heal(item.prop)
                            print(bcolors.OKBLUE + item.name + " heal for", str(item.prop), "HP" + bcolors.ENDC)
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
                            print("\nYou attacked " + enemies[enemy].name + " for ", dmg , " point of damage + "+ item.name + " deals "+str(item.prop) , " point of damage to "+enemies[enemy].name+".")
                            if enemies[enemy].get_hp() == 0:
                                   print(enemies[enemy].name + " has died.")
                                   print("\n")
                                   del enemies[enemy]
                                   defeated_enemies += 1

       print("\n")

       #Enemy
       b = 0
       for enemy in enemies:
              if defeated_players == 3:
                     print(bcolors.FAIL + "You lose!" + bcolors.ENDC)
                     running = False
              elif defeated_enemies == 3:
                     print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
                     running = False
              enemy_choice = random.randrange(0, 2)
              if enemy_choice == 0:
                     a = random.randrange(0,2)
                     enemy_dmg = enemy.gen_damage()
                     players[a].take_damage(enemy_dmg)
                     print(enemies[b].name + " attack for ", enemy_dmg," point of damage.")
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
                            print(bcolors.OKBLUE + spell.name + " heal for ", str(magic_dmg), "HP" + bcolors.ENDC)

                     elif spell.type == "Offensive":
                            a = random.randrange(0, 3)
                            players[a].take_damage(magic_dmg)

                            print(enemies[b].name +" uses " + spell.name+" deals",str(magic_dmg),"point of damage to "+players[a].name+".")
                            if players[a].get_hp() == 0:
                                   print(players[a].name + "has died.")
                                   del players[a]
                                   defeated_players += 1
                     b = +1
       #End of turn
