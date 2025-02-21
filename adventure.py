'''
Week 5 coding assignment: The Enchanted Artifacts and the Cryptic Library

Submitted by Braden Mills
'''

import random

def discover_artifact(player_stats, artifacts, artifact_name):
    """ Controls artifact discovery and updates player stats """
    if artifact_name in artifacts:
        artifact = artifacts[artifact_name]
        print(f"\nYou discovered {artifact_name}!")
        print(f"{artifact['description']}")
        if artifact["effect"] == "increases health":
            player_stats["health"] += artifact["power"]
            print(f"Your health increased by {artifact['power']}!")
        elif artifact["effect"] == "enhances attack":
            player_stats["attack"] += artifact["power"]
            print(f"Your attack increased by {artifact['power']}!")
        artifacts.pop(artifact_name) # Removes artifact so it cannot be found again
    else:
        print("You found nothing of interest.")
    return player_stats, artifacts

def find_clue(clues, new_clue):
    """ Manages new and repeated clues """
    if new_clue in clues:
        print("You already know this clue.")
    else:
        clues.add(new_clue)
        print(f"You discovered a new clue: {new_clue}")
    return clues

def acquire_item(inventory, item):
    """ Adds an item to the player's inventory """
    if item not in inventory:
        inventory.append(item)
        print(f"You acquired a {item}!")
    else:
        print(f"You already have {item}.")
    return inventory

def display_inventory(inventory):
    """ Displays the player's inventory """
    num = 1
    if not inventory:
        print("Your inventory is empty.")
    else:
        print("\nYour inventory:")
        for item in inventory:
            print(f"{num}. {item}")
            num += 1

def display_player_status(player_stats):
    """ Displays current health of player """
    print("Your current health:", player_stats["health"])

def handle_path_choice(player_stats):
    """ Updates the player's path choice and health accordingly """
    path = random.choice(["left", "right"])
    if path == "left":
        print("\nYou encounter a friendly gnome who heals you for 10 health points.")
        player_stats["health"] += 10
        player_stats["health"] = min(player_stats["health"], 100)
    elif path == "right":
        print("\nYou fall into a pit and lose 15 health points.")
        player_stats["health"] -= 15
        if player_stats["health"] < 0:
            player_stats["health"] = 0
            print("You are barely alive!")
    return player_stats

def combat_encounter(player_stats, monster_health, has_treasure):
    """ Controls the combat between monster and player """
    while player_stats["health"] > 0 and monster_health > 0:
        print("You attack!")
        monster_health -= player_stats["attack"]
        print(f"The monster's health is now {monster_health}.")

        if monster_health > 0:
            critical = random.random() < 0.5
            damage = 20 if critical else 10
            player_stats["health"] -= damage
            print(f"The monster hits you for {damage} damage!")
            print(f"Your health is now {player_stats['health']}.")

    if monster_health <= 0:
        print("You defeated the monster!")
        return has_treasure
    if player_stats["health"] <= 0:
        print("You have fallen in battle.")
    return False

def check_for_treasure(has_treasure):
    """ Checks whether the monster has treasure after being defeated """
    if has_treasure:
        print("You found the hidden treasure!")
    else:
        print("The monster did not have the treasure. You continue your journey.")

def enter_dungeon(player_stats, inventory, dungeon_rooms, clues):
    """ Determines the dungeon rooms and cryptic library """
    for room in dungeon_rooms:
        room_description, item, challenge_type, challenge_outcome = room
        print(f"\n{room_description}")
        if item:
            print(f"You found a {item}.")
            inventory.append(item)
        if challenge_type == "puzzle":
            print("You encounter a puzzle!")
            choice = input("Do you want to solve or skip the puzzle? ").lower()
            if choice == "solve":
                success = random.choice([True, False])
                print(challenge_outcome[0] if success else challenge_outcome[1])
                player_stats["health"] += challenge_outcome[2]

        elif challenge_type == "trap":
            print("You see a potential trap!")
            choice = input("Do you want to disarm or bypass the trap? ").lower()
            if choice == "disarm":
                success = random.choice([True, False])
                if success:
                    print(challenge_outcome[0])
                else:
                    print(challenge_outcome[1])
                    player_stats["health"] += challenge_outcome[2]
        elif challenge_type == "library":
            print("You explore the Cryptic Library...")
            possible_clues = [
                "The treasure is hidden where the dragon sleeps.",
                "The key lies with the gnome.",
                "Beware the shadows.",
                "The amulet unlocks the final door."
            ]
            selected_clues = random.sample(possible_clues, 2)
            for clue in selected_clues:
                clues = find_clue(clues, clue)
            if "staff_of_wisdom" in inventory:
                print("With the Staff of Wisdom, you understand the clues!")
                print("You can now bypass a future puzzle.")
        elif challenge_type == "none":
            print("There doesn't seem to be a challenge in this room. You move on.")
        display_inventory(inventory)
    print("You have explored all of the dungeon.")
    display_player_status(player_stats["health"])
    return player_stats, inventory, clues

def main():
    """Main game loop."""
    dungeon_rooms = [
        ("Dusty library", "key", "puzzle",
        ("Solved puzzle!", "Puzzle unsolved.", -5)),
        ("Narrow passage, creaky floor", "torch", "trap",
        ("Avoided trap!", "Triggered trap!", -10)),
        ("Grand hall, shimmering pool", "healing potion", "none", None),
        ("Small room, locked chest", "treasure", "puzzle",
        ("Cracked code!", "Chest locked.", -5)),
        ("Cryptic Library", None, "library", None)
    ]
    player_stats = {'health': 100, 'attack': 5}
    monster_health = 70
    inventory = []
    clues = set()
    artifacts = {
        "amulet_of_vitality": {
            "description": "Glowing amulet, life force.",
            "power": 15,
            "effect": "increases health"
        },
        "ring_of_strength": {
            "description": "Powerful ring, attack boost.",
            "power": 10,
            "effect": "enhances attack"
        },
        "staff_of_wisdom": {
            "description": "Staff of wisdom, ancient.",
            "power": 5,
            "effect": "solves puzzles"
        }
    }
    has_treasure = random.choice([True, False])
    display_player_status(player_stats)
    player_stats = handle_path_choice(player_stats)
    if player_stats['health'] > 0:
        treasure_obtained_in_combat = combat_encounter(
            player_stats, monster_health, has_treasure)
        if treasure_obtained_in_combat is not None:
            check_for_treasure(treasure_obtained_in_combat)
        if random.random() < 0.3:
            artifact_keys = list(artifacts.keys())
            if artifact_keys:
                artifact_name = random.choice(artifact_keys)
                player_stats, artifacts = discover_artifact(
                    player_stats, artifacts, artifact_name)
                display_player_status(player_stats)
        if player_stats['health'] > 0:
            player_stats, inventory, clues = enter_dungeon(
                player_stats, inventory, dungeon_rooms, clues)
            print("\n--- Game End ---")
            display_player_status(player_stats)
            print("Final Inventory:")
            display_inventory(inventory)
            print("Clues:")
            if clues:
                for clue in clues:
                    print(f"- {clue}")
            else:
                print("No clues.")

if __name__ == "__main__":
    main()
