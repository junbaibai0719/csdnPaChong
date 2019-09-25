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
        # cursor.execute('''create table if not exists offsetdata
        #                (shown_offset char primary key     not null ,
        #                 state int
        #                 );''')
        # #创建表保存文章数据，时间数据类型为timestamp，yyyy-mm-dd hh-mm-ss.sss,使用datetime(timestring)得到yyyy-mm-dd hh-mm-ss.sss形状的日期
        # cursor.execute('''create table if not exists articedata
        #                (article message_text primary key     not null ,
        #                 shown_time timestamp ,
        #                 category char
        #                 );''')
        self.conn.commit()

    def save(self, tablename = 'urldata', list=[]):
        # sqlcode0 = "insert into {} values (?,?)".format(tablename)
        sqlcode0 = "replace into {} values (?,?,?,?,?,?,?,?,?)".format(tablename)
        sqlcode1 = "insert into {} values (?,?,?,?,?,?,?,?,?)".format(tablename)
        # conn = sqlite3.connect(self.database)
        # cursor = conn.cursor()
        # 将url设为主键重复插入时会报错，try用来规避重复插入。
        # cursor.executemany(sqlcode0, (list))
        # try:
        #     cursor.executemany(sqlcode1,(list))
        # except Exception:
        #     print('**********************************************************************************************************')
        for i in list:
            try:
                self.cursor.execute(sqlcode1,(i))
            except Exception:
                if i[1] == 1:
                    self.cursor.execute(sqlcode0,(i))
                    print(i)
        self.conn.commit()

    def read(self, tablename = 'urldata',value = 0):
        # conn = sqlite3.connect(self.database)
        # cursor = conn.cursor()
        data = self.cursor.execute('select * from {} where state = {}'.format(tablename,value))
        self.conn.commit()
        count = data.fetchall()
        return count

    # 访问url函数，如果将一个url取出来访问
    def access(self, tablename = 'urldata',col = 'url'):
        # conn = sqlite3.connect(self.database)
        # cursor = conn.cursor()
        data = self.cursor.execute('select * from {} where state = {}'.format(tablename, 0))
        result = data.fetchmany(20)
        # list = []
        # for i in result:
        #     list.append((1,i[0]))
        # self.cursor.executemany('update {} set state = ? where {} = ?'.format(tablename, col), (list))
        self.conn.commit()
        return result

    # 设置状态
    def set_state(self, tablename, col, colval, state=1):
        self.cursor.execute('update {} set state = ? where {} = ?'.format(tablename, col), (state, colval))
        self.conn.commit()

    def search(self,tablename = 'urldata',what = 'url', col = 'lable' ,colval = ''):
        goturl = self.cursor.execute("select {} from {} where {} like ?".format(what,tablename,col),(colval,)).fetchall()
        self.conn.commit()
        return goturl

    def close(self):
        self.conn.close()



mysql = MySql('test.db')
data = mysql.read(value=1)
# for i in data:
#     print(i)
print(data.__len__())
print(mysql.read().__len__())
print(mysql.search(colval='%work%'))
mysql.close()

