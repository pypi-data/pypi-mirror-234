import contextlib
import datetime
from datetime import datetime as DateTime
import glob
import os
from pathlib import Path
import re
import time

def progress_bar(width, done, total, T1, T3, str='', prefix=''):
    ration = total / width
    t = int(round(done / ration))
    v = done / T1
    per = round((done / total) * 100)
    T2 = int(round((total - done) / v))
    day1 = int(T1 // 86400)
    day2 = T2 // 86400
    print(
        f'\r{prefix}' +
        f'{per:3d}%|{"▉" * t}{" " * (width - t)}| {done}/{total} ' +
        f'[{day1} {time.strftime("%H:%M:%S", time.gmtime(T1))} < {day2} {time.strftime("%H:%M:%S", time.gmtime(T2))}] ' +
        f'({round(v, 3):.1f} it/s) ', f'({round(T3 * 1000, 3):.1f} ms/it)', str, end='')

def increment_path(path, exist_ok=False, sep=''):
    # Increment path, i.e. runs/exp --> runs/exp{sep}0, runs/exp{sep}1 etc.
    path = Path(path)  # os-agnostic
    if (path.exists() and exist_ok) or (not path.exists()):
        return str(path)
    else:
        dirs = glob.glob(f"{path}{sep}*")  # similar paths
        matches = [re.search(rf"%s{sep}(\d+)" % path.stem, d) for d in dirs]
        i = [int(m.groups()[0]) for m in matches if m]  # indices
        n = max(i) + 1 if i else 2  # increment number
        return f"{path}{sep}{n}"  # update path

def check_path(path):
    if not os.path.exists(path):
        os.makedirs(path)

def create_tplt(num, width):
    # sample num = 8, width = 10
    # tplt = "{0:^10}\t{1:^10}\t{2:^10}\t{3:^10}\t{4:^10}\t{5:^10}\t{6:^10}\t{7:^10}"
    tplt = ''
    for i in range(num):
        if i == 0:
            tplt += '{'+str(i)+':^'+str(width)+'}'
        else: 
            tplt += ' {'+str(i)+':^'+str(width)+'}'
    return tplt

def delete_file(filepath):
    if (os.path.exists(filepath)) :
        #存在，则删除文件
        os.remove(filepath)



@contextlib.contextmanager
def mock_now(dt_value):  # type: ignore
    """Context manager for mocking out datetime.now() in unit tests.

    Example:
    with mock_now(datetime.datetime(2011, 2, 3, 10, 11)):
        assert datetime.datetime.now() == datetime.datetime(2011, 2, 3, 10, 11)
    """

    class MockDateTime(datetime.datetime):
        """Mock datetime.datetime.now() with a fixed datetime."""

        @classmethod
        def now(cls):  # type: ignore
            # Create a copy of dt_value.
            return DateTime(
                dt_value.year,
                dt_value.month,
                dt_value.day,
                dt_value.hour,
                dt_value.minute,
                dt_value.second,
                dt_value.microsecond,
                dt_value.tzinfo,
            )

    real_datetime = datetime.datetime
    datetime.datetime = MockDateTime
    try:
        yield datetime.datetime
    finally:
        datetime.datetime = real_datetime
