import random

# Slot machine configuration
REEL_ITEMS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
REEL_COUNT = 3
LINES_COUNT = 3
WIN_MULTIPLIER = {
    'A': 5,
    'B': 4,
    'C': 3,
    'D': 2,
    'E': 2,
    'F': 1,
    'G': 1
}

# Function to spin the slot machine
def spin_reels():
    return [[random.choice(REEL_ITEMS) for _ in range(REEL_COUNT)] for _ in range(LINES_COUNT)]

# Function to display the slot machine
def display_slot_machine(reels):
    for line in reels:
        print(' | '.join(line))

# Function to check for wins
def check_wins(reels, bet_lines):
    winnings = 0
    for line in range(bet_lines):
        if all(item == reels[line][0] for item in reels[line]):
            winnings += WIN_MULTIPLIER[reels[line][0]]
    return winnings

# Function to get user's deposit
def get_deposit():
    while True:
        try:
            deposit = float(input("Enter your deposit amount: $"))
            if deposit > 0:
                return deposit
            else:
                print("Deposit amount must be greater than zero.")
        except ValueError:
            print("Invalid input. Please enter a number.")

# Function to get user's bet
def get_bet(balance):
    while True:
        try:
            bet = float(input(f"Enter your bet amount (Current balance: ${balance}): $"))
            if 0 < bet <= balance:
                return bet
            else:
                print("Bet amount must be greater than zero and less than or equal to your balance.")
        except ValueError:
            print("Invalid input. Please enter a number.")

# Function to get number of lines to bet on
def get_bet_lines():
    while True:
        try:
            lines = int(input(f"Enter number of lines to bet on (1-{LINES_COUNT}): "))
            if 1 <= lines <= LINES_COUNT:
                return lines
            else:
                print(f"Number of lines must be between 1 and {LINES_COUNT}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

# Main game function
def slot_machine_game():
    print("Welcome to the Slot Machine!")
    
    balance = get_deposit()
    
    while True:
        bet = get_bet(balance)
        bet_lines = get_bet_lines()
        
        print("\nSpinning the reels...\n")
        reels = spin_reels()
        display_slot_machine(reels)
        
        winnings = check_wins(reels, bet_lines)
        total_winnings = bet * winnings
        
        if winnings > 0:
            print(f"\nCongratulations! You won ${total_winnings:.2f}.")
        else:
            print("\nSorry, no wins this time.")
        
        balance -= bet
        balance += total_winnings
        
        print(f"Your new balance is: ${balance:.2f}")
        
        if balance <= 0:
            print("\nYou have run out of money. Game over!")
            break
        
        play_again = input("Do you want to play again? (y/n): ").lower()
        if play_again != 'y':
            print(f"You cashed out with ${balance:.2f}. Thank you for playing!")
            break

if __name__ == "__main__":
    slot_machine_game()
