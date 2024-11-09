import tempfile
import shutil


def create_temp_files(html_file_paths):
    '''
    Create temporary HTML files for modifying and rendering.
    '''
    temp_files = []
    for fname in html_file_paths:
        temp = tempfile.NamedTemporaryFile(
            mode='w', delete=False, suffix='.html')
        shutil.copy(fname, temp.name)
        temp_files.append(temp.name)
    return temp_files


def append_script(html_file_paths, script):
    '''
    Append a script to a list of HTML files.
    '''
    for fname in html_file_paths:
        with open(fname, 'a') as f:
            f.write("\n<script>{script}</script>".format(script=script))


def batch_files(html_file_paths, threads):
    '''
    Nest a list of file paths into batches for parallel processing.
    '''
    batch_size = len(html_file_paths) // threads
    batches = [html_file_paths[i:i+batch_size]
               for i in range(0, len(html_file_paths), batch_size)]
    return batches
