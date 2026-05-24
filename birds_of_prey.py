import random

class Bird:
    def __init__(self, species, speed, weight, strength, energy=100, health=100):
        self.species = species
        self.speed = speed
        self.weight = weight
        self.strength = strength
        self.energy = energy
        self.health = health
        self.is_alive = True

    def __str__(self):
        return f"--- {self.species} ---\nHealth: {self.health}/100\nEnergy: {self.energy}/100\nSpeed: {self.speed}/10\nWeight: {self.weight}/10\nStrength: {self.strength}/10"

    def train_or_feed(self):
        self.energy += 25
        self.health += 10
        
        if self.energy > 100: 
            self.energy = 100
        if self.health > 100: 
            self.health = 100
            
        print(f"\n{self.species} is resting up. Energy and Health restored.")
        write_log(f"{self.species} trained.")

    def hunt(self):
        if self.energy < 20:
            print("\nYour bird is too tired! Not enough energy to hunt.")
            return

        self.energy -= 20
        weather_roll = random.randint(1, 10)
        modifier = 0
        
        if weather_roll <= 2:
            print("Oh no, a storm hit while flying! (-15 Health)")
            self.health -= 15
            modifier = -2
        elif weather_roll >= 9:
            print("Perfect tailwinds! You dive incredibly fast. (+2 success)")
            modifier = 2

        if self.health <= 0:
            self.is_alive = False
            return

        hunt_score = (self.speed * 0.5) + (self.strength * 0.5) + random.randint(1, 5) + modifier
        
        if hunt_score >= 8:
            print("Success! You caught your prey. (+10 Health)")
            self.health += 10
            if self.health > 100: 
                self.health = 100
            write_log(f"{self.species} hunted successfully.")
        else:
            print("Failure. The prey managed to escape.")
            write_log(f"{self.species} failed a hunt.")

    def get_health_bar(self, name, current, maximum):
        display_health = max(0, current)
        total_bars = int((display_health / maximum) * 20)
        
        health_string = ""
        for i in range(20):
            if i < total_bars:
                health_string += "█"
            else:
                health_string += "-"
                
        return f"{name:10} [{health_string}] {display_health}/{maximum}"

    def duel(self):
        print("\n" + "="*40)
        print("         DUEL INITIATED!        ")
        print("="*40)
        
        enemy_health = 100
        enemy_strength = random.randint(5, 10)
        enemy_speed = random.randint(5, 10)
        
        print(f"A wild rival bird challenges you for territory!")
        print(f"Your Stats  -> Strength: {self.strength}, Speed: {self.speed}")
        print(f"Rival Stats -> Strength: {enemy_strength}, Speed: {enemy_speed}\n")

        while self.health > 0 and enemy_health > 0:
            print(self.get_health_bar("You", self.health, 100))
            print(self.get_health_bar("Rival", enemy_health, 100))
            print("-" * 40)
            
            print("1. Talon Strike (Accurate, Low Damage)")
            print("2. Dive Bomb    (Risky, High Damage)")
            print("3. Roost        (Heal Health, Skip Attack)")
            print("4. Flee         (Attempt to escape)")
            
            choice = input("Choose your move (1-4): ")
            print("")
            
            if choice == '1':
                hit_chance = 80 + (self.speed * 2) - (enemy_speed * 2)
                if random.randint(1, 100) <= hit_chance:
                    damage = random.randint(10, 15) + self.strength
                    enemy_health -= damage
                    print(f"-> You hit the rival with Talon Strike for {damage} damage!")
                else:
                    print("-> You missed your Talon Strike!")
                    
            elif choice == '2':
                hit_chance = 50 + (self.speed * 2) - (enemy_speed * 2)
                if random.randint(1, 100) <= hit_chance:
                    damage = random.randint(25, 40) + self.strength
                    enemy_health -= damage
                    print(f"-> CRITICAL! You crushed the rival with a Dive Bomb for {damage} damage!")
                else:
                    print("-> Your Dive Bomb missed completely!")
                    
            elif choice == '3':
                heal_amount = random.randint(15, 25)
                self.health += heal_amount
                if self.health > 100: 
                    self.health = 100
                print(f"-> You backed off and Roosted, recovering {heal_amount} health!")
                
            elif choice == '4':
                flee_chance = 50 + (self.speed * 3) - (enemy_speed * 3)
                if random.randint(1, 100) <= flee_chance:
                    print("-> You successfully escaped the battle!")
                    write_log(f"{self.species} fled from a duel.")
                    return True
                else:
                    print("-> You tried to flee, but the rival blocked your path!")
            else:
                print("-> Invalid choice. You wasted your turn confused!")

            if enemy_health <= 0:
                print("\n*** You defeated the rival bird! ***")
                write_log(f"{self.species} won a dynamic duel.")
                return True

            print("\n-- Rival's Turn --")
            enemy_action = random.choice([1, 2])
            
            if enemy_action == 1:
                hit_chance = 80 + (enemy_speed * 2) - (self.speed * 2)
                if random.randint(1, 100) <= hit_chance:
                    damage = random.randint(10, 15) + enemy_strength
                    self.health -= damage
                    print(f"-> The rival slashes you for {damage} damage!")
                else:
                    print("-> The rival's attack missed!")
            else:
                hit_chance = 50 + (enemy_speed * 2) - (self.speed * 2)
                if random.randint(1, 100) <= hit_chance:
                    damage = random.randint(20, 35) + enemy_strength
                    self.health -= damage
                    print(f"-> The rival lands a devastating Swoop for {damage} damage!")
                else:
                    print("-> The rival's Swoop missed!")
                    
            print("-" * 40)

            if self.health <= 0:
                print("\n*** You were defeated in combat... ***")
                self.is_alive = False
                write_log(f"{self.species} died in a duel.")
                return False

def write_log(msg):
    try:
        with open("log.txt", "a") as file:
            file.write(msg + "\n")
    except Exception as e:
        pass 

def read_log():
    try:
        with open("log.txt", "r") as file:
            print("\n--- Activity Log ---")
            print(file.read())
    except FileNotFoundError:
        print("\nNo log found. Do some activities first!")

def save_game(bird):
    try:
        with open("save.txt", "w") as file:
            file.write(f"{bird.species},{bird.speed},{bird.weight},{bird.strength},{bird.energy},{bird.health}")
        print("\nGame saved successfully!")
    except Exception as e:
        print("\nError saving the game.")

def load_game():
    try:
        with open("save.txt", "r") as file:
            data = file.readline().strip().split(',')
            print(f"\nSuccessfully loaded game for: {data[0]}")
            return Bird(data[0], int(data[1]), int(data[2]), int(data[3]), int(data[4]), int(data[5]))
    except FileNotFoundError:
        print("\nNo save file found.")
        return None

def main():
    print("========================================")
    print("      BIRDS OF PREY SIMULATOR           ")
    print("========================================")
    
    print("\nWelcome to the skies!")
    print("In this game, you will take control of an apex predator.")
    print("Your goal is to survive by hunting prey, which costs energy.")
    print("If your energy gets low, you must rest and feed to recover.")
    print("Beware of random weather events while hunting!")
    print("When you feel strong enough, challenge a rival bird to a")
    print("turn-based duel to defend your territory.")
    print("========================================\n")
    
    player_bird = None
    
    load_choice = input("Load saved game? (Y/N): ")
    if load_choice.upper() == 'Y':
        player_bird = load_game()
        
    if player_bird == None:
        print("\n1. Wedge-tailed Eagle (Speed: 6, Weight: 8, Strength: 9)")
        print("2. Peregrine Falcon   (Speed: 10, Weight: 4, Strength: 5)")
        print("3. Brown Goshawk      (Speed: 7, Weight: 6, Strength: 7)")
        
        valid_input = False
        while not valid_input:
            choice = input("Choose your bird (1/2/3): ")
            if choice == '1':
                player_bird = Bird("Wedge-tailed Eagle", 6, 8, 9)
                valid_input = True
            elif choice == '2':
                player_bird = Bird("Peregrine Falcon", 10, 4, 5)
                valid_input = True
            elif choice == '3':
                player_bird = Bird("Brown Goshawk", 7, 6, 7)
                valid_input = True
            else:
                print("Invalid choice, try again.")

        try:
            with open("log.txt", "w") as file:
                file.write(f"New Game Started: {player_bird.species}\n")
        except:
            pass

    stop_flag = False
    
    while not stop_flag and player_bird.is_alive:
        print("\n1. Hunt prey species")
        print("2. Train or feed")
        print("3. Review status of bird")
        print("4. Log of hunts")
        print("5. Duel with another bird")
        print("6. Save Game")
        print("7. Quit")
        
        action = input("Choose an activity (1-7): ")
        
        if action == '1':
            player_bird.hunt()
        elif action == '2':
            player_bird.train_or_feed()
        elif action == '3':
            print("\n" + str(player_bird))
        elif action == '4':
            read_log()
        elif action == '5':
            if player_bird.duel():
                if input("\nContinue playing? (Y/N): ").upper() == 'N':
                    stop_flag = True
            else:
                stop_flag = True
        elif action == '6':
            save_game(player_bird)
        elif action == '7':
            stop_flag = True
        else:
            print("Invalid input.")
            
        if not player_bird.is_alive and action != '5':
            print("\nYour bird has died. Game over.")
            stop_flag = True

if __name__ == "__main__":
    main()