import numpy as np

from psychopy import session, visual, logging
from psychopy.hardware import keyboard
from psychopy.tests import utils
from psychopy.constants import STARTED, PAUSED, STOPPED
from pathlib import Path
import shutil
import inspect
import threading
import time


class TestSession:
    def setup_class(cls):
        root = Path(utils.TESTS_DATA_PATH) / "test_session" / "root"
        inputs = {
            'defaultKeyboard': keyboard.Keyboard(),
            'eyetracker': None
        }
        win = visual.Window([128,128], pos=[50,50], allowGUI=False, autoLog=False)
        cls.sess = session.Session(
            root,
            loggingLevel="info",
            inputs=inputs,
            win=win,
            experiments={
                'exp1': "exp1/exp1.psyexp",
                'exp2': "exp2/exp2.psyexp",
                'testCtrls': "testCtrls/testCtrls.psyexp",
                'error': "error/error.psyexp",
                'annotation': "annotation/annotation.psyexp"
            }
        )

    def test_outside_root(self):
        # Add an experiment from outside of the Session root
        expFile = Path(utils.TESTS_DATA_PATH) / "test_session" / "outside_root" / "externalExp.psyexp"
        self.sess.addExperiment(expFile, key="externalExp")
        # Check that file is copied
        newExpFile = self.sess.root / "outside_root" / "externalExp.psyexp"
        assert newExpFile.is_file()
        # Check that newly added experiment still runs
        self.sess.runExperiment("externalExp")
        # Remove external experiment
        shutil.rmtree(str(newExpFile.parent))
        del self.sess.experiments['externalExp']

    def test_run_exp(self):
        self.sess.runExperiment("exp2")
        self.sess.runExperiment("exp1")

    def test_ctrls(self):
        """
        Check that experiments check Session often enough for pause/resume commands sent asynchronously will still work.
        """
        def send_dummy_commands(sess):
            """
            Call certain functions of the Session class with time inbetween
            """
            # Set experiment going
            sess.runExperiment("testCtrls", blocking=False)
            # Wait 0.1s then pause
            time.sleep(.2)
            sess.pauseExperiment()
            # Wait 0.1s then resume
            time.sleep(.2)
            sess.resumeExperiment()
            # Wait then close
            time.sleep(.2)
            sess.stop()

        # Send dummy commands from a new thread
        thread = threading.Thread(
            target=send_dummy_commands,
            args=(self.sess,)
        )
        thread.start()
        # Start session
        self.sess.start()

    def test_sync_clocks(self):
        """
        Test that experiment clock is applied to ioHub
        """
        from psychopy import iohub

        def _sameTimes():
            times = [
                # ioHub process time
                self.sess.inputs['ioServer'].getTime(),
                # ioHub time in current process
                iohub.Computer.global_clock.getTime(),
                # experiment time
                self.sess.sessionClock.getTime(),
            ]
            # confirm that all values are within 0.001 of eachother
            avg = sum(times) / len(times)
            deltas = [abs(t - avg) for t in times]
            same = [d < 0.001 for d in deltas]

            return all(same)
        # setup experiment inputs
        self.sess.setupInputsFromExperiment("exp1")
        # knock ioHub timer out of sync
        time.sleep(1)
        # run experiment
        self.sess.runExperiment("exp1")
        # confirm that ioHub timer was brought back into sync
        assert _sameTimes(), (
            self.sess.inputs['ioServer'].getTime(),
            iohub.Computer.global_clock.getTime(),
            self.sess.sessionClock.getTime(),
        )

    def test_clock_format(self):
        cases = [
            # usual from-zero time should return a float
            {'val': "float", 'ans': float},
            # iso should return iso formatted string
            {'val': "iso", 'ans': str},
            # custom str format should return as custom formatted string
            {'val': "%m/%d/%Y, %H:%M:%S", 'ans': "%m/%d/%Y, %H:%M:%S"}
        ]

        for case in cases:
            sess = session.Session(
                root=Path(utils.TESTS_DATA_PATH) / "test_session" / "root",
                clock=case['val'],
                win=self.sess.win,
                experiments={
                    'clockFormat': "testClockFormat/testClockFormat.psyexp"
                }
            )

            sess.runExperiment('clockFormat', expInfo={'targetFormat': case['ans']})

    # def test_error(self, capsys):
    #     """
    #     Check that an error in an experiment doesn't interrupt the session.
    #     """
    #     # run experiment which has an error in it
    #     success = self.sess.runExperiment("error")
    #     # check that it returned False after failing
    #     assert not success
    #     # flush the log
    #     logging.flush()
    #     # get stdout and stderr
    #     stdout, stderr = capsys.readouterr()
    #     # check that our error has been logged as CRITICAL
    #     assert "CRITICAL" in stdout + stderr
    #     assert "ValueError:" in stdout + stderr
    #     # check that another experiment still runs after this
    #     success = self.sess.runExperiment("exp1")
    #     assert success
