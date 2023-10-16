import glob
import os


def generate_tpl_constants():
    tpl_files = glob.glob('../resources/tpl/**/*.tpl', recursive=True)

    constants = []
    for tpl_file in tpl_files:
        tpl_name = os.path.splitext(os.path.basename(tpl_file))[0]
        tpl_path = os.path.relpath(tpl_file, '../resources/tpl')
        tpl_constant = f"{tpl_name.upper()} = '{os.path.splitext(tpl_path)[0]}'"
        constants.append(tpl_constant)

    with open('tpl_constants.py', 'w') as file:
        file.write('"""\nAUTO GENERATE DON\'T CHANGE\nrun by utils/convert.py\n"""\n\n')
        file.write('\n'.join(constants))
        file.write('\n')


if __name__ == '__main__':
    generate_tpl_constants()
