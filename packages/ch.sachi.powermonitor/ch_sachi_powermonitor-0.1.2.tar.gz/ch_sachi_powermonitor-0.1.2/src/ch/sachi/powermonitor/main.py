import configparser
import datetime
import logging
import os
import sqlite3
from typing import List

from victron_ble.devices import BatteryMonitorData

from ch.sachi.powermonitor.powerdata_reader import PowerdataReader
from ch.sachi.powermonitor.restServicePowerdata import RestServicePowerdata


class Config:
    def __init__(self, id: str, key: str):
        if id is None or key is None:
            raise ValueError('We need id and key')
        self.id = id
        self.key = key


def read_config() -> Config:
    config = configparser.ConfigParser()
    config.read('powermonitor.cfg')
    if not config.has_section('powermonitor'):
        raise ValueError('no section powermonitor')
    default = config['powermonitor']
    return Config(default.get('id'), default.get('key'))


class MonitorRepository:
    def __init__(self, database=None):
        self.database = database

    def init(self) -> None:
        if os.path.isfile(self.database):
            logging.debug('Database ' + self.database + 'does exist already')
            return

        logging.debug('Initialize database ' + self.database)
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS powermon (
                    id INTEGER PRIMARY KEY,
                    created_at TIMESTAMP NOT NULL,
                    current real NOT NULL,
                    voltage real NOT NULL,
                    soc real NOT NULL,
                    consumed_ah real NOT NULL,
                    second_voltage real NOT NULL
                    )''')

    def write(self, data: BatteryMonitorData):
        if data is None:
            return
        logging.info('Save to database')
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            now = datetime.datetime.now()
            cur.execute('''INSERT INTO powermon(
                created_at, 
                current, 
                voltage, 
                soc, 
                consumed_ah, 
                second_voltage) 
                values(?, ?, ?, ?, ?, ?)
                ''',
                        (
                            now,
                            data.get_current(),
                            data.get_voltage(),
                            data.get_soc(),
                            data.get_consumed_ah(),
                            data.get_starter_voltage()
                        )
                        )

    def get_measures_after(self, last: str) -> List:
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT "
                "m.created_at, "
                "m.current, "
                "m.voltage, "
                "m.soc, "
                "m.consumed_ah, "
                "m.second_voltage "
                "from powermon m "
                "where m.created_at >= datetime(?, '+1 second')",
                last
            )
            records = cur.fetchall()
            measures_data = []
            for record in records:
                data = {
                    'created_at': record[0],
                    'current': str(record[1]),
                    'voltage': str(record[2]),
                    'soc': str(record[3]),
                    'consumed_ah': str(record[4]),
                    'second_voltage': str(record[5])
                }
                measures_data.append(data)
            return measures_data


def create_monitor_repository() -> MonitorRepository:
    return MonitorRepository('powermon.db')


def main():
    config = read_config()
    repo = create_monitor_repository()
    repo.init()
    data_reader = PowerdataReader(config.id, config.key)
    result = data_reader.read()
    if result is not None:
        repo.write(result)


def publish():
    config = read_config()
    repo = create_monitor_repository()
    repo.init()
    service = RestServicePowerdata('', '', '')
    last = service.get_last_timestamp()
    measures_to_post = repo.get_measures_after(last)
    if len(measures_to_post) > 0:
        logging.info('Posting ' + str(measures_to_post) + "'")
        service.post_measures(measures_to_post)


if __name__ == '__main__':
    main()
if __name__ == '__publish__':
    publish()
