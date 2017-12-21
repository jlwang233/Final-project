import sys
import random
import queue
from operator import itemgetter, attrgetter

class studyUnit:
	"""
	class for study unit
	"""
	def __init__(self):
		self.num = 0
		self.arriveTime = 0
		self.studyTime = 0

class seat:
	"""
	class for desk and room
	avaSize == 1 -> desk
	avaSize [2, 6] -> room
	"""
	def __init__(self):
		avaSize = 0
		availableTime = 0

class tableUnit:
	"""
	class for specific unit part of a table, where each seat has the same avaliable time
	"""
	def __init__(self, time, sp):
		self.avaTime = time
		self.space = sp;

class table:
	"""
	class for table
	"""
	def __init__(self):
		"""
		avaTime_space: list of tableUnits for this table
		"""
		self.totalSize = 0
		self.avaTime_space = []

def schedule(members, desks, rooms, tables, lastUnitArriveTime):
	"""
	function for scheduling study units to get seats in the library following FIFO
	members: the queue of study units
	desks: the list of desks in the ASC order sorted by available time
	rooms:  the list of rooms in the ASC order sorted by available time
	tables: the list of tables whose tableUnits are in the ASC order sorted by available time
	lastUnitArriveTime: the time of the last study unit arriving at the library
	totalWait: the total waiting time of all the study units
	memberSize: the number of study units
	numWaiting: the number of study units who are still waiting for seats while the 
		last study unit arriving at the library
	"""
	totalWait = 0
	memberSize = members.qsize()
	numWaiting = 0
	wait_lastUnit = 0

	while not(members.empty()):
		firstUnit = members.get()	#firstUnit: the first studyUnit in the queue
		if firstUnit.num == 1:	#firstUnit is an individual, desk or table
			desk = desks[0]
			#compute the wait time for the eariliest available desk
			wait_deskTime = desk.availableTime - firstUnit.arriveTime if desk.availableTime > firstUnit.arriveTime else 0

			#compute the wait time for the eariliest available table
			wait_tableTime = sys.maxsize
			index = -1
			for i in range(len(tables)):
				tables[i].avaTime_space.sort(key=attrgetter('avaTime'))
				waitTime = tables[i].avaTime_space[0].avaTime - firstUnit.arriveTime if tables[i].avaTime_space[0].avaTime > firstUnit.arriveTime else 0
				if waitTime < wait_tableTime:
					index = i
					wait_tableTime = waitTime

			#priority: desk > table
			if wait_deskTime <= wait_tableTime:
				if members.empty():
					wait_lastUnit += wait_deskTime
				if firstUnit.arriveTime + wait_deskTime >= lastUnitArriveTime:
					numWaiting += 1
				totalWait += wait_deskTime
				desks[0].availableTime = firstUnit.arriveTime + wait_deskTime + firstUnit.studyTime
				desks.sort(key=attrgetter('availableTime'))
			else:
				if members.empty():
					wait_lastUnit += wait_tableTime
				if firstUnit.arriveTime + wait_tableTime >= lastUnitArriveTime:
					numWaiting += 1
				totalWait += wait_tableTime
				#size: the size of the rest part of the selected table unit
				size = tables[index].avaTime_space[0].space - 1
				avaTime = tables[index].avaTime_space[0].avaTime
				tables[index].avaTime_space.remove(tables[index].avaTime_space[0])
				if size > 0 : tables[index].avaTime_space.append(tableUnit(avaTime, size))
				tables[index].avaTime_space.append(tableUnit(firstUnit.arriveTime + wait_tableTime + firstUnit.studyTime, 1))
		else:	#firstUnit is a study group, room or table
			#compute the wait time for the eariliest available room
			wait_roomTime = sys.maxsize
			indexRoom = -1
			for i in range(len(rooms)):
				if rooms[i].avaSize >= firstUnit.num:
					wait_roomTime = rooms[i].availableTime - firstUnit.arriveTime if rooms[i].availableTime > firstUnit.arriveTime else 0
					indexRoom = i
					break

			"""
			compute the wait time for the eariliest available table
			the expected table is that its (firstUnit.num)th available time of all the seats
			in this table is the earliest available time among all such seats in other tables
			"""
			wait_tableTime = sys.maxsize
			index = -1
			for i in range(len(tables)):
				waitTime = 0
				tables[i].avaTime_space.sort(key=attrgetter('avaTime'))
				curSize = firstUnit.num
				it = tables[i].avaTime_space
				for j in range(len(it)):
					if curSize <= 0 : break
					waitTime = it[j].avaTime - firstUnit.arriveTime if it[j].avaTime > firstUnit.arriveTime else 0
					curSize -= it[j].space

				if waitTime < wait_tableTime:
					wait_tableTime = waitTime
					index = i

			#priority: room > table
			if wait_roomTime <= wait_tableTime:
				if members.empty():
					wait_lastUnit += wait_roomTime
				if firstUnit.arriveTime + wait_roomTime >= lastUnitArriveTime:
					numWaiting += 1
				totalWait += wait_roomTime
				rooms[indexRoom].availableTime = firstUnit.arriveTime + wait_roomTime + firstUnit.studyTime
				rooms.sort(key=attrgetter('availableTime'))
			else:
				#update the selected firstUnit.num seats' available time to the time when this study group leaves library
				if members.empty():
					wait_lastUnit += wait_tableTime
				if firstUnit.arriveTime + wait_tableTime >= lastUnitArriveTime:
					numWaiting += 1
				totalWait += wait_tableTime
				size = firstUnit.num
				while len(tables[index].avaTime_space) > 0 and size - tables[index].avaTime_space[0].space >= 0:
					size -= tables[index].avaTime_space[0].space
					tables[index].avaTime_space.remove(tables[index].avaTime_space[0])
				if size > 0 : tables[index].avaTime_space[0].space -= size
				tables[index].avaTime_space.append(tableUnit(firstUnit.arriveTime + wait_tableTime + firstUnit.studyTime, firstUnit.num))

	print("Total Wait time: " + str(totalWait))
	print("Average Wait " + str(totalWait * 1.0 / memberSize) + " mins")
	print(str(numWaiting) + " tasks remaining")
	print("The last study unit has to wait " + str(wait_lastUnit) + "mins")

# Running part
n = int(input("Please input the number of study units(individual and study group): "))
k = int(input("Please input the number of simulations: "))

for j in range(k):
	print("the result of " + str(j + 1) + " simulation")
	members = queue.Queue()
	numDesk = 20
	numRoom = 10
	numTable = 5
	for i in range(n):
		mem = studyUnit()
		mem.num = 1 if random.randint(0, 1) == 0 else random.randint(2, 6)
		mem.arriveTime = i * 5
		mem.studyTime = random.randint(30, 150)	
		members.put(mem)

	desks = []
	for i in range(numDesk):
		desks.append(seat())
		desks[i].avaSize = 1
		desks[i].availableTime = 0

	rooms = []
	for i in range(numRoom):
		rooms.append(seat())
		rooms[i].avaSize = random.randint(2, 6)
		rooms[i].availableTime = 0

	tables = []
	for i in range(numTable):
		tables.append(table())
		tables[i].totalSize = 6
		tables[i].avaTime_space.append(tableUnit(0, 6))

	schedule(members, desks, rooms, tables, (n - 1) * 5)
