import sys
import socket
from tkinter import *
"""
if len(sys.argv) != 3:
    print('Pass the server IP / player number as command line arguments')
else:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((sys.argv[1], 59898))
        sock.sendall(sys.argv[2].encode('utf-8'))
        while True:
            line = sys.stdin.readline()
            if not line:
                # End of standard input, exit this entire script
                break
            sock.sendall(f'{line}'.encode('utf-8'))
            while True:
                data = sock.recv(128)
                print(data.decode("utf-8"), end='\n')
                if len(data) < 128:
                    # No more of this message, go back to waiting for next message
                    break
"""


class Application(Tk):
    def chat(self, event):
        """Evenement clavier"""
        msgClient =self.msgClient
        self.sock.send(msgClient.get().encode("Utf8"))
        self.frome()
    def connection(self):
        self.sock.connect(("127.0.1.1", 58989))
        print("you are successfullt connected")
    """Interface graphique"""
    def enter_player(self):
        self.sock.send((self.num_joueur.get()+'\n').encode('utf-8'))
        self.frome()
        self.draw_tourne()
        self.refresh()


    def enter_command(self):
        self.sock.send((self.command.get()+'\n').encode('utf-8'))

    def __init__(self,):
        self.main = None
        self.sock =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Tk.__init__(self,)
        self.title("Client Belote")
        self.connection()
        #Entry num joeur
        self.num_joueur = StringVar()
        self.ent =Entry(self, width =12, selectbackground ="royal blue",textvariable =self.num_joueur)
        self.ent.grid(padx =1, pady =2)
        self.bouton_player = Button(self, text = "Entrer", command= self.enter_player)
        self.bouton_player.grid(column = '1', row ='0')
        #entry command
        self.but_take = Button(self, text = "Prendre", command = self.take)
        self.but_take.grid(column = '1', row = '8')
        self.but_passe = Button(self, text = "Passer", command = self.passe)
        self.but_passe.grid(column ='0', row='7')
        #on dessine main
        self.draw_tourne(hidden= True)
        self.draw_tapis()
        self.draw_hand()
        self.but_play0 = Button(self, text = "Play 0", command = self.play0)
        self.but_play0.grid(column = '2', row = '7')
        self.but_play1 = Button(self, text = "Play 1", command = self.play1)
        self.but_play1.grid(column = '3', row = '7')
        self.but_play2 = Button(self, text = "Play 2", command = self.play2)
        self.but_play2.grid(column = '4', row = '7')
        self.but_play3 = Button(self, text = "Play 3", command = self.play3)
        self.but_play3.grid(column = '5', row = '7')
        self.but_play4 = Button(self, text = "Play 4", command = self.play4)
        self.but_play4.grid(column = '6', row = '7')
        self.but_play5 = Button(self, text = "Play 5", command = self.play5)
        self.but_play5.grid(column = '7', row = '7')
        self.but_play6 = Button(self, text = "Play 6", command = self.play6)
        self.but_play6.grid(column = '8', row = '7')
        self.but_play7 = Button(self, text = "Play 7", command = self.play7)
        self.but_play7.grid(column = '9', row = '7')
        self.annonce_points_tour = Label(self, text='Points du tour:').grid(column = '7', row='0')
        self.annonce_points_totaux = Label(self, text='Points totaux:').grid(column = '9', row='0')
        self.points_totaux = Label(self, text ='[0, 0]')
        self.points_totaux.grid(column='9', row ='1')
        self.points_tour = Label(self,text='[0, 0]')
        self.points_tour.grid(column = '7', row = '1')
        self.aquiletour= Label(self, text="A qui le tour ?").grid(column='5', row= '0')
        self.tour_de = Label(self, text = "J0")
        self.tour_de.grid(column = '5', row= '1')
        self.color_taken = StringVar()
        self.entree_couleur = Entry(self,width = 5, textvariable= self.color_taken)
        self.entree_couleur.grid(column ='1', row='7')
    def play0(self):
        self.sock.send(("play 0\n").encode('utf-8'))
        self.frome()
    def play1(self):
        self.sock.send(("play 1\n").encode('utf-8'))
        self.frome()
    def play2(self):
        self.sock.send(("play 2\n").encode('utf-8'))
        self.frome()
    def play3(self):
        self.sock.send(("play 3\n").encode('utf-8'))
        self.frome()
    def play4(self):
        self.sock.send(("play 4\n").encode('utf-8'))
        self.frome()
    def play5(self):
        self.sock.send(("play 5\n").encode('utf-8'))
        self.frome()
    def play6(self):
        self.sock.send(("play 6\n").encode('utf-8'))
        self.frome()
    def play7(self):
        self.sock.send(("play 7\n").encode('utf-8'))
        self.frome()

    def passe(self):
        self.sock.send(("take no" + "\n").encode('utf-8'))
        self.frome()

    def take(self):
        self.color_taken = self.color_taken.get()
        if self.color_taken.startswith('trefle'):
            self.sock.send(("take trefle \n").encode('utf-8'))
        elif self.color_taken.startswith('pique'):
            self.sock.send(("take pique \n").encode('utf-8'))
        elif self.color_taken.startswith('coeur'):
            self.sock.send(("take coeur \n").encode('utf-8'))
        elif self.color_taken.startswith('carreau'):
            self.sock.send(("take carreau \n").encode('utf-8'))
        else:
            self.sock.send(("take yes"+"\n").encode('utf-8'))
        reponse = self.sock.recv(1024).decode('utf-8')
        if reponse.startswith("well"):
            self.show_hand()
        else:
            print(reponse)

    def draw_tourne(self, hidden = False):
        if not(hidden):
            self.sock.send(("show totake" +"\n").encode('utf-8'))
            self.totake = self.sock.recv(1024).decode('utf-8')
            card_name = "deck/"+self.totake+".png"
            self.img_totake = PhotoImage(file = card_name).subsample(8, 8)
            self.panel_totake.configure(image = self.img_totake)
            self.panel_totake.image = self.img_totake

        else:
            self.img_totake = PhotoImage(file = "deck/empty.png").subsample(8,8)
            self.panel_totake = Label(self, image = self.img_totake)
            self.panel_totake.grid(column = '0', row = '8')
    def show_tour(self):
        self.sock.send(("show tour \n").encode('utf-8'))
        rep = self.sock.recv(1024).decode('utf-8')
        tour = rep.splitlines()
        self.tour_de.configure(text = tour[0])
        self.tour_de.text=tour[0]
    def draw_tapis(self):
        self.img_tapis = PhotoImage(file = "deck/empty.png").subsample(8,8)
        self.panel_j0 = Label(self, text = "J0")
        self.panel_j0.grid(column='1', row ='3')
        self.panel_tap0 = Label(self, image = self.img_tapis)
        self.panel_tap0.grid(column='2', row = '3')

        self.panel_j1 = Label(self, text="J1").grid(column='3', row ='5')
        self.panel_tap1 = Label(self, image = self.img_tapis)
        self.panel_tap1.grid(column='3', row = '4')
        self.panel_j2 = Label(self, text="J2").grid(column='5', row ='3')
        self.panel_tap2 = Label(self, image = self.img_tapis)
        self.panel_tap2.grid(column='4', row = '3')
        self.panel_j3 = Label(self, text="J3").grid(column='3', row ='1')

        self.panel_tap3 = Label(self, image = self.img_tapis)
        self.panel_tap3.grid(column='3', row = '2')

    def draw_hand(self, empty = True):
        self.img_vide = PhotoImage(file = "deck/empty.png").subsample(8,8)
        hand_row = 8
        self.panel1 = Label(self, image = self.img_vide)
        self.panel1.grid(column = '2', row=hand_row)
        self.panel2 = Label(self, image = self.img_vide)
        self.panel2.grid(column = '3', row=hand_row)
        self.panel3 = Label(self, image = self.img_vide)
        self.panel3.grid(column = '4', row=hand_row)
        self.panel4 = Label(self, image = self.img_vide)
        self.panel4.grid(column = '5', row=hand_row)
        self.panel5 = Label(self, image = self.img_vide)
        self.panel5.grid(column = '6', row=hand_row)
        self.panel6 = Label(self, image = self.img_vide)
        self.panel6.grid(column = '7', row=hand_row)
        self.panel7 = Label(self, image = self.img_vide)
        self.panel7.grid(column = '8', row=hand_row)
        self.panel8 = Label(self, image = self.img_vide)
        self.panel8.grid(column = '9', row=hand_row)

    def show_points(self):
        self.sock.send(("show points \n").encode('utf-8'))
        self.pointslong = self.sock.recv(1024).decode('utf-8')
        points = self.pointslong.splitlines()
        self.points_tour.configure(text = points[0])
        self.points_tour.text=points[0]
        self.points_totaux.configure(text = points[1])
        self.points_totaux.text=points[1]

    def show_hand(self):
        self.sock.send(("show hand"+'\n').encode('utf-8'))
        self.main = self.sock.recv(1024).decode('utf-8')
        hand = self.main.splitlines()
        if self.main.startswith("vide"):
            for k in range(1, 9):
                card_name = "deck/empty.png"
                self.img = PhotoImage(file = card_name).subsample(8, 8)
                exec("self.panel"+str(k)+".configure(image = self.img)")
                exec("self.panel"+str(k)+".image = self.img")

        else:
            for k in range(1, len(hand)+1):
                card_name = "deck/"+hand[k-1]+".png"
                self.img = PhotoImage(file = card_name).subsample(8, 8)
                exec("self.panel"+str(k)+".configure(image = self.img)")
                exec("self.panel"+str(k)+".image = self.img")
            if len(hand) < 8:
                for k in range(len(hand)+1, 9):
                    card_name = "deck/empty.png"
                    self.img = PhotoImage(file = card_name).subsample(8, 8)
                    exec("self.panel"+str(k)+".configure(image = self.img)")
                    exec("self.panel"+str(k)+".image = self.img")

    def show_tapis(self):
        self.sock.send(("show tapis\n").encode('utf-8'))
        self.tapis = self.sock.recv(1024).decode('utf-8')
        tapis_split = self.tapis.splitlines()
        for k in range(len(tapis_split)):
            card_code = tapis_split[k][1:]
            card_name = "deck/"+card_code+".png"
            if card_name != "deck/.png":
                card_prop = tapis_split[k][0]
                self.img = PhotoImage(file = card_name).subsample(8, 8)
                exec("self.panel_tap"+card_prop+".configure(image = self.img)")
                exec("self.panel_tap"+card_prop+".image = self.img")
            else:
                self.img = PhotoImage(file = "deck/empty.png").subsample(8, 8)
                exec("self.panel_tap"+str(k)+".configure(image = self.img)")
                exec("self.panel_tap"+str(k)+".image = self.img")
        if tapis_split == ['']:
            for k in range(4):
                self.img = PhotoImage(file = "deck/empty.png").subsample(8, 8)
                exec("self.panel_tap"+str(k)+".configure(image = self.img)")
                exec("self.panel_tap"+str(k)+".image = self.img")


    def frome(self):
        self.Msg_S =self.sock.recv(1024).decode('utf-8')
        print(self.Msg_S)

    def refresh(self):
        self.show_hand()
        self.show_tapis()
        self.draw_tourne()
        self.show_points()
        self.show_tour()
        self.after(1000, self.refresh) # run itself again after 1000 ms


dico_hand = dict()
for k in range(1,9):
    dico_hand[k] = "self.panel"+str(k)


if __name__=='__main__':
    app = Application()
    app.mainloop()
