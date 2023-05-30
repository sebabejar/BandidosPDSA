import pygame

import numpy as np
from tensorflow.python.keras import models

from recording_helper import record_audio, terminate
from tf_helper import preprocess_audiobuffer

commands = ['calle', 'arbol', 'ventana', 'puerta', 'siguiente']

loaded_model = models.load_model("modelo_76.h5", compile=False)

def predict_mic():
    audio = record_audio()
    spec = preprocess_audiobuffer(audio)
    prediction = loaded_model(spec)
    label_pred = np.argmax(prediction, axis=1)
    command = commands[label_pred[0]]
    print("Predicted label:", command)
    return command

if __name__ == "__main__":
    while True:
        command = predict_mic()
        if command == 'siguiente':
            terminate()
            break

from models import Bandido, Spaceship
from utils import  load_sprite, print_text
from pygame.math import Vector2


class Bandidos:

    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((800, 800))
        self.background = load_sprite("Bg", False)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 64)
        self.message = ""

        self.bandidos = []
        self.bullets = []
        self.spaceship = Spaceship((400, 720), self.bullets.append)

        positions = [(160, 600), (280, 562), (550, 500), (700, 500)]

        for i in range(4):
            position = Vector2(positions[i])
            self.bandidos.append(Bandido(position, self.bandidos.append))

    def main_loop(self):
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Space Rocks")

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                quit()
            elif (
                self.spaceship
                and event.type == pygame.KEYDOWN
                and event.key == pygame.K_SPACE
            ):
                self.spaceship.shoot()

        is_key_pressed = pygame.key.get_pressed()

        if self.spaceship:
            if is_key_pressed[pygame.K_q]:
                self.spaceship.rotate1(position=1)
                self.spaceship.shoot()
            elif is_key_pressed[pygame.K_w]:
                self.spaceship.rotate1(position=2)
                self.spaceship.shoot()
            elif is_key_pressed[pygame.K_e]:
                self.spaceship.rotate1(position=3)
                self.spaceship.shoot()
            elif is_key_pressed[pygame.K_r]:
                self.spaceship.rotate1(position=4)
                self.spaceship.shoot()
            elif is_key_pressed[pygame.K_p]:
                self.message = self.bandidos.len()

    def _process_game_logic(self):
        for game_object in self._get_game_objects():
            game_object.move(self.screen)

        for bullet in self.bullets[:]:
            for asteroid in self.bandidos[:]:
                if asteroid.collides_with(bullet):
                    self.bandidos.remove(asteroid)
                    self.bullets.remove(bullet)
                    break

        for bullet in self.bullets[:]:
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)

        if not self.bandidos and self.spaceship:
            self.message = "You won!"
    

    def _draw(self):
        self.screen.blit(self.background, (0, 0))

        for game_object in self._get_game_objects():
            game_object.draw(self.screen)

        if self.message:
            print_text(self.screen, self.message, self.font)

        pygame.display.flip()
        self.clock.tick(60)

    def _get_game_objects(self):
        game_objects = [*self.bandidos, *self.bullets]

        if self.spaceship:
            game_objects.append(self.spaceship)

        return game_objects
