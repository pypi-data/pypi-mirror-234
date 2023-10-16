from tketool.files import *
from tketool.lmc.prompts.prompt_controller import *
from tketool.lmc.tasks.translate import translate
from tketool.lmc.tasks.task_init import get_init_llm
from tketool.utils.progressbar import process_status_bar


def update_prompt_folder(root_folder, llm=None):
    """
    update all prompt translate to other language
    root_folder : prompt template folder
    """
    if llm is None:
        llm = get_init_llm()

    # read all content
    all_content = {name: {} for _, name in enum_directories(root_folder)}
    all_langs = [k for k in all_content.keys()]

    for lang in all_langs:
        for fpath, fname in enum_files(os.path.join(root_folder, lang)):
            prompt_key = fname.split('.')[0]
            all_content[lang][prompt_key] = read_prompt_file(fpath)

    # update
    finished_prompt = set()
    worklist = []
    for lang in all_langs:
        for kk, vv in all_content[lang].items():
            if kk in finished_prompt:
                continue
            standard_ver = vv['version']
            stardard_item = vv
            # find last version
            for lang2 in all_langs:
                if kk in all_content[lang2]:
                    if float(all_content[lang2][kk]['version']) > float(standard_ver):
                        standard_ver = all_content[lang2][kk]['version']
                        stardard_item = all_content[lang2][kk]

            # create task
            for lang2 in all_langs:
                if kk not in all_content[lang2] or float(standard_ver) > float(all_content[lang2][kk]['version']):
                    worklist.append((kk, lang2, stardard_item))

            finished_prompt.add(kk)

    pb = process_status_bar()
    # do task
    for key, tolang, item in pb.iter_bar(worklist, key="translate task"):
        translate_str = translate(tolang, item['templatestr'], tllm=llm)
        path = os.path.join(root_folder, tolang, f"{key}.txt")
        if translate_str is None:
            raise Exception("translate failed.")
        write_prompt_file(path, item['version'], item['description'], item['params'], translate_str)
        pb.print_log(f"translate {key} to {tolang} in version {item['version']} \n")
