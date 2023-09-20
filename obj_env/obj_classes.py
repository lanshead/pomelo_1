class PositionComp:
    def __init__(self, objid, name):
        self.objid = objid
        self.name = name
        self.stat_pos = 0
        self.sql_pos = 0

    def __repr__(self):
        return f'<{self.name}, {self.objid}, дельта = {self.eq_pos}, sql_data = {self.sql_pos}, потеря позиций {round(self.eq_pos / self.sql_pos * 100, 2)}% >'

    def __eq__(self, other):
        if isinstance(other, PositionComp):
            return self.objid == other.objid
        elif isinstance(other, int):
            return self.objid == int
        return NotImplemented

    def add_stat_pos(self, stat_pos):
        self.stat_pos = stat_pos

    def add_sql_pos(self, sql_pos):
        self.sql_pos = sql_pos

    @property
    def eq_pos(self):
        return self.sql_pos - self.stat_pos

