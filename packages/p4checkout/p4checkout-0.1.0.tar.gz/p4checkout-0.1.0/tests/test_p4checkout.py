from pathlib import Path

import P4
import os
import sys
import random
import string
import unittest
import itertools

sys.path.insert(0, str(Path(__file__).parent.parent))

from p4checkout import p4checkout, PerforceCheckout

HOME_DIR = Path(os.path.expanduser("~"))

USER = "bruno"
PORT = "localhost:1492"
CLIENT = "bruno_jam"
SRC_DIR = HOME_DIR / "p4checkout_test/workspaces/bruno_ws/src/"
SRC_DIR_DEPOT = "//jam/main/src"
EXISTING_FILE1 = "command.c"
EXISTING_FILE2 = "command.h"
NEW_FILE_TEMPLATE = "new_{}.c"

def create_random_new_file():
    path = SRC_DIR / NEW_FILE_TEMPLATE.format(''.join(random.choice(string.ascii_lowercase) for _ in range(10)))
    with open(path, "w") as f:
        f.write(f"New file: {path}")
    return path

class P4Wrapper:
    def __enter__(self):
        self.p4 = P4.P4()
        self.p4.user = USER
        self.p4.port = PORT
        self.p4.client = CLIENT
        self.p4.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.p4.disconnect()

    def revert_all_pending_changes(self):
        try:
            self.p4.run_revert('//...')
        except P4.P4Exception:
            pass
        for change in self.p4.iterate_changes(["-u", self.p4.user, "-c", self.p4.client]):
            if change["Status"] == "pending":
                self.p4.run_change(["-df", change["Change"]])
    
    def get_pending_changes(self):
        res = []
        for change in self.p4.iterate_changes(["-u", self.p4.user, "-c", self.p4.client]):
            if change["Status"] == "pending":
                res.append(change)
        return res
    
    def get_default_changelist_files(self):
        return [x["depotFile"] for x in self.p4.run_opened(["-u", self.p4.user, "-c", "default", "-C", self.p4.client])]


class P4CheckoutBaseTestClass(unittest.TestCase):

    P4_ARGS = {
        "user": USER,
        "port": PORT
    }

    def __init__(self, methodName: str = "runTest", file1 = None, file2 = None) -> None:
        super().__init__(methodName)
        self.file1 = file1
        self.file2 = file2

    @classmethod
    def setUpClass(cls):
        p4checkout.logging.basicConfig(level=p4checkout.logging.CRITICAL)

    def setUp(self) -> None:
        with P4Wrapper() as p4wrapper:
            p4wrapper.revert_all_pending_changes()
  
    def test_no_additional_cls(self):
        with PerforceCheckout(self.file1, **self.P4_ARGS) as p4checkout:
            changelists = [cl.description for cl in p4checkout.changelists]
            self.assertTrue("default" in changelists)
            self.assertTrue("New" in changelists)
            self.assertEqual(len(changelists), 2)

    def test_create_pending_cl(self):
        description = "This is a test"
        with PerforceCheckout(self.file1, **self.P4_ARGS) as p4checkout:
            p4checkout.checkout(p4checkout.CL_ID_NEW, description)
        
        with P4Wrapper() as p4wrapper:
            changelists = p4wrapper.get_pending_changes()
            self.assertEqual(len(changelists), 1)
            self.assertEqual(changelists[0]["Description"], description + "\n")

    def test_checkout_twice_new_cl(self):
        with PerforceCheckout(self.file1, **self.P4_ARGS) as p4checkout:
            p4checkout.checkout(p4checkout.CL_ID_NEW, "First CL")
        
        with self.assertRaises(Exception) as context:
            with PerforceCheckout(self.file1, **self.P4_ARGS) as p4checkout:
                p4checkout.checkout(p4checkout.CL_ID_NEW, "Second CL")
        self.assertTrue('File is already checked out' in str(context.exception))

    def test_checkout_twice_same_cl(self):
        with PerforceCheckout(self.file1, **self.P4_ARGS) as p4checkout:
            cl = p4checkout.checkout(p4checkout.CL_ID_NEW, "First CL")
        
        with self.assertRaises(Exception) as context:
            with PerforceCheckout(self.file1, **self.P4_ARGS) as p4checkout:
                p4checkout.checkout(cl, None)
        self.assertTrue('File is already checked out' in str(context.exception))

    def test_checkout_twice_default_cl_first(self):
        with PerforceCheckout(self.file1, **self.P4_ARGS) as p4checkout:
            p4checkout.checkout(p4checkout.CL_ID_DEFAULT, None)
        
        with self.assertRaises(Exception) as context:
            with PerforceCheckout(self.file1, **self.P4_ARGS) as p4checkout:
                p4checkout.checkout(p4checkout.CL_ID_NEW, "CL")
        self.assertTrue('File is already checked out' in str(context.exception))

    def test_checkout_twice_default_cl_second(self):
        with PerforceCheckout(self.file1, **self.P4_ARGS) as p4checkout:
            p4checkout.checkout(p4checkout.CL_ID_NEW, "CL")
        
        with self.assertRaises(Exception) as context:
            with PerforceCheckout(self.file1, **self.P4_ARGS) as p4checkout:
                p4checkout.checkout(p4checkout.CL_ID_DEFAULT, "CL")
        self.assertTrue('File is already checked out' in str(context.exception))

    def test_checkout_two_files_same_cl_new(self):
        with PerforceCheckout(self.file1, **self.P4_ARGS) as p4checkout:
            cl = p4checkout.checkout(p4checkout.CL_ID_NEW, "CL")
        
        with PerforceCheckout(self.file2, **self.P4_ARGS) as p4checkout:
            p4checkout.checkout(cl, None)
        
        with P4Wrapper() as p4wrapper:
            changelists = p4wrapper.get_pending_changes()
            self.assertEqual(len(changelists), 1)
            self.assertEqual(set([f"{SRC_DIR_DEPOT}/{Path(self.file1).name}", f"{SRC_DIR_DEPOT}/{Path(self.file2).name}"]),
                             set(changelists[0]["Files"]))
    
    def test_checkout_two_files_same_cl_default(self):
        with PerforceCheckout(self.file1, **self.P4_ARGS) as p4checkout:
            p4checkout.checkout(p4checkout.CL_ID_DEFAULT, None)
        
        with PerforceCheckout(self.file2, **self.P4_ARGS) as p4checkout:
            p4checkout.checkout(p4checkout.CL_ID_DEFAULT, None)
        
        with P4Wrapper() as p4wrapper:
            files = p4wrapper.get_default_changelist_files()
            self.assertEqual(set([f"{SRC_DIR_DEPOT}/{Path(self.file1).name}", f"{SRC_DIR_DEPOT}/{Path(self.file2).name}"]),
                             set(files))
            
    def test_checkout_two_files_different_cls_new_new(self):
        cl1_desc = "CL1"
        with PerforceCheckout(self.file1, **self.P4_ARGS) as p4checkout:
            cl1 = p4checkout.checkout(p4checkout.CL_ID_NEW, cl1_desc)
        
        cl2_desc = "CL2"
        with PerforceCheckout(self.file2, **self.P4_ARGS) as p4checkout:
            cl2 = p4checkout.checkout(p4checkout.CL_ID_NEW, cl2_desc)
        
        with P4Wrapper() as p4wrapper:
            changelists = p4wrapper.get_pending_changes()
            self.assertEqual(len(changelists), 2)
            for cl, file in {cl1: Path(self.file1).name, cl2: Path(self.file2).name}.items():
                for changelist in changelists:
                    if changelist["Change"] == cl:
                        self.assertEqual(set([f"{SRC_DIR_DEPOT}/{file}"]),
                                         set(changelist["Files"]))
                        
    def test_empty_description(self):
        with self.assertRaises(Exception) as context:
            with PerforceCheckout(self.file1, **self.P4_ARGS) as p4checkout:
                p4checkout.checkout(p4checkout.CL_ID_NEW, "")
        self.assertTrue('New changelist description cannot be empty' in str(context.exception))

    def test_bad_server(self):
        with self.assertRaises(Exception) as context:
            with PerforceCheckout(self.file1, user=self.P4_ARGS["user"], port=self.P4_ARGS["port"] + "1") as p4checkout:
                p4checkout.checkout(p4checkout.CL_ID_NEW, "New")
        self.assertTrue('Connection refused' in str(context.exception))

    def test_non_existent_file(self):
        with self.assertRaises(Exception) as context:
            with PerforceCheckout("/tmp/file.txt", **self.P4_ARGS) as p4checkout:
                p4checkout.checkout(p4checkout.CL_ID_NEW, "New")
        self.assertTrue('does not exist!' in str(context.exception))

    def test_file_outside_workspace(self):
        with self.assertRaises(Exception) as context:
            with PerforceCheckout(Path( __file__ ).absolute(), **self.P4_ARGS) as p4checkout:
                p4checkout.checkout(p4checkout.CL_ID_NEW, "New")
        self.assertTrue('Provided path is not under any known client' in str(context.exception))

def load_tests(loader, standard_tests, pattern):
    new_file1 = create_random_new_file()
    new_file2 = create_random_new_file()
    suite = unittest.TestSuite()
    
    for standard_test in standard_tests:
        for test in standard_test:
            if test.__class__ == P4CheckoutBaseTestClass:
                for file1, file2 in itertools.product([SRC_DIR / EXISTING_FILE1, new_file1], [SRC_DIR / EXISTING_FILE2, new_file2]):
                    suite.addTest(P4CheckoutBaseTestClass(str(test).split()[0], file1, file2))
            else:
                suite.addTest(test)
    return suite

if __name__ == "__main__":
    if not (SRC_DIR / EXISTING_FILE1).exists():
        raise Exception(f"Can't find Perforce sample depot, please setup via p4_sample_depot.sh script")
    unittest.main()
    