#!/usr/bin/env python
#coding=utf-8

import csv

class Solution:
	rowMask = [[False] * 9 for i in range(9)]
	colMask = [[False] * 9 for i in range(9)]
	areaMask = [[False] * 9 for i in range(9)]
	
	def __init__(self):
		"""
		read the csv file to board
		:type board: List[List[str]]
		"""
		with open("sudoku.csv","rb") as file:
			reader = csv.reader(file)
			board = list(reader)
			self.solveSudoku(board)
	
	def solveSudoku(self, board):
		"""
		:type board: List[List[str]]
		:rtype: void Do not return anything, modify board in-place instead.
		"""
		if len(board) != 9:
			print "can't read the data"
			return False
		if self.initSudoku(board):
			if self.recursiveSudoku(board,0,0):
				with open("sudoku_solve.csv","w") as file:
					writer = csv.writer(file,dialect=("excel"))
					for row in board:
						writer.writerow(row)
				print "solve success"
			else:
				print "solve false"
		else:
			print "can't init the mask"
		
	def initSudoku(self,board):
		"""
		fill the mask
		"""	
		for r in range(9):
			for c in range(9):
				area = r//3*3 + c//3
				if board[r][c] == '.':
					continue
				
				val = int(board[r][c]) - 1
				if self.rowMask[r][val] or self.colMask[c][val] or self.areaMask[area][val]:
					return False
				self.rowMask[r][val]= self.colMask[c][val]=self.areaMask[area][val]=True
		return True
	
	def recursiveSudoku(self, board, r, c):
		"""
		recursive
		"""
		if r == 9:
			return True
		
		if c == 9:
			return self.recursiveSudoku(board,r+1,0)
		
		if board[r][c] != '.':
			return self.recursiveSudoku(board,r,c+1)

		for val in range(9):
			area =  r//3*3 +c//3
			if self.rowMask[r][val] or self.colMask[c][val] or self.areaMask[area][val]:
				continue

			board[r][c] = str(val + 1)
			self.rowMask[r][val] = self.colMask[c][val] = self.areaMask[area][val] =True
			if self.recursiveSudoku(board,r,c+1):
				return True

			board[r][c] = '.'
			self.rowMask[r][val] = self.colMask[c][val] = self.areaMask[area][val] =False

		return False

if __name__ == "__main__":
	# slove and write
	Solution()

