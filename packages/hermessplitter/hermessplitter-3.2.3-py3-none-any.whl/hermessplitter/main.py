# from weightsplitter.main import WeightSplitter
import random
import threading

from ws_one_stable.main import WeightSplitter
from traceback import format_exc
from hermessplitter import functions
from hermessplitter.db import db_funcs
from hermessplitter.fast_api import main


class WeightSplitter(WeightSplitter):
    def __init__(self, ip, port, sql_shell,
                 port_name='/dev/ttyUSB0', terminal_name='CAS',
                 debug=False, logger=None, scale_protocol=None,
                 web_port=8003, baudrate=9600, emulate=None):
        # multiprocessing.Process(target=main.run_uvicorn, args=()).start()
        super().__init__(ip, port, debug=debug, port_name=port_name,
                         terminal_name=terminal_name, logger=logger,
                         scale_protocol=scale_protocol, baudrate=baudrate,
                         emulate=emulate)
        self.notes = ''
        self.active = False
        self.blocked = False
        # threading.Thread(target=self.start_fast_api, args=()).start()
        self.kf = 0
        self.hermes_weight = 0
        self.avg_tara = 0
        self.max_brutto = 0
        self.avg_weight = 0
        self.test_mode = self.define_if_test_mode()
        self.wdb_sqlshell = sql_shell
        self.ar = None  # not realized
        threading.Thread(target=functions.import_clients,
                         args=(self.wdb_sqlshell,)).start()
        threading.Thread(target=functions.import_auto,
                         args=(self.wdb_sqlshell,)).start()
        threading.Thread(target=main.run_uvicorn, args=(web_port,)).start()

    def block_auto_null(self):
        self.blocked = True

    def start_fast_api(self, port):
        main.run_uvicorn(port)

    def define_if_test_mode(self):
        result = db_funcs.get_test_mode()
        result_frmt = int(result[0])
        if result_frmt:
            return True

    def make_new_record(self, car_number, carrier, record_id):
        if self.blocked:
            return
        super().make_new_record(car_number, carrier, record_id)
        # self.set_status(True)
        self.activate(carnum=car_number, record_id=record_id,
                      client=carrier)

    def make_final_record(self, weight, record_id):
        self.make_log_hermes_db(weight, record_id=record_id)

    def turn_off_logging(self):
        self.blocked = False
        self.set_status(False)

    def activate(self, carnum, record_id, client=None):
        """ Активировать HERMES """
        if functions.check_hermes_active():
            self.record_id = record_id
            # kf = functions.get_kf(self.wdb_sqlshell, carrier=client)
            kf = db_funcs.get_auto_kf_by_car_number(carnum)
            if kf and not kf[0]:
                kf = db_funcs.get_client_kf_by_ex_id(client)
            try:
                if kf:
                    kf = kf[0] * 0.01
                else:
                    return
            except:
                return
            print('Получен KF Hermes =', kf)
            avg_tara = functions.get_avg_tara(self.wdb_sqlshell, carnum)
            max_brutto = functions.get_max_weight(self.wdb_sqlshell, carnum)
            avg_weigth = functions.get_avg_weight(self.wdb_sqlshell, carnum)
            self.notes = ''
            self.allowed_kf = random.randrange(50, 100)
            self.set_kf(kf)
            self.set_status(True)
            self.set_debug(self.debug)
            self.set_avg_tara(avg_tara)
            self.set_max_brutto(max_brutto)
            self.set_avg_weigth(avg_weigth)

    def set_kf(self, kf):
        self.show_print('setting kf', kf, debug=True)
        self.kf = 1.0 + kf

    def set_debug(self, debug):
        self.debug = debug

    def set_status(self, status):
        self.show_print('settings status', status, debug=True)
        self.active = status
        if not status:
            self.hermes_weight = 0

    def set_avg_tara(self, avg_tara):
        try:
            self.avg_tara = int(avg_tara)
        except:
            self.show_print(self.avg_tara, '-  ЭТО НЕ ЧИСЛО')
            self.avg_tara = 0

    def set_max_brutto(self, max_brutto):
        try:
            self.max_brutto = int(max_brutto)
        except:
            self.max_brutto = 0
        self.netto_max = self.max_brutto - self.avg_tara

    def send_data(self, data):
        data = self.make_magic(data)
        super().send_data(data)

    def set_avg_weigth(self, weight):
        try:
            self.avg_weight = int(weight)
        except:
            self.show_print(self.avg_weight, '-  ЭТО НЕ ЧИСЛО')
            self.avg_weight = 0

    def make_magic(self, data):
        if self.test_mode:
            print('\n[TEST] self.active', self.active)
            print('[TEST] isinstance(data, str)', isinstance(data, str))
            print('[TEST] isinstance(data, int)', isinstance(data, int))
            print('[TEST] self.avg_tara', self.avg_tara != 0)
            print('[TEST] self.max_brutto', self.max_brutto != 0)
            print('[TEST] self.avg_weight', self.avg_weight != 0)
            print('[TEST] int(data) > 300', int(data) > 300)
            print('[TEST] test_mode', self.test_mode)
        try:
            if self.active and (isinstance(data, str) or isinstance(data, int)) \
                    and self.max_brutto != 0 and self.avg_weight != 0 \
                    and int(data) > 300:
                print('\nHERMES WORK.\nDATA:{}'.format(data))
                if self.avg_tara == 0:
                    self.notes = 'Машина заехала впервые'
                    return str(data)
                data = int(data)
                if data < 0:
                    return str(data)
                # Вычитываем приблизительное (ожидаемое нетто)
                approx_netto = float(data) - float(self.avg_tara)
                self.notes = f'Ожидаемое нетто - {int(approx_netto)} кг ||'
                if approx_netto < 0:
                    self.notes += 'Ожидаемое нетто ниже 0'
                    return str(data)
                self.show_print('approximate cargo is', approx_netto)
                # self.kf ~ 1.2. Получаем вес, который мы накинем на ожидаемое нетто
                delta_k = approx_netto * float(self.kf) - approx_netto  # 400kg
                self.show_print('new delta_k', delta_k)
                """ Проверяем не выше ли то, что мы накинем того, что мы накинули
                бы на средний вес """
                delta_k = abs(delta_k)
                print('data', data)
                # 5 положение
                if int(delta_k) > 0:
                    new_data = float(data) + float(delta_k)
                    print('new_data', new_data)
                else:
                    new_data = data
                    self.notes += f'\nДельта около 0 ({delta_k}), KF={self.kf} || '
                # 2 положение
                if data > self.max_brutto:
                    self.notes += f"Текущий вес {data}, больше максимального {self.max_brutto} || "
                    new_data = data
                else:
                    if float(new_data) > float(self.max_brutto):  # 2 Положение
                        print("NEW DATA", new_data)
                        print("MAX_BRUTTO", self.max_brutto)
                        self.notes += f"\nВес {int(new_data)} больше макс.брутто ({self.max_brutto})! "
                        allowed_range = self.max_brutto - data
                        allowed_delta = allowed_range * self.allowed_kf * 0.01
                        #allowed_delta = random.randrange(int(allowed_range/3),
                        #                                   int(allowed_range))
                        new_data = data + allowed_delta
                        self.notes += f". Накинули {allowed_delta}. (Диапазон от {int(allowed_range/3)} до {allowed_range})"
                        #new_data = self.max_brutto - random.randrange(10,
                        #                                              40)  # 7100, 7190
                        if new_data < data:
                            self.notes += f"\nСработала проверка на отрицательнкую накидку"
                            new_data = data
                new_data = str(self.make_data_aliquot(new_data))
                self.hermes_weight = int(new_data) - int(data)
                if int(new_data) < int(data):
                    new_data = data
                # Если то, что мы накинем, больше чем двойной кф, вернуть обычный
                if int(new_data) > (int(data) * self.kf):
                    self.notes = '\nНакидка больше, чем максимальная дельта по кф'
                    print(self.notes)
                    print('New data', new_data)
                    print('Old data', data)
                    return str(data)
            else:
                new_data = str(data)
        except:
            new_data = str(data)
            self.show_print(format_exc())
            self.notes = 'Ошибка: {}'.format(format_exc())
        if self.test_mode:
            new_data = data
            self.notes += 'Тестовый режим'
        #print(self.notes)
        #print('New data:', new_data)
        #print('Old data:', data)
        return str(new_data)

    def make_log_hermes_db(self, final: int, hermes: int = None,
                           record_id=None):
        if not record_id:
            record_id = self.record_id
        if not self.active:
            return
        if not hermes:
            hermes = int(self.hermes_weight)
        try:
            db_funcs.create_new_record(record_id=record_id,
                                       clear_gross=final - hermes,
                                       hermes_gross=hermes,
                                       final_gross=final,
                                       test_mode=self.test_mode,
                                       notes=self.notes,
                                       kf_must_be=self.kf
                                       )
        except:
            print(format_exc())

    def make_netto_less(self, added, br_diff, kf):
        delta_k = added * kf
        if delta_k > br_diff:  # решить с кэфом
            over = delta_k - br_diff
            delta_k = delta_k - over * 1.1
        return delta_k
