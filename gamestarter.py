import subprocess
import os

def flappyHusein():
    script_path = os.path.join(os.getcwd(), "games", "flappybird", "flappy.py")
    subprocess.run(["python", script_path], cwd=os.path.dirname(script_path))

def dino():
    script_path = os.path.join(os.getcwd(), "games","flappybird", "dino", "dino.py")
    subprocess.run(["python", script_path], cwd=os.path.dirname(script_path))
