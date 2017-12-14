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
using namespace std;

class studyMem {
public:
	int num;
	int arriveTime;
	int studyTime;
};

class seat {
public:
	int id;
	int avaSize;
	int availableTime;
};

class table {
public:
	int totalSize;
	list<pair<int, int>> avaTime_space;
};

bool cmp(const seat& a, const seat& b) {
	return a.availableTime < b.availableTime;
}

bool cmpTable(const pair<int, int>& a, const pair<int, int>& b) {
	return a.first < b.first;
}

int schedule(queue<studyMem>& members, vector<seat>& desks, vector<seat>& rooms, vector<table>& tables) {
	double totalWait = 0;
	double memberSize = members.size();

	while (!members.empty()) {
		studyMem sm = members.front();
		members.pop();
		if (sm.num == 1) {
			seat desk = desks[0];
			int wait_deskTime = (desk.availableTime > sm.arriveTime) ? desk.availableTime - sm.arriveTime : 0;

			int wait_tableTime = INT_MAX;
			int index = -1;
			list<pair<int, int>>::iterator target;
			for (int i = 0; i < tables.size(); i++) {
				int waitTime;
				for (auto it = tables[i].avaTime_space.begin(); it != tables[i].avaTime_space.end(); it++) {
					waitTime = (it->first > sm.arriveTime) ? it->first - sm.arriveTime : 0;
					if (waitTime < wait_tableTime) {
						index = i;
						target = it;
						wait_tableTime = waitTime;
					}
				}
			}

			if (wait_deskTime <= wait_tableTime) {
				totalWait += wait_deskTime;
				desks[0].availableTime = sm.arriveTime + wait_deskTime + sm.studyTime;
				sort(desks.begin(), desks.end(), cmp);
			}
			else {
				totalWait += wait_tableTime;
				tables[index].avaTime_space.push_back(make_pair(sm.arriveTime + wait_tableTime + sm.studyTime, 1));
				int size = target->second - 1;
				int avaTime = target->first;
				tables[index].avaTime_space.erase(target);
				if (size > 0) tables[index].avaTime_space.push_back(make_pair(avaTime, size));
			}
		}
		else {
			int wait_roomTime = INT_MAX;
			int indexRoom = -1;
			for (int i = 0; i < rooms.size(); i++) {
				if (rooms[i].avaSize >= sm.num) {
					wait_roomTime = (rooms[i].availableTime > sm.arriveTime) ? rooms[i].availableTime - sm.arriveTime : 0;
					indexRoom = i;
					break;
				}
			}

			int wait_tableTime = INT_MAX;
			int index = -1;
			for (int i = 0; i < tables.size(); i++) {
				if (tables[i].totalSize < sm.num) continue;
				int waitTime = 0;
				sort(tables[i].avaTime_space.begin(), tables[i].avaTime_space.end(), cmpTable);
				int curSize = 0;
				for (auto it = tables[i].avaTime_space.begin(); it != tables[i].avaTime_space.end() && curSize < sm.num; it++) {
					waitTime += (it->first > sm.arriveTime) ? it->first - sm.arriveTime : 0;
					curSize += it->second;
				}
				if (waitTime < wait_tableTime) {
					waitTime = wait_tableTime;
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
				while (size - tables[index].avaTime_space.front().second > 0) {
					size -= tables[index].avaTime_space.front().second;
					tables[index].avaTime_space.pop_front();
				}
				if (size > 0) tables[index].avaTime_space.front().second -= size;
				tables[index].avaTime_space.push_back(make_pair(sm.arriveTime + wait_tableTime + sm.studyTime, sm.num));
			}
		}
	}
	cout << totalWait << endl;
	return totalWait / memberSize;
}


int main() {
	int n;
	


	system("pause");
	return 0;
}