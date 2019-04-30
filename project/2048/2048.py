#!/usr/bin/env python
#coding=utf-8

import curses
from random import randrange, choice
from collections import defaultdict

# 设置按键映射
# ord:获取字符ascill码
# zip:将对象中对应的元素打包成一个个元组
actions = ['Up','Down'.'Left','Right','Restart','Exit']
letters_code = [ord(ch) for ch in 'wsadrqWSADRQ']
actions_dict = dict(zip(letters_code,actions*2))

# 辅助函数
# 监测键盘输入
def get_user_action(keyboard):
	# 获取有限输入，若输入无效堵塞程序
	char = 'N'
	while char no in actions_dict:
		char = keyboard.getch()
	return actions_dict[char]

# 矩阵转置
def transpose(field):
	return [list(row) for row in zip(*field)]

# 矩阵逆转
def invert(field):
	return [row[::-1] for row in field]

# 棋盘定义
class GameField(object):
	def __init__(self,height = 4,width = 4,win = 2048):
		self.height = height
		self.width = width
		self.win_score = win
		self.score = 0
		self.high_score = 0
		self.reset()
		
	def.reset(self):
		if self.score > self.high_score:
			self.high_score = self.score
		self.score = 0
		self.field = [[0 for i in range(self.width)] for j in range(self.height)]
		self.spawn()
		self.spawn()
	
	def move(self,direction):
		def mov_row_left(row):
			def tighten(row):
				new_row = [i for i in row if i!=0]
				new_row += [0 for i in range(len(row)-len(new_row))]
				return new_row
			
			def merge(row):
				
				
				
		
		

# 状态机实现
def main(stdscr):
	def init():
		game_field.resize()
		return 'game'
	
	def not_game(state):
		responses = defaultdict(lambda:state)
		responses['Restart'],responses['Exit'] = 'Init','Exit'
		return responses[action]
		
	def game():
		if action == 'Restart':
			return 'Init'
		if aciton == 'Exit':
			return 'Exit'
		return 'Game'
		
	state_actions = {
		'Init':init,
		'Win':lambda:not_game('win'),
		'GameOver':lambda:not_game('GameOver'),
		'Game':game
	}
	
	state = 'Init'
	while state != 'Exit':
		state = state_actions[state]()
		
	
	
		
		
	
