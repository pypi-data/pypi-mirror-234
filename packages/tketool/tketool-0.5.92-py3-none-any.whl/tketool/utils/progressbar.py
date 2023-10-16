import math, sys, time
from collections.abc import Iterable

process_bar_current = None


def get_process_bar_current():
    global process_bar_current
    return process_bar_current


class process_status_bar:
    """
    控制台的进度条
    """

    def __init__(self, processbar_length=20):
        """
        初始化函数
        :param processbar_length: 进度条长度（打印长度）
        """
        self._iter_stack = []
        self._process_bar_len = processbar_length
        self._print_str = ""
        self._print_logs = []

        # set a mark of log
        global process_bar_current
        process_bar_current = self

    def _cast_second_strformat(self, sec):
        m, s = divmod(sec, 60)
        h, m = divmod(m, 60)
        return "%02d:%02d:%02d" % (h, m, s)

    def _flush_(self):

        if len(self._iter_stack) == 0:
            sys.stdout.write('\r')
            sys.stdout.write("                                                      ")
            sys.stdout.flush()
            return

        stack_str = ""
        for iter_i in range(len(self._iter_stack) - 1):
            p_value = self._iter_stack[iter_i]['value'] / float(self._iter_stack[iter_i]['max'])
            p_value = "%.2f" % (p_value * 100)
            p_count = f"{self._iter_stack[iter_i]['value']}/{self._iter_stack[iter_i]['max']}"

            if self._iter_stack[iter_i]['value'] != 0:
                avg_cost = self._iter_stack[iter_i]['avg_cost']
                b_dic = self._iter_stack[iter_i]
                sur_plus = avg_cost * b_dic['max'] - time.time() + b_dic['start']
                time_show = f" {self._cast_second_strformat(avg_cost)},{self._cast_second_strformat(sur_plus)}"
            else:
                time_show = "-:-:-,-:-:-"

            stack_str += f"[{self._iter_stack[iter_i]['key']}  {p_count}  {p_value}%({time_show})] >>"
            pass

        current_item = self._iter_stack[-1]
        p_value = 0 if float(current_item["max"]) == 0 else current_item["value"] / float(current_item["max"])
        p_value_str = "%.2f" % (p_value * 100)

        bar_size = math.floor(p_value * self._process_bar_len)

        bar_str = ""
        for i in range(self._process_bar_len):
            if i + 1 <= bar_size:
                bar_str += "*"
            else:
                bar_str += " "

        if current_item['value'] != 0:
            avg_cost = current_item['avg_cost']
            sur_plus = current_item['plus_cost']
            time_show = f"{self._cast_second_strformat(avg_cost)},{self._cast_second_strformat(sur_plus)}"
        else:
            time_show = "-:-:-,-:-:-"

        bar_str = f'{stack_str} {current_item["key"]} {current_item["value"]}/{current_item["max"]}  [{bar_str}]{p_value_str}% [{time_show}] - {self._print_str} '

        if len(self._print_logs) == 0:
            sys.stdout.write('\r' + bar_str)
        else:
            sys.stdout.write('\r')
            for s in self._print_logs:
                sys.stdout.write(s + "\n")
            self._print_logs.clear()
            sys.stdout.write(bar_str)
        sys.stdout.flush()

    def iter_bar(self, iter_item, value=0, key=None, max=None):
        """
        进度条的遍历方法
        :param iter_item: 主遍历对象
        :param value: value起始
        :param key: 遍历名称
        :param max: 遍历的数量
        :return: 可遍历对象
        """

        def get_length(iter_item):
            if isinstance(iter_item, Iterable):
                try:
                    return len(iter_item)
                except TypeError:
                    # 'iter_item' is an iterable but doesn't have a __len__ method.
                    # It could be something like an infinite generator.
                    raise Exception("该对象为无限长度的可迭代对象")
            else:
                raise Exception("需要指定max值")

        if max is None:
            max = get_length(iter_item)

        self.start(key, max, value)
        for _iter in iter_item:
            yield _iter
            self.one_done()

        self.stop_current()

    def start(self, key, max, value=0):
        if key is None:
            key = f"Iter {len(self._iter_stack)}"
        self._iter_stack.append({
            'key': key,
            'value': value,
            'max': max,
            'start': time.time(),
            'avg_cost': 0,
            'plus_cost': 0
        })
        self._flush_()

    def set_value(self, v):
        self._iter_stack[-1]['value'] = v

        if self._iter_stack[-1]['value'] != 0:
            avg_cost = (time.time() - self._iter_stack[-1]['start']) / self._iter_stack[-1]['value']
            sur_plus = avg_cost * (self._iter_stack[-1]['max'] - self._iter_stack[-1]['value'])
            self._iter_stack[-1]['avg_cost'] = avg_cost
            self._iter_stack[-1]['plus_cost'] = sur_plus
        else:
            self._iter_stack[-1]['avg_cost'] = 0
            self._iter_stack[-1]['plus_cost'] = 0

        self._flush_()

    def one_done(self):
        self.set_value(self._iter_stack[-1]['value'] + 1)

    def stop_current(self):
        self._iter_stack.pop(-1)
        self._flush_()

        # clear a mark of log
        if len(self._iter_stack) == 0:
            global process_bar_current
            process_bar_current = None

    # def update_process_value(self, v):
    #     """
    #     强制更新进度条的进度数值
    #     :param v: 要更新的数值
    #     :return: 无返回
    #     """
    #     self._iter_stack[-1]['value'] = v

    def process_print(self, str):
        """
        打印过程中的状态信息（覆盖输出）
        :param str: 状态信息
        :return: 无返回
        """
        self._print_str = str
        self._flush_()

    def print_log(self, str):
        """
        过程中打印log（不覆盖，使用换行）
        :param str: 状态信息
        :return: 无返回
        """
        self._print_logs.append(str+"\n")
        self._flush_()
