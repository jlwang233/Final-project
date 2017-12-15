import numpy as np
import math
import random
import pandas as pd


class Seat:
    """ An OO class to create a seat unit
    seat_id 1-50 are desk
    seat_id

    """
    #
    def __init__(self, seat_id, seat_type):
        """

        :param seat_id: an integer containing id of seat
        :param seat_type: a string containing type of seat
        """
        self.seat_id = seat_id
        self.size = 0
        self.seat_type = seat_type
        self.taken = 0

    def get_seat_id(self):
        """
        >>> Seat(3,'desk').get_seat_id()
        3
        """
        return self.seat_id

    def get_seat_type(self):
        """
        :return: a string containing type of the seat

        >>> Seat(3,'desk').get_seat_type()
        'desk'

        """

        return self.seat_type

    def get_seat_size(self):
        """
        :return: an integer containing size of the seat

        >>> Seat(3,'desk').get_seat_size()
        1
        >>> Seat(90,'table').get_seat_size()
        6


        """
        if self.seat_type == 'desk':
            self.size = 1
        else:
            self.size = 6
        return self.size

    def add_new(self, new_study_size):
        """

        :param new_study_size: an integer containing enter study unit size

        >>> a=Seat(120,'table')
        >>> a.add_new(4)
        >>> a.taken
        4
        """
        self.taken += new_study_size

    def remove_old(self,exit_study_size):
        """

        :param exit_study_size: an integer containing exit study unit size
        """
        self.taken -= exit_study_size

    def occupied(self):
        """

        :return: a boolean representing whether the seat is fully occupied or not

        >>> a = Seat(3,'desk')
        >>> a.add_new(1)
        >>> a.occupied()
        True
        >>> a = Seat(3,'desk')
        >>> a.add_new(2)
        >>> a.occupied()
        Traceback (most recent call last):
        ...
        ValueError
        >>> a = Seat(95,'room')
        >>> a.add_new(3)
        >>> a.occupied()
        True
        >>> a = Seat(120,'table')
        >>> a.add_new(3)
        >>> a.occupied()
        False
        """

        if self.get_seat_type() in ['room','desk']:
            if self.taken > 0:
                return True
            elif self.taken == 0:
                return False

        elif self.get_seat_type() == 'table':
            if self.taken == self.size:
                return True
            else:
                return False

    def left(self):
        """ only applicable to table

        :return: an integer containing amount of room left in a seat
        >>> a = Seat(120,'table')
        >>> a.add_new(3)
        >>> a.left()
        3
        >>> a.add_new(1)
        >>> a.seat_left()
        2
        >>> b = Seat(90,'room')
        >>> b.add_new(3)
        >>> b.left()
        0


        """
        if self.get_seat_type() == 'table':
            return self.get_seat_size() - self.taken

        else:
            if self.taken != 0:
                return 0
            elif self.taken == 0:
                return self.get_seat_size()



class Study:
    # An OO class to create a study unit
    def __init__(self, study_id):
        """

        :param study_id: an integer containing ID of the study unit
        """
        self.ID = study_id
        self.size = np.random.choice([1, 1, 1, 1, 1, 2, 3, 4, 5, 6])
        self.timeSpend = math.ceil(np.random.chisquare(5, size=None)) * 20
        self.timeEnter = 0
        self.seatAssigned = 0
        self.study_type = None

    def get_study_id(self):
        """

        :return: an integer containing the ID of the study unit
        >>> Study(3).get_study_id()
        3
        """
        return self.ID

    def get_study_size(self):
        """

        :return: an integer containing the size of the study unit
        >>> a = Study(3).get_study_size
        >>> a in [1, 2, 3, 4, 5, 6]
        True
        """

        return self.size

    def get_study_seat(self):
        """

        :return: an integer containing the ID of the seat assigned
        >>> a = Study(3)
        >>> a.seatAssigned = 3
        >>> a.get_study_seat()
        3
        """
        return self.seatAssigned

    def get_time_spend(self):
        """

        :return: return an integer containing time spent in library
        >>> a = Study(3).get_time_spend()
        >>> type(a) == int
        True
        """
        return self.timeSpend

    def get_study_type(self):
        """

        :return: return a string containing the type of the study unit
        >>> a = Study(3).get_study_type()
        >>> a in ['individual', 'group']
        True
        """
        if self.size == 1:
            self.study_type = 'individual'
        else:
            self.study_type = 'group'

        return self.study_type

    def time_stamp(self):
        """

        :rtype: int
        :return: an integer containing time when study unit enter the queue
        >>> Study(3).time_stamp()
        15
        """
        return self.ID * 5

    def time_enter(self):
        """

        :return: an integer containing time when study unit enter the seat
        >>> a = Study(3)
        >>> a.timeEnter = 60
        >>> a.time_enter()
        60
        """
        return self.timeEnter

    def time_exit(self):
        """

        :return: an integer containing time when study unit exit the seat
        >>> a = Study(3)
        >>> a.timeEnter = 60
        >>> b = a.time_exit()
        >>> b > a.time_enter()
        True
        """
        return self.timeEnter + self.timeSpend

    def wait_time(self):
        """

        :return: an integer containing minutes of time waiting in queue
        >>> a = Study(3)
        >>> a.timeEnter = 60
        >>> a.wait_time()
        45
        """
        return self.time_enter() - self.time_stamp()


class Simulation:
    def __init__(self,new_study_id):
        self.seats = []
        self.study_record = []
        self.exit_time = pd.DataFrame(columns=['StudyID','SeatID','StudySize','timeExit'])
        self.new_study_id = new_study_id

    @staticmethod
    def seat_arrange(a, b, c):
        """ arrange the seats in the library with sear_id and seat_type

        :param a: an integer containing end number of desk
        :param b: an integer containing end number of room
        :param c: an integer containing end number of table
        """
        seats = []
        for i in range(a):
            seats.append(Seat(i+1, 'desk'))
        for i in range(a, b):
            seats.append(Seat(i+1, 'room'))
        for i in range(b, c):
            seats.append(Seat(i+1, 'table'))

    def study_record(self, study_id):
        self.study_record.append(Study(study_id))


    def seat_assign(self, study: Study, seat:Seat):
        study.seatAssigned = seat.seat_id
        study.timeEnter = study.time_stamp()
        seat.add_new(study.get_study_size())
        self.exit_time_record(study)


    def study_enter(self, study:Study):
        if study.get_study_size() == 1:
            wait_individual = [astudy for astudy in self.study_record if astudy.size == 1
                               and astudy.seatAssigned is None]
            if len(wait_individual) == 0:
                for seat in self.seats:
                    if seat.get_seat_type() in ['desk','table']:
                        if seat.occupied() is False:
                            self.seat_assign(study,seat)
                            break


        if study.get_study_size() > 1:
            wait_group = [astudy for astudy in self.study_record if astudy.size > 1
                          and astudy.seatAssigned is None]
            if len(wait_group) == 0:
                for seat in self.seats:
                    if seat.get_seat_type() in ['room','table']:
                        if seat.seat_left() >= study.get_study_size():
                            self.seat_assign()
                            break

    def exit_time_record(self, study: Study):
        col_name = ['StudyID', 'SeatID', 'StudySize', 'timeExit']
        new_record = pd.DataFrame([[study.get_study_id(), study.get_study_seat(), study.get_study_size(),
                                    study.time_exit()]], columns=col_name)
        self.exit_time = self.exit_time.append(new_record, columns= col_name)

    def study_exit(self, study: Study):
        a = study.get_study_seat()
        self.seats[a-1].remove_old(study.get_study_size())

        if self.seats[a-1].get_seat_id == 'desk':
            for study in self.study_record:
                if study.size == 1 and study.seatAssigned is None:
                    self.seat_assign(study,self.seats[a-1])
                    break

        if self.seats[a-1].get_seat_id == 'room':
            for study in self.study_record:
                if study.size > 1 and study.seatAssigned is None:
                    self.seat_assign(study, self.seats[a - 1])
                    break

        if self.seats[a-1].get_seat_id == 'table':
            left_size = self.seats[a-1].left
            for study in self.study_record:
                if study.seatAssigned is None:
                    if study.get_study_size() <= left_size:
                        self.seat_assign(study, self.seats[a-1])
                        break

    def simulator(self):
        for i in range(self.new_study_id*5):


















