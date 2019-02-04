#!C:\Users\myron\AppData\Local\Programs\Python\Python36-32\python.exe
#Homework 4
#Myron Woods




import cgi
import random
import sqlite3



def getDeck():
    ls = []
    ls.extend(range(52))
    random.shuffle(ls)
    try:
        con = sqlite3.connect('cards.db')
        cur = con.cursor()
        cur.executescript("""
            Drop table if exists DECK;
            create table if not exists DECK(Id INT, CardVal INT, Image TEXT);
        """)

        cardls = []
        for i in range(52):
            cardls.append( ( i+1, cardFaceVal(ls[i]), cardImage(ls[i]) ))

        cur.executemany("Insert into DECK Values(?,?,?)", cardls)

        con.commit()

        # cur.execute("SELECT * FROM DECK")
        # for row in cur:
        #    print(row)

    except sqlite3.Error:
        if con:
            print("Error! Rolling Back")
            con.rollback()

    finally:
        if con:
            con.close()


def cardImage(num):
    faces = ("ace", "2", "3", "4", "5", \
             "6", "7", "8", "9", "10", \
             "jack", "queen", "king")
    suits = ("hearts", "diamonds", "clubs", "spades")
    suitNum = num // 13
    faceNum = num % 13
    return suits[suitNum] + "-" + faces[faceNum]+ ".png"


def cardFaceVal(num):
    faceIndex = num % 13
    if (faceIndex >= 10):
        return 10
    else:
        return faceIndex + 1


def getCardImage(num):
    answer = ("error")
    try:
        con = sqlite3.connect('cards.db')
        cur = con.cursor()

        cur.execute("Select Image from DECK WHERE ID = " + str(num))
        answer = cur.fetchone()

    except sqlite3.Error:
        if con:
            print("Error! Rolling Back")
            con.rollback()

    finally:
        if con:
            con.close()

    return answer[0]


def getCardFaceVal(num):
    answer = ("0")
    try:
        con = sqlite3.connect('cards.db')
        cur = con.cursor()

        cur.execute("Select CardVal from DECK WHERE ID = " + str(num))
        answer = cur.fetchone()

    except sqlite3.Error:
        if con:
            print("Error! Rolling Back")
            con.rollback()

    finally:
        if con:
            con.close()

    return int(answer[0])


def main():

	try:
		print ("Content-type: text/html\n")
		print ("<html>")
		print ("<body style='background-color:lightblue'>")
		print ("<h1 style='color:green'>Welcome to Black Jack!</h1>")
		print ("<form method='post' action='BlackJack.py'>")
	   

		form = cgi.FieldStorage()

		currentCard = 1
		if (form.getvalue("currentCard")):
			currentCard = int(form.getvalue("currentCard"))
		

		if (currentCard == 1):
			getDeck()
			currentCard = 2
			lastPlayerCard = 2
		else:
			lastPlayerCard = int(form.getvalue("lastPlayerCard"))
		print ("<input id='cval' type='hidden' name='currentCard' value='" + str(currentCard+1) + "'>")
		print ("<input id='lval' type='hidden' name='lastPlayerCard' value='" + str(lastPlayerCard) + "'>")
		
		playerHandValue = 0
		aceCount = 0
		gameOver = False
		
		for num in range(1, lastPlayerCard+1):
			playerHandValue += getCardFaceVal(num)
			if (getCardFaceVal(currentCard) == 1):
				playerHandValue += 10
				aceCount += 1
			while (playerHandValue > 21 and aceCount > 0):
				playerHandValue -= 10
				aceCount -= 1
		print("<h2>Player Hand: "+ str(playerHandValue) + "</h2>")
		
		for num in range(1, lastPlayerCard+1):
			print("<img src='/cards/" + getCardImage(num) + "'>")
		
		if (playerHandValue == 21):
			gameOver = True
			print ("<h2>Black Jack!!! You win !!!</h2>")
		elif (playerHandValue > 21):
			gameOver = True
			print ("<h2>Busted!!! You lose !!!</h2>")
		elif(lastPlayerCard==currentCard):
			print("<h2>Do you want a hit? </h2>")
			print ("<button onclick='document.getElementById(\"lval\").value=" + str(lastPlayerCard+1) +
			"; this.form.submit();'>yes</button>")
			print ("<button onclick='this.form.submit();'>no</button>")
		
		
				
		
		if (lastPlayerCard < currentCard and not gameOver):
			dealerHandValue = 0
			aceCount =0
			done = False
			num = lastPlayerCard
			
			while (not done):
				num += 1
				currentCard += 1
				dealerHandValue += getCardFaceVal(num)
				if (getCardFaceVal(num) == 1):
					dealerHandValue += 10
					aceCount += 1
				while (dealerHandValue > 21 and aceCount > 0):
					dealerHandValue -= 10
					aceCount -= 1
				if (playerHandValue <= dealerHandValue <= 21):
					done = True
				elif (dealerHandValue > 21):
					done = True
				
			print("<h2>Dealer Hand: "+ str(dealerHandValue) + "</h2>")
			
			for num in range(lastPlayerCard+1, currentCard):
				print("<img src='/cards/" + getCardImage(num) + "'>")
				
			if (dealerHandValue <= 21):
				print("<h2>Dealer Wins</h2>")
			else:
				print("<h2>Dealer Busted!!!Player Wins!!!</h2>")
			gameOver = True
			
		if(gameOver):
			print ("<button onclick='document.getElementById(\"cval\").value=1; this.form.submit();'>Play Again?</button>")
	except:
		print ("<!-- --><hr><h1>Oops  An error occurred.</h1>")
		cgi.print_exception()     # Prints traceback, safely


	print ("</form>")
	print ("</body></html>")
    
main()
