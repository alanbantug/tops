#! python3

import numpy as np
import pandas as pd
from pandas import Series, DataFrame

from collections import defaultdict
import datetime
import operator
import random
import copy
import os

import math
from time import time

import itertools
from itertools import combinations

# the next two lines are required to create the classifier
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import train_test_split


class getCombinations(object):

	def __init__(self, selected, ltype, usage, distrib):

		self.distrib = distrib

		if self.distrib == 1:
			self.selectedNumbers = selected[:30]
		else:
			self.selectedNumbers = selected[:25]

		self.selectedNumbers = selected[:30]

		self.ltype = ltype
		self.othNumbers = []
		self.extNumbers = []
		self.limit = 0
		self.extlimit = 0

		if self.ltype == 1:
			self.limit = 39

		elif self.ltype == 2:
			self.limit = 47
			self.extlimit = 27

		elif self.ltype == 3:
			self.limit = 70
			self.extlimit = 25

		elif self.ltype == 4:
			self.limit = 69
			self.extlimit = 25

		for i in range(self.limit):
			if i+1 in self.selectedNumbers:
				pass
			else:
				self.othNumbers.append(i+1)

		for i in range(self.extlimit):
			self.extNumbers.append(i+1)

		random.shuffle(self.extNumbers)

		self.getCounts(usage)


	def getCounts(self, usage):

		''' This procedure will get the count of possible combinations based on the numbers selected
		'''

		self.numberCount = len(self.selectedNumbers)
		self.divCount = usage / 5
		self.comboCount = math.factorial(self.numberCount) / (math.factorial(self.numberCount - self.divCount) * math.factorial(self.divCount))
		self.duplCount = 25 - self.numberCount

	def randomSelect(self, usage):

		''' This function will generate the combinations using itertools instead of manually going thru
		    the combinations which is done in the old function. The generation will be limited to 100 loops.
		'''

		# initialize the generator
		n_set = self.initIterator(usage)

		selection = []
		numbers_used = []

		loop_count = 0

		# set the starting point of the iterator
		for i in range(random.randint(1, self.comboCount)):
			next(n_set)

		while True:

			try:
				if self.numberCount < 25 and len(selection) == 4:

					missed = [num for num in self.selectedNumbers if num not in numbers_used]

					while True:
						num_list = sorted(next(n_set))

						missed_found = len([1 for m in missed if m in num_list])

						if missed_found == len(missed):
							break
				else:
					num_list = sorted(next(n_set))

				if self.checkCounts(num_list, selection):

					# check if the generated combination satisfies the criteria
					if self.checkDistribution(num_list) and self.checkConsecutives(num_list, selection) and self.checkSpread(num_list):

						for num in num_list:
							numbers_used.append(num)

						selection.append(num_list)

						if self.numberCount < 25 and len(selection) == 4:
							for i in range(500):
								next(n_set)

				if len(selection) == 5:
					break

			except:
				n_set = self.initIterator(usage)

				loop_count += 1

				# if the loop is on the second go-around, get a new starting point
				if loop_count == 2:

					selection = []
					numbers_used = []

					loop_count = 0

					for i in range(random.randint(1, self.comboCount)):
						next(n_set)

		# select a Super number if the lotto game selected is SuperLotto
		if self.ltype == 2 or self.ltype == 3 or self.ltype == 4:
			for sel in selection:
				sel.append(self.extNumbers[random.randint(0, self.extlimit - 1)])

		return selection


	def initIterator(self, usage):

		''' This function will be called to initialize the combination generator
		'''

		num_chk = copy.copy(self.selectedNumbers)

		random.shuffle(num_chk)

		n_set = itertools.combinations(num_chk, 5)

		return n_set

	def checkSpread(self, n_list):

		return True if n_list[4] - n_list[0] > 12 else False

	def checkConsecutives(self, n_list, selection):

		# This function checks if a combination has consecutive numbers. If there are consecutive numbers, return 1
		with_con = 0

		c_count = np.sum([1 for i in range(len(n_list) - 1) if n_list[i] + 1 == n_list[i + 1]])

		if c_count <= 1:
			with_con += 1
		else:
			return False

		# loop thru all the contents of sel_copy
		for sel in selection:
			c_count = np.sum([1 for i in range(len(sel) - 1) if sel[i] + 1 == sel[i + 1]])

			if c_count >= 1:
				with_con += 1

		return True if with_con <= 1 else False

	def checkCounts(self, n_list, selection):

		# This function checks the numbers in the generated combinations exist is the selected combinations

		unique = True

		if self.numberCount >= 25:
			limit = 0
		else:
			if len(selection) < 4:
				limit = 0
			else:
				limit = 1

		for n in n_list:
			n_count = 0
			for sel in selection:
				n_count += sel.count(n)

			if n_count > limit:
				unique = False

		return unique

	def checkDistribution(self, n_list):

		ranges = self.getRanges(self.limit)

		part_a = [n for n in n_list if n <= ranges[0]]
		part_b = [n for n in n_list if n >= ranges[0] + 1 and n <= ranges[1]]
		part_c = [n for n in n_list if n >= ranges[1] + 1]

		if len(part_a) < 3 and len(part_b) < 3 and len(part_c) < 3:
			if self.distrib == 1:
				return True
			else:
				return False
		else:
			if self.distrib == 1:
				return False
			else:
				return True

	def getRanges(self, limit):

		ranges = []

		ranges.append(int(limit/3))
		ranges.append(int(limit/3) * 2)

		return ranges

	def getMore(self, n_set, selection, count):

		while True:

			n_set_new = copy.copy(n_set)
			o_set_new = copy.copy(self.othNumbers)

			random.shuffle(o_set_new)

			for i in range(count):
				n_set_new.append(o_set_new.pop())

			n_set_new = sorted(n_set_new)

			if self.checkConsecutives(n_set_new) == 0 and self.checkUnique(n_set_new, selection):
				break

		return n_set_new
