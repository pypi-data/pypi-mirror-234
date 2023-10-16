import os
import glob
import yaml
import shutil
import unittest
import subprocess
from pathlib import Path


class TestCMDCommands(unittest.TestCase):
    """pharmacelera-launch test cases."""

    statics: dict
    path = Path().absolute()

    @classmethod
    def setUpClass(cls) -> None:
        try:
            with open(os.path.join(cls.path, "testMocks", "config.yaml"), "r") as filename:
                config = yaml.safe_load(filename)
                cls.statics = config.get("static")
        except yaml.parser.ParserError:
            print("Could not parse yaml config")
        except Exception as exp:
            print(exp)

    def tearDown(self) -> None:
        self.remove("input_molecules.sdf", "activities.csv")
        shutil.rmtree(os.path.join(self.path, "inputs"), ignore_errors=True)
        shutil.rmtree(os.path.join(self.path, "outputs"), ignore_errors=True)

    def test_A_run_cmd_command_no_arg(self):
        """Executing CMD command without any arguments."""
        print(self.shortDescription())
        out = subprocess.check_output("pharmacelera-cmd")
        self.assertEqual(
            str(out, "UTF-8").rstrip(), "No argument parameter is present. Please, use --help to get more information"
        )

    def test_B_run_cmd_no_id_value(self):
        """Executing CMD command with empty id."""
        print(self.shortDescription())
        process = subprocess.run(
            ["pharmacelera-cmd", "--id"],
            capture_output=True,
            text=True,
        )
        err = process.stderr.split("\n")[-2].strip()
        self.assertEqual(err, ": error: argument --id: expected one argument")

    def test_C_run_cmd_no_host_connection(self):
        """Executing CMD with no connection to host."""
        print(self.shortDescription())
        process = subprocess.run(
            ["pharmacelera-cmd", "--id", "xxx", "--port", "5000"],
            capture_output=True,
            text=True,
        )
        err = process.stderr.split("\n")[0]
        err_desc = process.stderr.split("\n")[1]
        self.assertEqual(err, "ERROR:root:Request failed")
        self.assertGreater(err_desc.index("Failed to establish a new connection"), 0)

    def test_D_run_cmd_list_with_wrong_status(self):
        """Executing CMD list experiments with wrong status."""
        print(self.shortDescription())
        process = subprocess.run(
            [
                "pharmacelera-cmd",
                "--option",
                "list?status=unknown",
                "--port",
                self.statics["PORT"],
                "--uri",
                self.statics["URI"],
            ],
            capture_output=True,
            text=True,
        )
        out_with_color = process.stdout.split("\n")[1]
        self.assertEqual(out_with_color, "\x1b[91mNo experiment found.\x1b[0m")

    def test_E_run_cmd_list_with_finished_status(self):
        """Executing CMD list all finished experiments."""
        print(self.shortDescription())
        process = subprocess.run(
            [
                "pharmacelera-cmd",
                "--option",
                "list?status=finished",
                "--port",
                self.statics["PORT"],
                "--uri",
                self.statics["URI"],
            ],
            capture_output=True,
            text=True,
        )
        self.assertGreater(process.stdout.index("finished"), 0)

    def test_G_run_example_experiment(self):
        """Launching experiment for further cmd command testings."""
        print(self.shortDescription())
        outputs = []
        for line in self.execute(["pharmacelera-launch", "testMocks/config.yaml"]):
            if line.strip():
                outputs.append(line.strip())
        self.__class__.exp_id = outputs[0]

    def test_H_get_single_experiment(self):
        """Executing CMD get single experiment with id."""
        print(self.shortDescription())
        process = subprocess.run(
            [
                "pharmacelera-cmd",
                "--id",
                self.__class__.exp_id,
                "--port",
                self.statics["PORT"],
                "--uri",
                self.statics["URI"],
            ],
            capture_output=True,
            text=True,
        )
        print(process.stdout)
        count = process.stdout.split("\n")[0]
        self.assertEqual(count, "\x1b[94mCount: 1\x1b[0m")

    def test_J_kill_experiment_not_running(self):
        "Executing CMD kill not running experiment."
        print(self.shortDescription())
        process = subprocess.run(
            [
                "pharmacelera-cmd",
                "--option",
                "kill",
                "--id",
                self.__class__.exp_id,
                "--port",
                self.statics["PORT"],
                "--uri",
                self.statics["URI"],
            ],
            text=True,
            capture_output=True,
        )
        print(process.stdout)
        out_response = process.stdout.split("\n")[-3]
        self.assertEqual(out_response, "{'msg': 'No running/pending experiment found.'}")

    def test_K_download_experiment(self):
        "Executing CMD download finished experiment."
        print(self.shortDescription())
        process = subprocess.run(
            [
                "pharmacelera-cmd",
                "--option",
                "download",
                "--id",
                self.__class__.exp_id,
                "--port",
                self.statics["PORT"],
                "--uri",
                self.statics["URI"],
            ],
            text=True,
            capture_output=True,
        )
        print(process.stdout)
        generated_output = False
        for file in glob.glob(str(self.path) + "/*"):
            if file.find("test_case_cmd_") > -1:
                generated_output = True
                self.remove(file)
            if file.endswith("_TEST_MODEL") or file.endswith("tmp"):
                shutil.rmtree(file, ignore_errors=True)
        self.assertTrue(generated_output)

    def test_L_remove_experiment(self):
        "Execute CMD remove experiment."
        print(self.shortDescription())
        process = subprocess.run(
            [
                "pharmacelera-cmd",
                "--option",
                "remove",
                "--id",
                self.__class__.exp_id,
                "--port",
                self.statics["PORT"],
                "--uri",
                self.statics["URI"],
            ],
            text=True,
            capture_output=True,
        )
        print(process.stdout)
        process = subprocess.run(
            [
                "pharmacelera-cmd",
                "--id",
                self.__class__.exp_id,
                "--port",
                self.statics["PORT"],
                "--uri",
                self.statics["URI"],
            ],
            capture_output=True,
            text=True,
        )
        out_response = process.stdout.split("\n")[0]
        self.assertEqual(out_response, "\x1b[91mNo experiment found with the given id.\x1b[0m")

    def test_M_upload_no_parameter(self):
        """Execute upload binary command without parameter."""
        print(self.shortDescription())
        process = subprocess.run(["pharmacelera-cmd", "--option", "upload"], capture_output=True, text=True)
        out_response = process.stdout.split("\n")
        self.assertEqual(out_response[0], "\x1b[1mUploading binary and/or license ...\x1b[0m")
        self.assertEqual(out_response[1], "\x1b[91mPlease define binary and/or license path and filename.\x1b[0m")

    def test_N_upload_send_wrong_binary_type(self):
        """Execute upload binary command with wrong --type command."""
        print(self.shortDescription())
        process = subprocess.run(
            ["pharmacelera-cmd", "--option", "upload", "--type", "pharmqsa", "--binary", "notexists"],
            capture_output=True,
            text=True,
        )
        out_response = process.stdout.split("\n")[-2]
        self.assertEqual(out_response, "\x1b[91mBinary type is wrong, must be pharmqsar or pharmscreen")

    def test_O_upload_wrong_binary_path(self):
        """Execute upload binary command with a binary path that does not exists."""
        print(self.shortDescription())
        process = subprocess.run(
            ["pharmacelera-cmd", "--option", "upload", "--binary", "notexists"], capture_output=True, text=True
        )
        out_response = process.stdout.split("\n")[-2]
        self.assertEqual(
            out_response,
            "\x1b[91mCould not find the binary, please make sure binary is in the current folder or use absolute path.\x1b[0m",
        )

    def test_O_upload_binary_correctly(self):
        """Execute upload binary command with a binary path that does not exists."""
        print(self.shortDescription())
        process = subprocess.run(
            [
                "pharmacelera-cmd",
                "--option",
                "upload",
                "--binary",
                "testMocks/pharmqsar",
                "--port",
                self.statics["PORT"],
                "--uri",
                self.statics["URI"],
            ],
            capture_output=True,
            text=True,
        )
        out_response = process.stdout.split("\n")[1]
        self.assertEqual(
            out_response,
            "\x1b[92mUploaded.\x1b[0m",
        )

    def execute(self, cmd):
        """Executing command line with subprocess."""
        popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
        for stdout_line in iter(popen.stdout.readline, ""):
            yield stdout_line
        popen.stdout.close()
        return_code = popen.wait()
        if return_code:
            raise subprocess.CalledProcessError(return_code, cmd)

    def remove(self, *args):
        """Remove files and ignore error.
        args: iterable strings
        """
        for file in args:
            try:
                os.remove(os.path.join(self.path, file))
            except OSError:
                pass
