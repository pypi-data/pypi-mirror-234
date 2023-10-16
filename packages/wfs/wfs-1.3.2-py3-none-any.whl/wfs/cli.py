import os
import click
from pathlib import Path
from wfs.fgen import *

mypath = Path.cwd()


@click.group()
def cli():
    pass


@cli.command()
@click.argument('project', metavar='<project>')
@click.argument('apl', type=click.Choice(['mobile', 'web']), metavar='<apl>')
def main(project, apl):
    """
    CLI.
    """
    print(project, apl)
    if project:
        ppath = mypath / project
        create_scaffold(project_name=ppath, apl_name=apl)
        return 0


def create_scaffold(project_name, apl_name):
    """
    create scaffold with specified project name.
    """
    def create_folder(path):
        os.makedirs(path, exist_ok=True)
        msg = "created folder: {}".format(path)
        # log.info(msg)

    def create_file(path, file_content=""):
        if not os.path.exists(path):
            if file_content is not None:
                with open(path, 'w') as f:
                    f.write(file_content)
                msg = "created file: {}".format(path)
                rtx = 'Y'
            else:
                msg = "create excel file: {}".format(path)
                rtx = 'YY'
        else:
            msg = "File already exists. Not creating a new one."
            rtx = 'N'
        # print(msg)
        return rtx
        # log.info(msg)

    create_folder(project_name)
    create_folder(os.path.join(project_name, "test_dir"))
    create_folder(os.path.join(project_name, "reports"))
    create_folder(os.path.join(project_name, "reports", "screenshots"))
    file_path = mypath / project_name / "reports" / "web_results.xlsx"
    getf = create_file(file_path, None)
    if getf == 'YY':
        create_excel_sheet_results(file_path)
    create_folder(os.path.join(project_name, "test_data"))
    if apl_name == 'mobile':
        create_folder(os.path.join(project_name, "test_data", "mobile"))
        file_path_test = mypath / project_name / "test_data" / "mobile" / "app_test_case_and_data.xlsx"
        getf = create_file(file_path_test, None)
        if getf == 'YY':
            create_excel_sheet_for_testcase(file_path_test)
        file_path_repo = mypath / project_name / "test_data" / "mobile" / "app_object_repo.xlsx"
        getf = create_file(file_path_repo, None)
        if getf == 'YY':
            create_excel_sheet_for_object_repo(file_path_repo, app="mobile")
        create_file(os.path.join(project_name, "test_data", "mobile", "get_text_item.txt"))
        create_folder(os.path.join(project_name, "test_data", "mobile", "apps"))
        create_file(os.path.join(project_name, "test_dir", "test_zigapp.py"), test_zigapp_sample)
        create_file(os.path.join(project_name, "mproxy.py"), test_mproxy)
    else:
        create_folder(os.path.join(project_name, "test_data", "web"))
        file_path_test = mypath / project_name / "test_data" / "web" / "fms_test_case_and_data.xlsx"
        getf = create_file(file_path_test, None)
        if getf == 'YY':
            create_excel_sheet_for_testcase(file_path_test)
        file_path_repo = mypath / project_name / "test_data" / "web" / "fms_object_repo.xlsx"
        getf = create_file(file_path_repo, None)
        if getf == 'YY':
            create_excel_sheet_for_object_repo(file_path_repo)
        create_file(os.path.join(project_name, "test_data", "web", "get_text_item.txt"))
        create_file(os.path.join(project_name, "test_dir", "test_onefms.py"), test_web_sample)
        create_file(os.path.join(project_name, "proxy.py"), test_wproxy)
    create_file(os.path.join(project_name, "requirement.txt"), test_requires)
    create_file(os.path.join(project_name, "conf.ini"), conf_requires)
    create_file(os.path.join(project_name, "run.py"), run_test)

if __name__ == '__main__':
    cli()
