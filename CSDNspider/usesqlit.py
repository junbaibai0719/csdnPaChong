import sqlite3

class MySql():
    def __init__(self, database):
        # 连接数据库
        self.database = database
        self.conn = sqlite3.connect(self.database)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''create table if not exists urldata
                       (url char primary key     not null ,
                        state int,
                        title message_text ,
                        nickname nchar ,
                        shown_year year ,
                        showm_month month ,
                        shown_day day ,
                        shown_time time , 
                        lable message_text 
                        );''')
        self.conn.commit()

    def save(self, tablename = 'urldata', list=[]):
        sqlcode0 = "replace into {} values (?,?,?,?,?,?,?,?,?)".format(tablename)
        sqlcode1 = "insert into {} values (?,?,?,?,?,?,?,?,?)".format(tablename)
        for i in list:
            try:
                self.cursor.execute(sqlcode1,(i))
            except Exception:
                if i[1] == 1:
                    self.cursor.execute(sqlcode0,(i))
                    print(i)
        self.conn.commit()

    def read(self, tablename = 'urldata'):
        # conn = sqlite3.connect(self.database)
        # cursor = conn.cursor()
        data = self.cursor.execute('select * from {} where state =0'.format(tablename))
        self.conn.commit()
        count = data.fetchall()
        return count

    # 访问url函数，如果将一个url取出来访问
    def access(self, tablename = 'urldata',col = 'url'):
        data = self.cursor.execute('select * from {} where state = {}'.format(tablename, 0))
        result = data.fetchmany(30)
        self.conn.commit()
        return result

    # 设置状态
    def set_state(self, tablename, col, colval, state=1):
        self.cursor.execute('update {} set state = ? where {} = ?'.format(tablename, col), (state, colval))
        self.conn.commit()

    def search(self,tablename = 'urldata',col = 'url',colval = ''):
        self.cursor.execute('select {} from {} where {} like {}')

    def close(self):
        self.conn.close()

