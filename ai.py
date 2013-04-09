#-*- coding:utf-8-*-
import pprint
from copy import deepcopy

WIDTH = 4
HEIGHT = 5
HUMAN='human'
AI='ai'


def make_board():
    board=[]
    for x in range(0,WIDTH):
        board.append([])
    return board

def make_move(board,player,column,type):
    if type == 'remove':
        if board[column][0] == player:
            board[column].remove(player)
            
    if type == 'add':
        if len(board[column]) < HEIGHT:
            board[column].append(player)
    
def show_board(board):
    board=deepcopy(board)
    #refill
    for y in range(0,HEIGHT):
        for x in range(0,WIDTH):
            try:
                print x,y
                board[x][y]
            except:
                board[x].append(None)
                

    print '\n---------------------------'
    for y in range(HEIGHT-1,-1,-1):
        for x in range(0,WIDTH):
            print board[x][y],'|',
        print '\n---------------------------'    
    
if __name__ == '__main__':
    board = make_board()
    make_move(board,HUMAN,2,'add')
    pprint.pprint(board)
    show_board(board)
