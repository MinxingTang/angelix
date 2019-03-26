import os
import errno
from os.path import basename, join, exists
from utils import cd
import subprocess
import logging
import sys
import tempfile
from glob import glob

logger = logging.getLogger(__name__)

class Tester:

    def __init__(self, config, oracle, workdir):
        #print ("__init__ in Tester is invoked")
        #print ("config= "+ config + ", oracle= "+oracle + ", workdir= "+workdir)
        self.config = config
        self.oracle = oracle
        self.workdir = workdir

    def __call__(self, project, test, dump=None, trace=None, load=None, klee=False, env=os.environ, check_instrumented=False):
        #print ("__call__ in Test is invoked. Project dir: " + project.dir + ", test ID: " + test)
        src = basename(project.dir)
        if klee:
            logger.info('running test \'{}\' of {} source with KLEE'.format(test, src))
        else:
            if not self.config['mute_test_message']:
                logger.info('running test \'{}\' of {} source'.format(test, src))
        environment = dict(env)
        # dump, trace, klee are all none when run_test() is first invoked in Angelix in evaluate() 
        if dump is not None:
            environment['ANGELIX_WITH_DUMPING'] = dump
            reachable_dir = join(dump, 'reachable')  # maybe it should be done in other place?
            try:
                os.mkdir(reachable_dir)
            except:
                raise OSError("Cannot create directory (%s)!\n" % (reachable_dir))
        if trace is not None:
            environment['ANGELIX_WITH_TRACING'] = trace
        if (trace is not None) or (dump is not None) or (load is not None):
            environment['ANGELIX_RUN'] = 'angelix-run-test'
        if klee:
            environment['ANGELIX_RUN'] = 'angelix-run-klee'
            # using stub library to make lli work
            environment['LLVMINTERP'] = 'lli -load {}/libkleeRuntest.so'.format(os.environ['KLEE_LIBRARY_PATH'])
        if load is not None:
            environment['ANGELIX_WITH_LOADING'] = load
        environment['ANGELIX_WORKDIR'] = self.workdir
        environment['ANGELIX_TEST_ID'] = test
        #print ("ANGELIX_WORKDIR: " + self.workdir)

        dirpath = tempfile.mkdtemp()
        executions = join(dirpath, 'executions')
       
        environment['ANGELIX_RUN_EXECUTIONS'] = executions
        #print ("ANGELIX_RUN_EXECUTIONS: " + executions)

        if self.config['verbose'] and not self.config['mute_test_message']:
            subproc_output = sys.stderr
        else:
            subproc_output = subprocess.DEVNULL

        with cd(project.dir):
            #print ("Invoking subprocess.Popen: " + self.oracle + " " + test)
            proc = subprocess.Popen(self.oracle + " " + test,
                                    env=environment,
                                    stdout=subproc_output,
                                    stderr=subproc_output,
                                    shell=True)
            if klee or self.config['test_timeout'] is None: # KLEE has its own timeout
                code = proc.wait()
            else:
                #print ("proc wait for time out: " + self.config['test_timeout'])
                code = proc.wait(timeout=self.config['test_timeout'])

        instrumented = True
        if dump is not None or trace is not None or klee:
            if exists(executions):
                with open(executions) as file:
                    content = file.read()
                    if len(content) > 1:
                        logger.warning("ANGELIX_RUN is executed multiple times by test {}".format(test))
                        instrumented = False
            else:
                if not self.config['mute_test_message']:
                    logger.warning("ANGELIX_RUN is not executed by test {}".format(test))
                    instrumented = False

        if check_instrumented:
            return (code == 0, instrumented)
        else:
            return code == 0
