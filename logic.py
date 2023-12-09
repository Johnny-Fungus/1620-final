from PyQt6.QtWidgets import *
from gui import *
import random as ran
import csv


class Logic(QMainWindow, Ui_Form):
    """
    This class holds the logic for the application
    :param QMainWindow: main window class
    :param Ui_Form: UI_Form class containing gui for application
    """

    def __init__(self):
        """
        This function sets the default values of the Logic class
        """
        super().__init__()
        self.setupUi(self)
        self.startButton.clicked.connect(lambda: self.startgame())
        self.mainMenuButton.clicked.connect(lambda: self.endgame())

        self.__player1 = {"name": "Mr. Toe", "symbol": "O", "points": 0, "id": "1"}
        self.__player2 = {"name": "Mrs. Tac", "symbol": "X", "points": 0, "id": "2"}

        self.__currentplayer = {}
        self.__gamecount = 0
        self.__whowon = ""

        with open("saves.csv", "a", newline="") as outfile:
            writer = csv.writer(outfile)
            header = ["game_number", "game_point", "who_won", "player1_name", "player2_name", "player1_points",
                      "player2_points"]
            writer.writerow(header)

        self.gbutton00.clicked.connect(lambda: self.game_event("00"))
        self.gbutton01.clicked.connect(lambda: self.game_event("01"))
        self.gbutton02.clicked.connect(lambda: self.game_event("02"))
        self.gbutton10.clicked.connect(lambda: self.game_event("10"))
        self.gbutton11.clicked.connect(lambda: self.game_event("11"))
        self.gbutton12.clicked.connect(lambda: self.game_event("12"))
        self.gbutton20.clicked.connect(lambda: self.game_event("20"))
        self.gbutton21.clicked.connect(lambda: self.game_event("21"))
        self.gbutton22.clicked.connect(lambda: self.game_event("22"))

        self.player1readout.setText(f'{self.__player1["name"]}\n{self.__player1["symbol"]}\n{self.__player1["points"]}')
        self.player2readout.setText(f'{self.__player2["name"]}\n{self.__player2["symbol"]}\n{self.__player2["points"]}')

        self.stackedWidget.setCurrentWidget(self.page)

    def startgame(self):
        """
        This function sets up variables used in the game, displays the game page, and sets the readouts for each player
        """
        if self.lineEdit.text() != "":
            self.__player1["name"] = self.lineEdit.text()

        if self.lineEdit_2.text() != "":
            self.__player2["name"] = self.lineEdit_2.text()

        self.__gamecount += 1
        self.__whowon = "no winners"
        self.__gamepoint = self.gp_selector.value()
        self.player1readout.setText(f'{self.__player1["name"]}\n{self.__player1["symbol"]}\n{self.__player1["points"]}')
        self.player2readout.setText(f'{self.__player2["name"]}\n{self.__player2["symbol"]}\n{self.__player2["points"]}')
        self.stackedWidget.setCurrentWidget(self.page_2)

        random = ran.randint(0, 1)
        if random == 0:
            self.__currentplayer = self.__player1
        else:
            self.__currentplayer = self.__player2

        self.gamereadout.setText(f"{self.__currentplayer["name"]} goes first!")

    def endgame(self):
        """
        This function resets game variables at the end of the game and handles setting the scoreboard
        """
        with open("saves.csv", "a", newline="") as outfile:
            writer = csv.writer(outfile)
            writer.writerow([self.__gamecount, self.__gamepoint, self.__whowon,
                             self.__player1["name"], self.__player2["name"],
                             self.__player1["points"], self.__player2["points"]])

        self.resetbuttons()
        self.__player1["points"] = 0
        self.__player2["points"] = 0

        with open("saves.csv", "r") as infile:
            reader = csv.reader(infile)
            scoreboard_text = ""
            for line in reader:
                for element in line:
                    scoreboard_text += f"{element} "
                scoreboard_text += "\n"
            print(scoreboard_text)
            self.scoreboard.setText(scoreboard_text)

        self.gp_selector.setValue(0)
        self.stackedWidget.setCurrentWidget(self.page)

    def game_event(self, identifier: str):
        """
        This function sets the text of and disables buttons that have been pressed, it also switches the current player

        :param identifier: This is a string that identifies a button in the tic-tac-toe grid
        """
        self.getbutton(identifier).setText(self.__currentplayer["symbol"])
        self.getbutton(identifier).setEnabled(False)
        self.checkwin()

        if self.__currentplayer["id"] == "1":
            self.__currentplayer = self.__player2
        else:
            self.__currentplayer = self.__player1

    def getbutton(self, identifier: str):
        """
        This function returns the button object associated with an identifier

        :param identifier: This is a string that identifies a button in the tic-tac-toe grid
        :return: The button object that is associated with the identifier
        """
        if identifier == "00":
            return self.gbutton00
        elif identifier == "01":
            return self.gbutton01
        elif identifier == "02":
            return self.gbutton02
        elif identifier == "10":
            return self.gbutton10
        elif identifier == "11":
            return self.gbutton11
        elif identifier == "12":
            return self.gbutton12
        elif identifier == "20":
            return self.gbutton20
        elif identifier == "21":
            return self.gbutton21
        elif identifier == "22":
            return self.gbutton22

    def checkwin(self):
        """
        This is a function that checks the grid for matches. It also handles match, win, and scratch game conditions and updates readouts accordingly
        """
        match = False
        if (self.gbutton00.text() == self.gbutton01.text() and self.gbutton01.text() == self.gbutton02.text() and self.gbutton00.text() != ''
                or self.gbutton10.text() == self.gbutton11.text() and self.gbutton11.text() == self.gbutton12.text() and self.gbutton10.text() != ''
                or self.gbutton20.text() == self.gbutton21.text() and self.gbutton21.text() == self.gbutton22.text() and self.gbutton20.text() != ''
                or self.gbutton00.text() == self.gbutton10.text() and self.gbutton10.text() == self.gbutton20.text() and self.gbutton00.text() != ''
                or self.gbutton01.text() == self.gbutton11.text() and self.gbutton11.text() == self.gbutton21.text() and self.gbutton01.text() != ''
                or self.gbutton02.text() == self.gbutton12.text() and self.gbutton12.text() == self.gbutton22.text() and self.gbutton02.text() != ''
                or self.gbutton00.text() == self.gbutton11.text() and self.gbutton11.text() == self.gbutton22.text() and self.gbutton00.text() != ''
                or self.gbutton20.text() == self.gbutton11.text() and self.gbutton11.text() == self.gbutton02.text() and self.gbutton20.text() != ''):
            match = True

        if (self.gbutton00 != ''
                and self.gbutton01.text() != ''
                and self.gbutton02.text() != ''
                and self.gbutton10.text() != ''
                and self.gbutton11.text() != ''
                and self.gbutton12.text() != ''
                and self.gbutton20.text() != ''
                and self.gbutton21.text() != ''
                and self.gbutton22.text() != ''
                and match == False):
            self.resetbuttons()
            self.gamereadout.setText(f'Scratch Game')

        if match:
            self.gamereadout.setText(f'{self.__currentplayer["name"]} ({self.__currentplayer["symbol"]}) got a match!')
            self.__currentplayer["points"] += 1

            if self.__currentplayer["id"] == "1":
                self.player1readout.setText(f'{self.__currentplayer["name"]}\n{self.__currentplayer["symbol"]}\n{self.__currentplayer["points"]}')
            else:
                self.player2readout.setText(f'{self.__currentplayer["name"]}\n{self.__currentplayer["symbol"]}\n{self.__currentplayer["points"]}')

            if self.__currentplayer["points"] >= self.__gamepoint:
                self.gamereadout.setText(f"End of Game\n{self.__currentplayer["name"]} wins")
                self.__whowon = self.__currentplayer["name"]
                self.disablebuttons()
            else:
                self.resetbuttons()

    def closeEvent(self, QCloseEvent=None):
        """
        This function clears the saves file when the application is closed

        :param QCloseEvent: the close event object that is created when the x button is clicked
        """
        try:
            file = open("saves.csv", "w")
            file.close()
        except FileNotFoundError:
            pass

    def disablebuttons(self):
        """
        This function disables all buttons
        """
        self.gbutton00.setEnabled(False)
        self.gbutton01.setEnabled(False)
        self.gbutton02.setEnabled(False)
        self.gbutton10.setEnabled(False)
        self.gbutton11.setEnabled(False)
        self.gbutton12.setEnabled(False)
        self.gbutton20.setEnabled(False)
        self.gbutton21.setEnabled(False)
        self.gbutton22.setEnabled(False)

    def enablebuttons(self):
        """
        This function enables all buttons
        """
        self.gbutton00.setEnabled(True)
        self.gbutton01.setEnabled(True)
        self.gbutton02.setEnabled(True)
        self.gbutton10.setEnabled(True)
        self.gbutton11.setEnabled(True)
        self.gbutton12.setEnabled(True)
        self.gbutton20.setEnabled(True)
        self.gbutton21.setEnabled(True)
        self.gbutton22.setEnabled(True)

    def resetbuttons(self):
        """
        This function enables all buttons and clears their text
        """
        self.gbutton00.setEnabled(True)
        self.gbutton01.setEnabled(True)
        self.gbutton02.setEnabled(True)
        self.gbutton10.setEnabled(True)
        self.gbutton11.setEnabled(True)
        self.gbutton12.setEnabled(True)
        self.gbutton20.setEnabled(True)
        self.gbutton21.setEnabled(True)
        self.gbutton22.setEnabled(True)

        self.gbutton00.setText("")
        self.gbutton01.setText("")
        self.gbutton02.setText("")
        self.gbutton10.setText("")
        self.gbutton11.setText("")
        self.gbutton12.setText("")
        self.gbutton20.setText("")
        self.gbutton21.setText("")
        self.gbutton22.setText("")





