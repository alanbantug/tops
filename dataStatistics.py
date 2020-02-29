#! python3

import numpy as np
import pandas as pd
from pandas import Series, DataFrame

import matplotlib.pyplot as plt

import pdb

from collections import defaultdict
import datetime
import operator
import random
import copy
import os

from time import time
import math

import itertools

class dataStatistics(object):

	def __init__(self, config, infile, ltype):

		self.infile = infile
		self.ltype = ltype

		if ltype == 1:
			self.topLimit = 39
		elif ltype == 2:
			self.topLimit = 47
		elif ltype == 3:
			self.topLimit = 70
		elif ltype == 4:
			self.topLimit = 69

		self.lastWinner = []
		self.last_match_draws = 0
		self.max_gap = 0

		if self.infile == None:
			self.numberCounts = defaultdict(int)
			self.megaCounts = defaultdict(int)
			self.dataHash = {}
			self.patternCounts = {'5O': 0, '4O': 0, '3O': 0, '3E': 0, '4E': 0, '5E': 0}
			self.lastestDraw = 0
		else:
			self.numberCounts, self.megaCounts, self.patternCounts, self.dataHash, self.latestDraw, self.latestWinner = self.hashDataFile()
			self.reformatFile()


	def hashDataFile(self):

		''' This function will create a hash table for the data file passed. Note this will be common for fantasy and superlotto
		'''
		hashTable = {}
		ncounter = defaultdict(int)
		mcounter = defaultdict(int)
		pcounter = {'5O': 0, '4O': 0, '3O': 0, '3E': 0, '4E': 0, '5E': 0}

		latest_draw = 0

		with open(self.infile, 'r') as f_data:

			for data in f_data:

				fields = data.split()

				if len(fields) == 0:
					continue

				if fields[0].isdigit():

					# get the draw and store it in the last draw field
					if latest_draw == 0:
						latest_draw = int(fields[0])
						latest_winner = [int(num) for num in fields[5:10]]

					# create the hash key
					hash_key = bytes([int(num) for num in fields[5:10]])

					# store the draw number with the hash key if it is still not in the table. this is needed so that
					# subsequent similar draws will not overwrite the latest draw
					if hash_key in hashTable:
						pass
					else:
						hashTable[hash_key] = int(fields[0])

					for num in fields[5:10]:
						ncounter[int(num)] += 1

					if len(fields) > 10:
						mcounter[int(fields[10])] += 1

					p = self.checkPattern(fields[5:10])
					pcounter[p] += 1

		# sort the numbers by occurence
		sorted_ncounter = sorted(ncounter.items(), key=operator.itemgetter(1), reverse=True)
		ncounts = {num:count for num, count in sorted_ncounter}

		sorted_mcounter = sorted(mcounter.items(), key=operator.itemgetter(1), reverse=True)
		mcounts = {num:count for num, count in sorted_mcounter}

		return ncounter, mcounter, pcounter, hashTable, latest_draw, latest_winner

	def checkPattern(self, numbers):

		odd_count = np.sum(1 for n in numbers if int(n) % 2 != 0)
		eve_count = np.sum(1 for n in numbers if int(n) % 2 == 0)

		if odd_count > 2:
			pattern = str(odd_count) + 'O'
		else:
			pattern = str(eve_count) + 'E'

		return pattern

	def reformatFile(self):

		''' This function will create the CSV file to build the dataframe
		'''

		if self.ltype == 1:
			self.reformatFantasy()
		else:
			self.reformatSuperMegaPower(self.ltype)

		# self.analyzeData()

	def reformatFantasy(self):

		rec_ctr = 0

		with open('data\\cf_data.csv', 'w') as myOutput:
			with open(self.infile, 'r') as myInput:

				for dataLine in myInput:

					fields = dataLine.split()

					if len(fields) > 0:

						if fields[0].isdigit():

							# build the data to write to csv_data
							data = []

							in_date = fields[2] + ' ' + fields[3] + ' ' + fields[4]
							draw_date = datetime.datetime.strptime(in_date, '%b %d, %Y').date()

							data.append(fields[0])
							data.append(str(draw_date))

							for n in fields[5:10]:
								data.append(n)

							winner = ",".join(data)
							myOutput.write(winner)
							myOutput.write("\n")

							rec_ctr += 1

		myInput.close()
		myOutput.close()

	def reformatSuperMegaPower(self, ltype):

		''' This function will count the occurences and get the top 25
		'''

		if ltype == 2:
			dfile = 'data\\cs_data.csv'
		elif ltype == 3:
			dfile = 'data\\cm_data.csv'
		else:
			dfile = 'data\\cp_data.csv'

		rec_ctr = 0

		with open(dfile, 'w') as myOutput:
			with open(self.infile, 'r') as myInput:

				for dataLine in myInput:

					fields = dataLine.split()

					if len(fields) > 0:

						if fields[0].isdigit():

							# build the data to write to csv_data
							data = []

							in_date = fields[2] + ' ' + fields[3] + ' ' + fields[4]
							draw_date = datetime.datetime.strptime(in_date, '%b %d, %Y').date()

							data.append(fields[0])
							data.append(str(draw_date))

							for n in fields[5:10]:
								data.append(n)

							data.append(fields[10])

							winner = ",".join(data)
							myOutput.write(winner)
							myOutput.write("\n")

		myInput.close()
		myOutput.close()


	def analyzeData(self):

		''' This function will do several things:

			1. Read the CSV file into a DataFrame
			2. Get the top 25 numbers at the time before the draws and then compares them with the winning draws
			3. Get the date of when the numbers from the last draw came from the top 25, the count of such incidents, and the shortest
			   and longest dates in between the occurences
		'''

		if self.ltype == 1:
			self.analyzeFantasyFile()

		elif self.ltype == 2:
			self.analyzeSuperFile()

		elif self.ltype == 3:
			self.analyzeMegaFile()

		elif self.ltype == 4:
			self.analyzePowerFile()

	def analyzeFantasyFile(self):

		# Load the csv_data file into a dataframe

		fantasy_file = pd.read_csv('data\\cf_data.csv', nrows=1000, header=None)
		fantasy_file.columns = ['Draw', 'Date', 'A', 'B', 'C', 'D', 'E']

		fantasy_file['MS'] = fantasy_file[['Draw', 'A', 'B', 'C', 'D', 'E']].apply(self.topNumbersAtDraw, args=(1,), axis=1)

		fantasy_select = copy.copy(fantasy_file[fantasy_file['MS'] == 5])
		gap_list = fantasy_select[['Draw']].apply(self.getGapList, axis=0)

		fantasy_select = fantasy_select.set_index(pd.Index([n for n in range(len(fantasy_select))]))
		gap_list = gap_list.set_index(pd.Index([n for n in range(len(gap_list))]))

		fantasy_select = pd.concat([fantasy_select, gap_list], axis=1)
		fantasy_select.columns = ['Draw', 'Date', 'A', 'B', 'C', 'D', 'E', 'MS', 'GAP']

		fantasy_select.to_csv('data\\cf_select.csv')

		self.first_match = fantasy_select['Date'].min()
		self.last_match = fantasy_select['Date'].max()

		last_match_split = self.last_match.split('-')

		date_a = datetime.datetime(int(last_match_split[0]), int(last_match_split[1]), int(last_match_split[2]))
		curr_date  = datetime.datetime.now()

		self.last_match_days = curr_date - date_a
		self.last_match_draws = fantasy_file['Draw'].max() - fantasy_select['Draw'].max()
		self.last_compare = fantasy_file['MS'].iloc[0]

		self.exact_match = fantasy_select['MS'].count()
		self.max_gap = fantasy_select['GAP'].max()
		self.min_gap = fantasy_select[fantasy_select['GAP'] > 0]['GAP'].min()

		# delete the results files
		try:
			os.remove('data\\results.jpg')
		except:
			pass

		plt.figure(figsize=(4,3))
		plt.plot(fantasy_file['MS'][:100])
		plt.savefig('data\\results.jpg')

	def analyzeSuperFile(self):

		# Load the csv_data file into a dataframe
		superlotto_file = pd.read_csv('data\\cs_data.csv', nrows=1000, header=None)
		superlotto_file.columns = ['Draw', 'Date', 'A', 'B', 'C', 'D', 'E', 'S']

		superlotto_file['MS'] = superlotto_file[['Draw', 'A', 'B', 'C', 'D', 'E']].apply(self.topNumbersAtDraw, args=(2,), axis=1)

		superlotto_select = copy.copy(superlotto_file[superlotto_file['MS'] == 5])
		gap_list = superlotto_select[['Draw']].apply(self.getGapList, axis=0)

		superlotto_select = superlotto_select.set_index(pd.Index([n for n in range(len(superlotto_select))]))
		gap_list = gap_list.set_index(pd.Index([n for n in range(len(gap_list))]))

		superlotto_select = pd.concat([superlotto_select, gap_list], axis=1)
		superlotto_select.columns = ['Draw', 'Date', 'A', 'B', 'C', 'D', 'E', 'S', 'MS', 'GAP']

		superlotto_select.to_csv('data\\cs_select.csv')

		self.first_match = superlotto_select['Date'].min()
		self.last_match = superlotto_select['Date'].max()
		last_match_split = self.last_match.split('-')

		date_a = datetime.datetime(int(last_match_split[0]), int(last_match_split[1]), int(last_match_split[2]))
		curr_date  = datetime.datetime.now()

		self.last_match_days = curr_date - date_a
		self.last_match_draws = superlotto_file['Draw'].max() - superlotto_select['Draw'].max()
		self.last_compare = superlotto_file['MS'].iloc[0]

		self.exact_match = superlotto_select['MS'].count()
		self.max_gap = superlotto_select['GAP'].max()
		self.min_gap = superlotto_select[superlotto_select['GAP'] > 0]['GAP'].min()

		# delete the results files
		try:
			os.remove('data\\results.jpg')
		except:
			pass

		plt.figure(figsize=(4,3))
		plt.plot(superlotto_file['MS'][:100])
		plt.savefig('data\\results.jpg')

	def analyzeMegaFile(self):

		# Load the csv_data file into a dataframe
		megalotto_file = pd.read_csv('data\\cm_data.csv', nrows=1000, header=None)
		megalotto_file.columns = ['Draw', 'Date', 'A', 'B', 'C', 'D', 'E', 'M']

		megalotto_file['MS'] = megalotto_file[['Draw', 'A', 'B', 'C', 'D', 'E']].apply(self.topNumbersAtDraw, args=(3,), axis=1)

		megalotto_select = copy.copy(megalotto_file[megalotto_file['MS'] == 5])
		gap_list = megalotto_select[['Draw']].apply(self.getGapList, axis=0)

		megalotto_select = megalotto_select.set_index(pd.Index([n for n in range(len(megalotto_select))]))
		gap_list = gap_list.set_index(pd.Index([n for n in range(len(gap_list))]))

		megalotto_select = pd.concat([megalotto_select, gap_list], axis=1)
		megalotto_select.columns = ['Draw', 'Date', 'A', 'B', 'C', 'D', 'E', 'M', 'MS', 'GAP']

		megalotto_select.to_csv('data\\cm_select.csv')

		self.first_match = megalotto_select['Date'].min()
		self.last_match = megalotto_select['Date'].max()
		last_match_split = self.last_match.split('-')

		date_a = datetime.datetime(int(last_match_split[0]), int(last_match_split[1]), int(last_match_split[2]))
		curr_date  = datetime.datetime.now()

		self.last_match_days = curr_date - date_a
		self.last_match_draws = megalotto_file['Draw'].max() - megalotto_select['Draw'].max()
		self.last_compare = megalotto_file['MS'].iloc[0]

		self.exact_match = megalotto_select['MS'].count()
		self.max_gap = megalotto_select['GAP'].max()
		self.min_gap = megalotto_select[megalotto_select['GAP'] > 0]['GAP'].min()

		# delete the results files
		try:
			os.remove('data\\results.jpg')
		except:
			pass

		plt.figure(figsize=(4,3))
		plt.plot(megalotto_file['MS'][:100])
		plt.savefig('data\\results.jpg')


	def analyzePowerFile(self):

		# Load the csv_data file into a dataframe
		powerball_file = pd.read_csv('data\\cm_data.csv', nrows=1000, header=None)
		powerball_file.columns = ['Draw', 'Date', 'A', 'B', 'C', 'D', 'E', 'M']

		powerball_file['MS'] = powerball_file[['Draw', 'A', 'B', 'C', 'D', 'E']].apply(self.topNumbersAtDraw, args=(4,), axis=1)

		powerball_select = copy.copy(powerball_file[powerball_file['MS'] == 5])
		gap_list = powerball_select[['Draw']].apply(self.getGapList, axis=0)

		powerball_select = powerball_select.set_index(pd.Index([n for n in range(len(powerball_select))]))
		gap_list = gap_list.set_index(pd.Index([n for n in range(len(gap_list))]))

		powerball_select = pd.concat([powerball_select, gap_list], axis=1)
		powerball_select.columns = ['Draw', 'Date', 'A', 'B', 'C', 'D', 'E', 'M', 'MS', 'GAP']

		powerball_select.to_csv('data\\cp_select.csv')

		self.first_match = powerball_select['Date'].min()
		self.last_match = powerball_select['Date'].max()
		last_match_split = self.last_match.split('-')

		date_a = datetime.datetime(int(last_match_split[0]), int(last_match_split[1]), int(last_match_split[2]))
		curr_date  = datetime.datetime.now()

		self.last_match_days = curr_date - date_a
		self.last_match_draws = powerball_file['Draw'].max() - powerball_select['Draw'].max()
		self.last_compare = powerball_file['MS'].iloc[0]

		self.exact_match = powerball_select['MS'].count()
		self.max_gap = powerball_select['GAP'].max()
		self.min_gap = powerball_select[powerball_select['GAP'] > 0]['GAP'].min()

		# delete the results files
		try:
			os.remove('data\\results.jpg')
		except:
			pass

		plt.figure(figsize=(4,3))
		plt.plot(powerball_file['MS'][:100])
		plt.savefig('data\\results.jpg')

	def matchTopNumbers(self, data):

		draw, numa, numb, numc, numd, nume = data

		draw_set = [numa, numb, numc, numd, nume]

		sorted_ncounter = sorted(self.numberCounts.items(), key=operator.itemgetter(1), reverse=True)
		ncounts = {num:count for num, count in sorted_ncounter}
		top_numbers = list(ncounts.keys())[:25]

		match_count = 0

		for n in draw_set:
			match_count += top_numbers.count(int(n))

		return match_count

	def getGapList(self, draw):

		gap_list = []

		for idx in range(len(draw) - 1):

			diff = draw.iloc[idx] - draw.iloc[idx + 1]
			gap_list.append(diff)

		# add one more to account for the gap for the last row, whcih would be zero since nothing comes after
		gap_list.append(0)

		return gap_list

	def topNumbersAtDraw(self, data, f_source):

		if f_source == 1:
			d_file = 'data\\cf_data.csv'
		elif f_source == 2:
			d_file = 'data\\cs_data.csv'
		elif f_source == 3:
			d_file = 'data\\cm_data.csv'
		else:
			d_file = 'data\\cp_data.csv'

		draw, numa, numb, numc, numd, nume = data

		numbers = [numa, numb, numc, numd, nume]

		# copy the counter
		work_counter = copy.deepcopy(self.numberCounts)

		# read the file from the top
		# while draw is greater than or equal to the draw passed, subtract the numbers

		with open('data\\cf_data.csv', 'r') as d_file:

			for dataLine in d_file:

				fields = dataLine.split(',')

				if len(fields) > 0:

					if fields[0].isdigit():

						if int(fields[0]) >= int(draw):

							work_counter = self.subtractCount(fields[5:10], work_counter)
						else:

							break

		d_file.close()

    	# sort the count
		sorted_counter = sorted(work_counter.items(), key=operator.itemgetter(1), reverse=True)

		top_counter = {k:v for k,v in sorted_counter}

		# get the top 10 numbers and compare
		t_count = np.sum([1 for n in numbers if n in list(top_counter.keys())[:25]])

		return int(t_count)


	def subtractCount(self, numbers, work_counter):

		for n in numbers:
			work_counter[int(n)] -= 1

		return work_counter

	def writeGenerated(self, config, selection):

		config.updateLastSet(self.ltype, selection)


	def getTopNumbers(self):

		''' Sort and then convert the keys object to list and get only the top 25 numbers
		'''

		sorted_ncounter = sorted(self.numberCounts.items(), key=operator.itemgetter(1), reverse=True)
		ncounts = {num:count for num, count in sorted_ncounter}

		return list(ncounts.keys())


	def getDataStatistics(self):

		sorted_ncounter = sorted(self.numberCounts.items(), key=operator.itemgetter(0), reverse=False)
		ncounts = {num:count for num, count in sorted_ncounter}

		if len(self.megaCounts) > 0:
			sorted_mcounter = sorted(self.megaCounts.items(), key=operator.itemgetter(0), reverse=False)
			mcounts = {num:count for num, count in sorted_mcounter}
		else:
			mcounts = self.megaCounts

		return ncounts, mcounts, self.patternCounts, self.last_match_draws, self.max_gap


	def getLastDraw(self):

		return self.latestDraw, self.latestWinner


	def getStats(self):

		return self.numberCounts
