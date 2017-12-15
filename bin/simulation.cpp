#include<iostream>
#include<string>
#include<stack>
#include<unordered_map>
#include<unordered_set>
#include<queue>
#include<vector>
#include<map>
#include<set>
#include<list>
#include<cstdlib>
#include<ctime>
#include<algorithm>
using namespace std;

class studyMem {
public:
	int num;
	long long arriveTime;
	long long studyTime;
};

class seat {
public:
	//int id;
	int avaSize;
	long long availableTime;
};

class tableUnit {
public:
	long long avaTime;
	int space;
	tableUnit(long long time, int sp) : avaTime(time), space(sp) {}
};

class table {
public:
	int totalSize;
	//int id;
	list<tableUnit> avaTime_space;
};

bool cmp(const seat& a, const seat& b) {
	return a.availableTime < b.availableTime;
}

bool cmpTable(tableUnit& a, tableUnit& b) {
	return a.avaTime < b.avaTime;
}

double schedule(queue<studyMem>& members, vector<seat>& desks, vector<seat>& rooms, vector<table>& tables) {
	long long totalWait = 0;
	int memberSize = members.size();

	while (!members.empty()) {
		studyMem sm = members.front();
		members.pop();
		if (sm.num == 1) {
			seat desk = desks[0];
			long long wait_deskTime = (desk.availableTime > sm.arriveTime) ? desk.availableTime - sm.arriveTime : 0;

			long long wait_tableTime = INT_MAX;
			int index = -1;
			for (int i = 0; i < tables.size(); i++) {
				tables[i].avaTime_space.sort(cmpTable);
				long long waitTime = (tables[i].avaTime_space.front().avaTime > sm.arriveTime) ? tables[i].avaTime_space.front().avaTime - sm.arriveTime : 0;
				if (waitTime < wait_tableTime) {
					index = i;
					wait_tableTime = waitTime;
				}
			}

			if (wait_deskTime <= wait_tableTime) {
				totalWait += wait_deskTime;
				desks[0].availableTime = sm.arriveTime + wait_deskTime + sm.studyTime;
				sort(desks.begin(), desks.end(), cmp);
			}
			else {
				totalWait += wait_tableTime;
				int size = tables[index].avaTime_space.front().space - 1;
				long long avaTime = tables[index].avaTime_space.front().avaTime;
				tables[index].avaTime_space.pop_front();
				if (size > 0) tables[index].avaTime_space.push_back(tableUnit(avaTime, size));
				tables[index].avaTime_space.push_back(tableUnit(sm.arriveTime + wait_tableTime + sm.studyTime, 1));
				//cout << tables[index].avaTime_space.back().avaTime << " " << tables[index].avaTime_space.back().space << endl;
			}
		}
		else {
			long long wait_roomTime = INT_MAX;
			int indexRoom = -1;
			for (int i = 0; i < rooms.size(); i++) {
				if (rooms[i].avaSize >= sm.num) {
					wait_roomTime = (rooms[i].availableTime > sm.arriveTime) ? rooms[i].availableTime - sm.arriveTime : 0;
					indexRoom = i;
					break;
				}
			}

			long long wait_tableTime = INT_MAX;
			int index = -1;
			for (int i = 0; i < tables.size(); i++) {
				//if (tables[i].totalSize < sm.num) continue;
				long long waitTime = 0;
				tables[i].avaTime_space.sort(cmpTable);
				int curSize = sm.num;
				for (auto it = tables[i].avaTime_space.begin(); it != tables[i].avaTime_space.end() && curSize > 0; it++) {
					waitTime = (it->avaTime > sm.arriveTime) ? it->avaTime - sm.arriveTime : 0;
					curSize -= it->space;
				}

				if (waitTime < wait_tableTime) {
					wait_tableTime = waitTime;
					index = i;
				}
			}
			if (wait_roomTime <= wait_tableTime) {
				totalWait += wait_roomTime;
				rooms[indexRoom].availableTime = sm.arriveTime + wait_roomTime + sm.studyTime;
				sort(rooms.begin(), rooms.end(), cmp);
			}
			else {
				totalWait += wait_tableTime;
				int size = sm.num;
				while (size - tables[index].avaTime_space.front().space > 0) {
					size -= tables[index].avaTime_space.front().space;
					tables[index].avaTime_space.pop_front();
				}
				if (size > 0) tables[index].avaTime_space.front().space -= size;
				tables[index].avaTime_space.push_back(tableUnit(sm.arriveTime + wait_tableTime + sm.studyTime, sm.num));
				//cout << tables[index].avaTime_space.back().avaTime << " " << tables[index].avaTime_space.back().space << endl;
			}
		}
	}
	cout << "total Wait time: " << totalWait << endl;
	return totalWait * 1.0 / memberSize;
}


int main() {
	int n;
	cout << "Please input the number of study units(individual and study group): " << endl;
	cin >> n;
	int k;
	cout << "Please input the number of simulations: " << endl;
	cin >> k;
	srand((unsigned)time(NULL));
	for (int j = 0; j < k; j++) {
		cout << "the result of " << j + 1 << " simulation" << endl;
		queue<studyMem> members;
		int numDesk = 50;
		int numRoom = 10;
		int numTable = 20;
		for (int i = 0; i < n; i++) {
			studyMem mem;
			if (rand() % 2) mem.num = 1;	//individual
			else mem.num = 2 + rand() % 5;	//the number of persons in the study group (2~6)
			mem.arriveTime = i * 2;
			mem.studyTime = 30 + rand() % 121;	//study time 30~150
			members.push(mem);
		}
		vector<seat> desks(numDesk);
		for (int i = 0; i < numDesk; i++) {
			desks[i].avaSize = 1;
			desks[i].availableTime = 0;
		}
		vector<seat> rooms(numRoom);
		for (int i = 0; i < numRoom; i++) {
			rooms[i].avaSize = 2 + rand() % 5;	//room size: 2~6
			rooms[i].availableTime = 0;
		}
		vector<table> tables(numTable);
		for (int i = 0; i < numTable; i++) {
			tables[i].totalSize = 6;	//table size: 6
			tables[i].avaTime_space.push_back(tableUnit(0, 6));
		}
		double ave = schedule(members, desks, rooms, tables);
		cout << "Average Wait " << ave << " secs" << endl;
	}
	return 0;
}
