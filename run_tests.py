# How to run:
# python run_tests.py -u https://github.com/<repository url> -s <student name> -d <date of deadline as YYYY-MM-DD>

__author__ = 'Gerardo Aragon, David Manlove'

import os, subprocess, shutil
import config_file_nolive as cf
import errno, os, stat
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# From: http://stackoverflow.com/questions/1213706/what-user-do-python-scripts-run-as-in-windows
def handleRemoveReadonly(func, path, exc):
  excvalue = exc[1]
  if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
      os.chmod(path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO) # 0777
      func(path)
  else:
      raise

def generate_file_list(test_cases):
    '''
        Helper function to generate a file list of the test set
    '''

    out = ['decorators.py', 'test_utils.py']
    for ch in test_cases:
        out.append('tests_' + ch + '.py')

    return out

def runtests(in_tests, in_errors):
    '''
    Function that runs tests given that a test has not passed
    '''
    out_tests = in_tests
    out_errors = in_errors
    for ch in in_tests:
        for key in in_tests[ch]:
            if in_tests[ch][key] is False:
                temp_test = 'rango.tests_' + ch + '.' + key
                print(temp_test)
                process = subprocess.Popen(['python', 'manage.py', 'test', temp_test], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, err = process.communicate()
                p_status = process.wait()
                out = out.decode('utf-8')
                try:
                    err = err.decode('utf-8')
                except:
                    err = str(err)
                if 'error' in err.lower() or 'errors' in err.lower() or 'Traceback' in err or 'Errno' in err:
                    print('++ FAILED!')
                    out_errors[key] = temp_test + '\n' + err
                else:
                    print('++PASSED!')
                    out_tests[ch][key] = True
                    out_errors[key] = None

    return out_tests, out_errors

def main(url_git, student_no, date_deadline):
    '''
    Main function that clones the repository given the deadline date, runs tests for each commit found in the repository
    and saves results and errors in the 'output' folder for the given student number
    '''

    # copy reports to student directory
    dir_student = os.path.join(BASE_DIR, "output", student_no)
    if not os.path.exists(dir_student):
        os.makedirs(dir_student)

    GIT_CLONE = 'git clone '
    GIT_CHKOUT = 'git checkout'
    GIT_CHKOUT_MASTER = 'git checkout master@{' + date_deadline + '23:59:59}'
    GIT_ADD = 'git add .'
    GIT_STASH = 'git stash'
    GIT_STASH_DROP = 'git stash drop'
    GIT_LOG = ['git', 'log', '--pretty=%H', '--before='+date_deadline]
    TEMP_DIR = 'temporal'

    test_cases = cf.dict_chs
    test_files = generate_file_list(test_cases)
    error_in_tests = dict()

    with open(os.path.join(dir_student, 'results.json'), 'w') as fp:
        json.dump(test_cases, fp, indent=4)

    try:
        #print(os.path.join(BASE_DIR, TEMP_DIR))
        #shutil.rmtree(os.path.join(BASE_DIR, TEMP_DIR), ignore_errors=False, onerror=handleRemoveReadonly)
        os.system("rmdir " + os.path.join(BASE_DIR, TEMP_DIR) + " /s /q")
    except Exception as e:
        print("Exception -> " + str(e))
        #print(os.path.join(BASE_DIR, TEMP_DIR) + " does not exist!!")

    ## Clone Repository
    with open(os.path.join(dir_student, 'report_errors.txt'), 'w') as fp:
        fp.write("I found errors while cloning your github repository: "+url_git)
        fp.write('===========================================================================\n\n\n')

    ret = subprocess.call(GIT_CLONE + url_git + " " + TEMP_DIR, shell=True)
    print(ret)
    assert(ret == 0)

    # Retrieve log history
    with open(os.path.join(dir_student, 'report_errors.txt'), 'w') as fp:
        fp.write("I couldn't get your log history in your github repository: "+url_git)
        fp.write('===========================================================================\n\n\n')

    os.chdir(os.path.join(BASE_DIR, TEMP_DIR))

    process = subprocess.Popen(GIT_LOG, stdout=subprocess.PIPE)
    out, err = process.communicate()
    out = out.decode('ascii')
    commits = out.split('\n')[0:-1]
    commits.reverse()

    print("Repository has " + str(len(commits)) + " commits!")
    noCommits = len(commits)

    with open(os.path.join(dir_student, 'commits.txt'), 'w') as fp:
        fp.write(str(len(commits)))
        fp.write('\n')

    with open(os.path.join(dir_student, 'report_errors.txt'), 'w') as fp:
        fp.write("It seems your github repository is not about Rango: "+url_git)
        fp.write('===========================================================================\n\n\n')

    working_dir = ''
    for root, dirs, files in os.walk("."):
        for name in files:
            if 'urls.py' == name:
                working_dir = os.path.dirname(os.path.abspath(root))
                break

    print("Project dir: " + working_dir)
    assert(os.path.isdir(os.path.abspath(working_dir + '/rango')))

    with open(os.path.join(dir_student, 'report_errors.txt'), 'w') as fp:
        fp.write("I found errors while running the automated tests in github repository: "+url_git)
        fp.write('===========================================================================\n\n\n')

    # Iterate over commits and run tests
    for c in commits:
        os.chdir(os.path.join(BASE_DIR, TEMP_DIR))
        ret = subprocess.call(GIT_CHKOUT + " " + c, shell=True)
        assert(ret == 0)

        working_dir = ''
        for root, dirs, files in os.walk("."):
            for name in files:
                if 'manage.py' == name:
                    working_dir = os.path.abspath(root)
                    break

        print(working_dir)

        # RUN TESTS HERE!!!!
        if os.path.isdir(os.path.abspath(working_dir + '/rango')):
            os.chdir(working_dir)
            try:
                shutil.rmtree(working_dir + '/rango/migrations', ignore_errors=False, onerror=handleRemoveReadonly)
                #os.system("rmdir " + os.path.join(BASE_DIR, TEMP_DIR) + " /s /q")
                os.remove("db.sqlite3")
            except:
                print("Couldn't delete db.sqlite3 and migrations folder")
            try:
                subprocess.call('python manage.py makemigrations rango')
            except:
                try:
                    subprocess.call('python manage.py makemigrations')
                except:
                    print("Error while making migrations rango!")
            try:
                subprocess.call('python manage.py migrate')
            except:
                print("Error while migrating rango!")
            for each in test_files:
                shutil.copyfile(os.path.join(BASE_DIR, each), os.path.join(working_dir , 'rango', each))


            test_cases, error_in_tests = runtests(test_cases, error_in_tests)

        # Discard everything
        os.chdir(os.path.join(BASE_DIR, TEMP_DIR))
        ret = subprocess.call(GIT_ADD, shell=True)
        assert(ret == 0)
        ret = subprocess.call(GIT_STASH, shell=True)
        ret = subprocess.call(GIT_STASH_DROP, shell=True)
        ret = subprocess.call(GIT_CHKOUT_MASTER, shell=True)
        assert(ret == 0)
    ## -------
    os.chdir(BASE_DIR)

    with open(os.path.join(dir_student, 'results.json'), 'w') as fp:
        json.dump(test_cases, fp, indent=4)

    with open(os.path.join(dir_student, 'report_errors.txt'), 'w') as fp:
        for each in error_in_tests:
            if error_in_tests[each] is not None:
                fp.write(error_in_tests[each])
                fp.write('===========================================================================\n\n\n')

    # with open(os.path.join(dir_student, 'report_errors.txt'), 'w') as fp:
    #     for each in error_in_tests:
    #         fp.write(each)
    #         fp.write('===========================================================================\n\n\n')

    #shutil.rmtree(os.path.join(BASE_DIR, TEMP_DIR), ignore_errors=False, onerror=handleRemoveReadonly)
    os.system("rmdir " + os.path.join(BASE_DIR, TEMP_DIR) + " /s /q")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", help="git repository where tests should run")
    parser.add_argument("-s", "--student", help="student number")
    parser.add_argument("-d", "--deadline", help="deadline")
    args = parser.parse_args()

    if args.url is not None and args.student is not None and args.deadline is not None:
        #try:
        main(args.url, args.student, args.deadline)
        #except Exception as e:
        #    print(e)
    else:
        raise BaseException("url, student number and deadline are required!!. Type 'python main_script.py -h' for further help")
