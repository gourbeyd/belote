 # A server program which accepts requests from clients to capitalize strings. When
 # clients connect, a new thread is started to handle a client. The receiving of the
 # client data, the capitalizing, and the sending back of the data is handled on the
 # worker thread, allowing much greater throughput because more clients can be handled
 # concurrently.
import belote
import socketserver
import threading
import socket

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True

class PlayerHandler(socketserver.StreamRequestHandler):
    def handle(self):
        client = f'{self.client_address} on {threading.currentThread().getName()}'
        print(f'Connected: {client}')
        joueur = None
        if joueur is None:
            data = self.rfile.readline()
            joueur = int(data)
            print(joueur)
        self.id = joueur
        try:
            self.initialize()
            self.process_commands()
        except Exception as e:
            print(e)
        print(f'Closed: {client}')

    def send(self, message):
        self.wfile.write(f'{message}\n'.encode('utf-8'))

    def initialize(self):
        Game.join(self)
        self.send('salut joueur ' + str(self.id))
    def process_commands(self):
        while True:
            command = self.rfile.readline()
            if not command:
                break
            command = command.decode('utf-8')
            if command.startswith("show hand"):
                self.show_hand()
            elif command.startswith("show totake"):
                self.show_totake()
            elif command.startswith("take yes"):
                self.game.takes(self, True)
            elif command.startswith("take no"):
                self.game.takes(self, False)
            elif command.startswith("take coeur"):
                self.game.takes(self, True, "coeur")
            elif command.startswith("take pique"):
                self.game.takes(self, True, "pique")
            elif command.startswith("take trefle"):
                self.game.takes(self, True, "trefle")
            elif command.startswith("take carreau"):
                self.game.takes(self, True, "carreau")
            elif command.startswith("play "):
                indicecarte = int(command[5])
                self.game.plays(self, indicecarte)
            elif command.startswith("show tapis"):
                self.show_tapis()
            elif command.startswith("show points"):
                self.show_points()
            elif command.startswith("show tour"):
                self.show_tour()
            else:
                self.show_wrongcommand()
    def show_tour(self):
        toplay ="J"+ str(self.game.current_player) +"\n"
        self.wfile.write(toplay.encode('utf-8'))

    def show_points(self):
        points_tour = self.game.points_tour
        points_overall = self.game.points_overall
        message = str(points_tour) + "\n" +str(points_overall)+"\n"
        self.wfile.write(message.encode('utf-8'))
    def show_wrongcommand(self):
        message = "Unknown command \n"
        self.wfile.write(message.encode('utf-8'))
    def show_tapis(self):
        tapisstr = "\n"
        for carte in self.game.tapis:
            tapisstr += str(carte.proprietaire)+str(carte)+"\n"
        self.wfile.write(tapisstr.encode('utf-8'))

    def show_totake(self):
        totake = self.game.to_be_taken
        self.wfile.write((str(totake)).encode('utf-8'))
    def show_hand(self):
        hand = ""
        for carte in self.game.mains[self.id]:
            hand += str(carte)+"\n"
        if hand == "":
            hand  = "vide \n"
        self.wfile.write(hand.encode('utf-8'))

class Game:
    next_game = None
    game_selection_lock = threading.Lock()
    def __init__(self):
        self.deck = belote.creer_deck()
        self.distributeur = 3
        self.mains = [[] for k in range(4)]
        self.to_be_taken = belote.debut_distrib(self.deck, self.mains, self.distributeur)
        self.current_player = (self.distributeur+1)%4
        self.tapis = []
        self.preneur= None
        self.der = False
        self.points_overall = [0, 0]
        self.points_tour = [0, 0]

    def plays(self, player, indicecarte):
        if player.id == self.current_player:
            if len(self.tapis)<4:
                self.tapis.append(self.mains[player.id].pop(indicecarte))
                player.send("you played, next")
                self.current_player = (self.current_player+1)%4
            if len(self.tapis) == 4:
                (self.current_player, pts_pli) = belote.vainqueur_pli(self.tapis, self.der)
                self.points_tour = [self.points_tour[0]+pts_pli[0], self.points_tour[1]+pts_pli[1]]
                for carte in self.tapis:
                    self.deck.append(carte)
                self.tapis = []
                if len(self.mains[0])==1:
                    self.der = True
                if self.mains == [[], [], [], []]:
                    self.distributeur = (self.distributeur+1)%4
                    self.current_player = (self.distributeur+1)%4
                    self.der = False
                    self.to_be_taken = belote.debut_distrib(self.deck, self.mains, self.distributeur)
                    if self.preneur%2 == 0:#lequipe 0,2 a pris
                        if self.points_tour[0] > 80:
                            self.points_overall = [self.points_overall[0]+self.points_tour[0], self.points_overall[1]+self.points_tour[1]]
                        else:
                            self.points_overall = [self.points_overall[0], self.points_overall[1]+162]
                    else:
                        if self.points_tour[1] > 80:
                            self.points_overall = [self.points_overall[0]+self.points_tour[0], self.points_overall[1]+self.points_tour[1]]
                        else:
                            self.points_overall = [self.points_overall[0] + 162, self.points_overall[1]]

                    self.points_tour = [0, 0]
        else:
            player.send("not your turn to play")

    def takes(self, player, prend, color=None):
        if not color:
            color = self.to_be_taken.couleur
        if player.id == self.current_player:
            if prend:
                belote.fin_distrib(self.deck, self.mains, player.id, self.to_be_taken, self.distributeur, color)
                player.send("well done, you took  "+str(color))
                self.current_player = (self.distributeur+1)%4
                self.preneur = player.id
            else:
                self.current_player = (self.current_player+1)%4
                player.send("you didn't take")
        else:
            player.send("not your turn to speak")


    @classmethod
    def join(cls, player):
        with cls.game_selection_lock:
            if cls.next_game is None:
                cls.next_game = Game()
                player.game = cls.next_game
            else:
                player.game = cls.next_game

with ThreadedTCPServer(('', 58989), PlayerHandler) as server:
    print(f'belote server is running...')
    print(socket.gethostbyname(socket.gethostname()))
    server.serve_forever()
