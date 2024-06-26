#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import re
import sys
from abc import ABC, abstractmethod
from random import randint, randrange

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

class MyMath(ABC):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    @abstractmethod
    def operation(self, a, b):
        pass

class add(MyMath):
    def operation(self, a, b):
        return a+b

class subtract(MyMath):
    def operation(self, a, b):
        return a-b

class divide(MyMath):
    def operation(self, a, b):
        result = a/b

        if result.is_integer():
            formatted_result = int(result)
        else:
            formatted_result = round(result, 2)

        return formatted_result

class multiply(MyMath):
    def operation(self, a, b):
        return a*b

def selectInput():
    selection = input("\nSelect number for operation: \n 1. Add\n 2. Subtract\n 3. Divide\n 4. Multiply\n> ")
    return selection

def playAgain():
    decision = input("\nWould you like to play again? ([yes]/no): ")

    return decision.lower() in ["yes", "y"]

def correctAns():
    print("\nCongratulations! The LED is clapping for you!\n")
    t_end = time.time() + 5
    while time.time() < t_end:
        GPIO.output(18, True)
        time.sleep(.25)
        GPIO.output(18, False)
        time.sleep(.25)

if __name__ == "__main__":
    while True:
        selection = selectInput()
        a = randint(10,99)
        b = randint(10,99)
        options = {
            "1": "add",
            "2": "subtract",
            "3": "divide",
            "4": "multiply"
        }

        while True:
            try:
                command = (eval(options[selection]))(a, b)
                break
            except KeyError:
                print("\nPlease select a number from the list. Try again.\n")
                selection = selectInput()

        value = command.operation(a,b)

        for count in range(3, -1, -1):
            ans = input(f"\nThe numbers randomly generated are {a} and {b}. You have chosen to {options[selection]}. What is the answer? ")

            if ans == str(value):
                correctAns()
                break
            else:
                print(f"\nWrong answer! You have {count} more tries. Please enter your answer: ")
        else:
            print("\nYou have exceeded the number of tries. Game Over!")

        if not playAgain():
            print("\nThanks for playing, goodbye!")
            break
