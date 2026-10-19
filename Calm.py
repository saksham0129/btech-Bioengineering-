#!/usr/bin/env python3
"""
Calm.py — simple terminal mindfulness helper

Features:
- Show a centered inspirational quote
- Guided breathing cycle (default 4-4-6) with countdown
- Configurable rounds and durations
- Simple interactive menu
"""
import os
import sys
import time
import random
import shutil
import signal
from textwrap import fill

QUOTES = [
    "You have power over your mind — not outside events. Realize this, and you will find strength. — Marcus Aurelius",
    "Breath is the bridge which connects life to consciousness. — Thich Nhat Hanh",
    "The mind is like water. When it's turbulent, it's difficult to see. When it's calm, everything becomes clear.",
    "Within you, there is a stillness and a sanctuary to which you can retreat at any time and be yourself."
]

def handle_sigint(signum, frame):
    print("\n\nExiting calmly. Take care.")
    sys.exit(0)

signal.signal(signal.SIGINT, handle_sigint)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def term_width():
    try:
        return shutil.get_terminal_size().columns
    except Exception:
        return 80

def center_print(text, pad_top=0, pad_bottom=0):
    width = term_width()
    lines = str(text).splitlines()
    for _ in range(pad_top):
        print()
    for line in lines:
        print(line.center(width))
    for _ in range(pad_bottom):
        print()

def show_quote():
    clear_screen()
    quote = random.choice(QUOTES)
    # wrap the quote to a readable width and center
    wrapped = fill(quote, width=min(70, term_width()-10))
    center_print(wrapped, pad_top=2, pad_bottom=2)
    input("\nPress Enter to return to menu...")

def countdown(duration, label=""):
    width = term_width()
    for i in range(duration, 0, -1):
        bar = f"{label} {i}s"
        # place the countdown roughly centered
        sys.stdout.write("\r" + bar.center(width))
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\r" + " " * width + "\r")
    sys.stdout.flush()

def breathing_cycle(inhale=4, hold=4, exhale=6, rounds=4):
    clear_screen()
    center_print("Guided Breathing", pad_top=1, pad_bottom=1)
    center_print(f"Pattern: inhale {inhale}s — hold {hold}s — exhale {exhale}s", pad_bottom=1)
    center_print(f"Rounds: {rounds}", pad_bottom=2)
    time.sleep(1)

    try:
        for r in range(1, rounds+1):
            center_print(f"Round {r}/{rounds}", pad_bottom=1)
            # Inhale
            center_print("Inhale...", pad_bottom=0)
            countdown(inhale, label="Inhale")
            # Hold
            center_print("Hold...", pad_bottom=0)
            countdown(hold, label="Hold")
            # Exhale
            center_print("Exhale...", pad_bottom=0)
            countdown(exhale, label="Exhale")
            # small pause between rounds
            if r != rounds:
                center_print("Relax for 3 seconds...", pad_bottom=0)
                countdown(3, label="Rest")
                clear_screen()
        center_print("Well done. Take a moment to notice how you feel.", pad_top=1, pad_bottom=2)
        input("Press Enter to return to menu...")
    except KeyboardInterrupt:
        print("\nInterrupted. Returning to menu...")
        time.sleep(0.5)

def get_positive_int(prompt, default):
    try:
        val = input(f"{prompt} [{default}]: ").strip()
        return int(val) if val else default
    except Exception:
        print("Invalid input, using default.")
        return default

def main_menu():
    while True:
        clear_screen()
        center_print("Welcome to Calm.", pad_top=1, pad_bottom=1)
        print("1) Guided breathing (default 4-4-6)")
        print("2) Show a calming quote")
        print("3) Guided breathing (customize durations/rounds)")
        print("4) Exit")
        choice = input("\nChoose an option (1-4): ").strip()
        if choice == "1":
            breathing_cycle()
        elif choice == "2":
            show_quote()
        elif choice == "3":
            inhale = get_positive_int("Inhale seconds", 4)
            hold = get_positive_int("Hold seconds", 4)
            exhale = get_positive_int("Exhale seconds", 6)
            rounds = get_positive_int("Rounds", 4)
            breathing_cycle(inhale=inhale, hold=hold, exhale=exhale, rounds=rounds)
        elif choice == "4":
            clear_screen()
            center_print("Goodbye — be well.", pad_top=2, pad_bottom=1)
            break
        else:
            print("Invalid choice. Try again.")
            time.sleep(1)

if __name__ == "__main__":
    main_menu()
