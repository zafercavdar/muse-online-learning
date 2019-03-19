import datetime

import pandas as pd
from muselsl.stream import list_muses
from muselsl.stream import stream as start_stream


backend = 'gatt'
interface = 'hci0'

muses = list_muses(backend=backend, interface=interface)

all_data = None
batch_data = []


MODE = 'RECORD' # or TEST
MUSE_SAMPLE_RATE = 256
BATCH_SIZE = MUSE_SAMPLE_RATE * 3


subject_index_mapping = {
    0: 'ABDULLAH BUDAN',
    1: 'SAMED BICER'
    2: 'AHMET UYSAL',
    3: 'ZAFER CAVDAR'
    4: 'OZGE AKPINAR'
}


def saver(data):
    global all_data
    print('received {}'.format(data))
    all_data.append(data)


def load_classifier():
    path = '.....'
    model = None
    return model


def lifter(model):

    def test(record):
        batch_data.append(record)
            
        if len(batch_data) == BATCH_SIZE:
            df = pd.DataFrame(batch_data)
            df = df.drop(columns=['timestamp'])
            single_record = df.mean(axis=1)
            subject_pred = model.predict(single_record)[0]
            subject = subject_index_mapping[subject_pred]
            print(subject)
            batch_data = []
    
    return test


if len(muses) > 0:
    muse = muses[0]
    mac_address = muse['address']
    name = muse['name']

    if MODE == 'RECORD':
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
                        callback=saver)

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
    elif MODE == 'TEST':
        model = load_classifier()
        while(True):
            input('Enter to start testing.')
            start_stream(address=mac_address,
                        backend=backend,
                        interface=interface,
                        name=name,
                        callback=lifter(model))
            restart = input('Restart testing? (Y/N): ')
            if restart.upper() == 'Y':
                continue
            else:
                break
        

    else:
        print('MODE {} is not defined.'.format(MODE))
else:
    print('Muse cannot found. Exiting ...')
