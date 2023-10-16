import threading, time
from queue import Queue
from collections import OrderedDict


class AtomicCounter:
    def __init__(self):
        self.value = 0
        self._lock = threading.Lock()

    def increment(self, add_value=1):
        with self._lock:
            self.value += add_value
            return self.value

    @property
    def Value(self):
        return self.value


def do_multitask(iterations, task_fun, thread_count=3, max_queue_buffer=0):
    task_lock = threading.Lock()
    # 创建任务队列和结果集
    task_q = Queue(maxsize=max_queue_buffer)
    results = OrderedDict()
    task_done_event = threading.Event()

    counter = AtomicCounter()

    def worker():
        while True:
            index, item = task_q.get(block=True)
            if item is None:
                break
            result = task_fun(item)
            with task_lock:
                results[index] = result
            task_done_event.set()
            task_q.task_done()
        counter.increment()

    def put_task():
        # 将任务放入队列
        for index, item in enumerate(iterations):
            task_q.put((index, item), block=True)
        for _ in range(thread_count):  # 在队列中加入None，以通知所有工作线程退出
            task_q.put((None, None))
        #print("put exit")
        task_done_event.set()

    Insert_thread = threading.Thread(target=put_task)
    Insert_thread.start()

    # 启动工作线程
    threads = []
    for _ in range(thread_count):
        t = threading.Thread(target=worker)
        t.start()
        threads.append(t)

    outer_index = 0
    while True:
        task_done_event.wait(timeout=1)
        task_done_event.clear()
        while True:
            with task_lock:
                if outer_index in results:
                    yield results[outer_index]
                    del results[outer_index]
                    outer_index += 1
                else:
                    break

        if counter.Value == thread_count:
            break


# def ddd(a):
#     time.sleep(0.5)
#     return a + 10
#
#
# for p in do_multitask([1,2,3,4,5,6,7,8,9], ddd, max_queue_buffer=5):
#     print(p)
#
# time.time()
