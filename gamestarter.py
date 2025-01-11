import subprocess
import os

def flappyHusein():
    script_path = os.path.join(os.getcwd(), "games", "flappybird", "flappy.py")
    subprocess.run(["python", script_path], cwd=os.path.dirname(script_path))

def dino():
    script_path = os.path.join(os.getcwd(), "games", "dino", "dino.py")
    subprocess.run(["python", script_path], cwd=os.path.dirname(script_path))

def mushroom():
    script_path = os.path.join(os.getcwd(), "games", "mushroom", "mantar.py")
    subprocess.run(["python", script_path], cwd=os.path.dirname(script_path))

def snake():
    script_path = os.path.join(os.getcwd(), "games", "snake", "snake.py")
    subprocess.run(["python", script_path], cwd=os.path.dirname(script_path))

def tetris():
    script_path = os.path.join(os.getcwd(), "games", "tetris", "game.py")
    subprocess.run(["python", script_path], cwd=os.path.dirname(script_path))

def ikdört():
    script_path = os.path.join(os.getcwd(), "games", "2048", "2048.py")
    subprocess.run(["python", script_path], cwd=os.path.dirname(script_path))