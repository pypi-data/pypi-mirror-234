from hermessplitter.main import WeightSplitter
import unittest
import threading
from wsqluse.wsqluse import Wsqluse


class MainTest(unittest.TestCase):
    sql_shell = Wsqluse(dbname="gdb",
                        password="0kra1na&73",
                        host="localhost",
                        user="qodex")

    def __init__(self, *args, **kwargs):
        super(MainTest, self).__init__(*args, **kwargs)


    def test_a(self):
        self.hs = WeightSplitter(ip='127.0.0.1', port=5432,
                                 debug=True, terminal_name="CAS",
                                 sql_shell=self.sql_shell)
        self.hs.activate(carnum='А319ЕК702', client=1, record_id=12)
        all_data = ['0', '-50', '10', '40', '8700', '8800', '8820', '8810', '8810', '8810']
        #all_data = ["17000"]
        magic_data = []
        for data in all_data:
            response = self.hs.make_magic(data)
            magic_data.append(response)
        count = 0
        for d in all_data:
            print(d, magic_data[count])
            count += 1
        #print("MAGIC DATA", dict(zip(all_data, magic_data)))


if __name__ == '__main__':
    unittest.main()