import datetime

import pandas as pd
from muselsl.stream import list_muses
from muselsl.stream import stream as start_stream

backend = 'gatt'
interface = 'hci0'

muses = list_muses(backend=backend, interface=interface)

all_data = None

def handler(data):
    print('received {}'.format(data))
    all_data.append(data)


if len(muses) > 0:
    muse = muses[0]
    mac_address = muse['address']
    name = muse['name']
    while(True):
        global all_data
        # get experiment information
        subject = input('Name of the subject: ')
        state = input('Name of the state: ')
        all_data = []

        input('Enter to start recording.')

        # blocking call
        start_stream(address=mac_address,
                    backend=backend,
                    interface=interface,
                    name=name,
                    callback=handler)

        should_save = input('Save the data? (Y/N): ')
        if should_save == 'Y' or should_save == 'y':
            df = pd.DataFrame(all_data)
            now = datetime.datetime.now()
            date = '{}-{}-{}'.format(now.year, now.month, now.day)
            filename = '{}_{}_{}.csv'.format(subject.upper(), state.upper(), date)
            df.to_csv(filename, sep='\t')
            print('Data is saved to {}'.format(filename))

        new_measurement = input('New measurement? (Y/N): ')
        if new_measurement == 'Y' or new_measurement == 'y':
            continue
        else:
            break
else:
    print('Muse cannot found. Exiting ...')
