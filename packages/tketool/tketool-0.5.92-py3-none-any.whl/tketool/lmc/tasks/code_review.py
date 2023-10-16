import time
from tketool.lmc.prompts.prompt_controller import get_prompt
from tketool.lmc.lmc_linked import lmc_linked_model
from tketool.lmc.tasks.task_init import get_init_llm
from tketool.logs import log, print_dash_line
import glob, os
from tketool.files import read_file, write_file_line
from tketool.utils.progressbar import process_status_bar
from langchain.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


def codereview(path, filter="*", addition_mark='.report'):
    """
    review the code, generic the report.
    path : the code folder path
    filter : filter str, like *.py
    """
    if filter is None or filter == "":
        filter = "*"
    if addition_mark is None or addition_mark == "":
        addition_mark = ".report"
    path = os.path.join(path, filter)
    llm = get_init_llm()

    link_model = lmc_linked_model(llm).set_prompt_template(get_prompt("codereviews"))

    link_model.log_state()

    allfiles = [filepath for filepath in glob.iglob(path, recursive=False)]
    pb = process_status_bar()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

    for filepath in pb.iter_bar(allfiles, key="file"):
        pb.process_print(filepath)
        documents = read_file(filepath)
        documents = documents.replace("    ", " ")

        if len(documents) == 0:
            continue

        pb.print_log(f"Code File {filepath} Length:{len(documents)}")
        split_document = text_splitter.split_text(documents)
        for idx, doc_split in pb.iter_bar(enumerate(split_document), key="split", max=len(split_document)):
            results, logs = link_model(lang="chinese", content=doc_split)
            if len(results) == 0:
                pb.print_log(f"file {filepath} error.")
            else:
                if idx == 0:
                    write_file_line(filepath + addition_mark, [results[0]])
                else:
                    write_file_line(f"{filepath}_{idx}_{addition_mark}", [results[0]])
