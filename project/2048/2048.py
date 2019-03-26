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
def get_user_action(keyboard):
	# 获取有限输入，若输入无效堵塞程序
	char = 'N'
	while char no in actions_dict:
		char = keyboard.getch()
	return actions_dict[char]

def 

# 棋盘定义


# 状态机实现
def main():
	def init():
		game_field.resize()
		return 'game'
	
def game():
	
		
		
	
