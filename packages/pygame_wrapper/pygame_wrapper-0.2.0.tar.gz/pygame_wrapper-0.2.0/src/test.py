"""
Used for testing: game.py, menu.py, fonts.py, logging.py, and color.py
also btw I do more testing than this, its just that most of them wont work on other systems unlike this one.
(I do not test filesystem.py, use at your own risk.)
"""
from pygame_wrapper import GameType, MenuType, CustomColor, Font
from pygame_wrapper.logging import setupLogging
from pygame_wrapper.UI import Checkbox, Button
from logging import INFO, DEBUG
import pygame

logger = setupLogging("main", level=INFO)


class MainMenu(MenuType):
    def __init__(self, screen, fpsClock, font):
        super().__init__(screen, fpsClock)
        self.c = CustomColor((0, 255, 0))
        self.font: Font = font

    def logic(self):
        logger.debug("Menu Logic")

    def rendering(self):
        logger.debug("Menu Rendering")
        self.screen.fill(self.c)
        self.font.multiline_render_to(self.screen, (50, 50), "This is the main\nmenu")
        pygame.display.flip()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            self.logic()
            self.rendering()


class Game(GameType):
    def __init__(self):
        super().__init__("Testing Application", (1080, 720))
        self.c = CustomColor((255, 0, 0))
        self.font = Font("./ExtraLightFont.ttf", 40, CustomColor((50, 150, 25)))
        self.menus = [MainMenu(self.screen, self.fpsClock, self.font)]
        self.button = Button(300, 300, 200, 50, (150, 150, 150), (100, 100, 100), self.font, "button")
        self.checkBox = Checkbox(300, 600, 50, 50, (150, 150, 150), (0, 255, 255))
        self.needsHook = [self.button, self.checkBox]

    def logic(self):
        logger.debug("Logic")

    def rendering(self):
        logger.debug("Rendering")
        self.screen.fill(self.c)
        self.font.multiline_render_to(self.screen, (100, 100), "This is the game\n thing")
        self.button.render_to(self.screen)
        self.checkBox.render_to(self.screen)
        pygame.display.flip()

    def run(self):
        while True:
            events = pygame.event.get()
            for hookable in self.needsHook:
                hookable.hook_events(events)
            for event in events:
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    logger.info(f"Key pressed: {pygame.key.name(event.key)}")
                    if event.key == pygame.K_a:
                        self.router(0).run()
            self.logic()
            self.rendering()

    def router(self, case) -> MenuType:
        return self.menus[case]


def checkForFont():
    from pathlib import Path
    import urllib.request

    if not Path('./ExtraLightFont.ttf').is_file():
        # this means that the font file isnt downloaded, dont worry! we will download it for you
        logger.info(f"Missing ExtraLightFont.ttf, downloading...")
        # this probably leaked my api token but i dont care
        fonturl = 'http://fonts.gstatic.com/s/bricolagegrotesque/v1/3y9U6as8bTXq_nANBjzKo3IeZx8z6up5BeSl5jBNz_19PpbpMXuECpwUxJBOm_OJWiaaD30YfKfjZZoLvZviyM0vs-wJDtw.ttf'
        try:
            with urllib.request.urlopen(fonturl) as response:
                body = response.read()
                with open(Path('./ExtraLightFont.ttf'), 'wb') as ff:
                    ff.write(body)
        except Exception as e:
            logger.error("Unable to download font file, raising exception.")
            raise e


def main():
    checkForFont()
    pygame.init()
    g = Game()
    g.run()


if __name__ == "__main__":
    main()
    logger.debug("LEVEL TESTING")
    logger.info("Yeah im testing levels")
    logger.warning("This is a warning bro")
    logger.error("We gonna have an error")
    logger.critical("We are going critical")
