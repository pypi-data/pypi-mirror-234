from langchain.llms.base import LLM
from tketool.lmc.models import LLM_Plus
from langchain.schema.output_parser import BaseOutputParser
import re
from langchain.output_parsers import OutputFixingParser
from langchain.prompts import PromptTemplate
from tketool.logs import log, print_dash_line, log_state


class lmc_linked_model():
    def __init__(self, llm: LLM_Plus):
        self.llm = llm
        self.retry_count = 1
        self.invoke_times = 1
        self.output_parser = None
        self.fix_output_parser = None
        self.prompt_template = None
        self.init_func_list = []
        self.norm_func_list = []
        self.completed_func_list = []
        self.exception_func_list = []

        def model_invoke(ori_prompt, last_output, log):
            log['prompt'] = last_output
            result = self.llm(last_output)
            log['result'] = result
            return result

        self.norm_func_list.append(model_invoke)

    def _fix_output(self, output):
        try:
            result = self.fix_parser.parse(output)
            return result
        except Exception as ex:
            return None

    def set_retry(self, count):
        self.retry_count = count
        return self

    def set_times(self, count):
        self.invoke_times = count
        return self

    def set_prompt_template(self, temp_str):

        def _find_bracket_words(s):
            # 使用正则表达式找出所有大括号内的词语
            words = re.findall(r'\{(.*?)\}', s)

            # 去重并输出
            return list(set(words))

        def prompt_temp(ori_prompt, last_output, log):
            if self.prompt_template is None:
                template_str = temp_str
                template_vars = _find_bracket_words(temp_str)
                template_partial_vars = {}
                if self.output_parser is not None:
                    template_str += "\n{format_instructions}"
                    template_partial_vars['format_instructions'] = self.output_parser.get_format_instructions()
                self.prompt_template = PromptTemplate(
                    template=template_str,
                    input_variables=template_vars,
                    partial_variables=template_partial_vars
                )

            log['type'] = "prompt template generic."
            prompt = self.prompt_template.format(**last_output)
            log['prompt'] = prompt
            return prompt

        self.init_func_list.append(prompt_temp)

        return self

    def set_output_parser(self, out_paser: BaseOutputParser):
        if self.output_parser is not None:
            raise Exception("more than one parser has been set.")

        self.output_parser = out_paser

        def add_parser(ori_prompt, last_output, log):
            log['parser_name'] = type(out_paser).__name__
            log['last_output'] = last_output
            result = out_paser.parse(last_output)
            log['parsed_result'] = result
            return result

        self.norm_func_list.append(add_parser)

        return self

    def set_enum_output_parser(self, enumlist):
        pass

    def set_output_fix(self):
        if self.output_parser is None:
            raise Exception("have not set the output parser.")

        self.fix_output_parser = OutputFixingParser.from_llm(parser=self.output_parser, llm=self.llm)

        def add_fix(ori_prompt, last_output, log):
            log['parser_name'] = type(self.fix_output_parser).__name__
            log['last_output'] = last_output
            result = self.fix_output_parser.parse(last_output)
            log['parsed_result'] = result
            return result

        self.exception_func_list.append(add_fix)

        return self

    def log_state(self):
        log("Summary:", True)
        print_dash_line()
        for k, v in self.llm.state().items():
            log(f"{k}\t:\t{str(v)}", True)

    def _invoke_list_func(self, ori_input, history_output_list, log_list, func_list):
        try:
            for fc in func_list:
                log = {}
                last_output = history_output_list[-1]
                last_output = fc(ori_input, last_output, log)
                history_output_list.append(last_output)
                log_list.append(log)

            return None
        except Exception as ex:
            return ex

    def __call__(self, prompt=None, **kwargs):

        all_logs = []
        result_list = []
        init_result_list = []

        if prompt is None:
            init_result_list.append(kwargs)
        else:
            init_result_list.append(prompt)

        invoke_result = self._invoke_list_func(kwargs, init_result_list, all_logs, self.init_func_list)
        if invoke_result is not None:
            raise invoke_result

        for time_idx in range(self.invoke_times):
            log_dic_list = []
            for retry_id in range(self.retry_count):
                log_state(f"invoke time:{time_idx}, retry:{retry_id}")
                middle_result_list = [init_result_list[-1]]

                normal_invoke_result = self._invoke_list_func(kwargs, middle_result_list, log_dic_list,
                                                              self.norm_func_list)

                if normal_invoke_result is None:
                    result_list.append(middle_result_list[-1])
                    break

                if len(self.exception_func_list) == 0:
                    log_dic_list.append({
                        "error_time": f"time:{time_idx},retry:{retry_id},normal_invoke",
                        "error_msg": str(normal_invoke_result)
                    })
                    log_state(f"invoke time:{time_idx}, retry:{retry_id} failed.")
                    continue

                log_state(f"invoke time:{time_idx}, retry:{retry_id} failed, run fix...")

                exception_invoke_result = self._invoke_list_func(kwargs, middle_result_list, log_dic_list,
                                                                 self.exception_func_list)

                if exception_invoke_result is None:
                    result_list.append(middle_result_list[-1])
                    break
                else:
                    log_dic_list.append({
                        "error_time": f"time:{time_idx},retry:{retry_id},exception_invoke",
                        "error_msg": str(exception_invoke_result)
                    })

                    log_state(
                        f"invoke time:{time_idx}, retry:{retry_id} failed, run fix failed. ex_msg: {str(exception_invoke_result)}")

            all_logs.append(log_dic_list)

        self._invoke_list_func(kwargs, result_list, all_logs, self.completed_func_list)

        return result_list, all_logs
