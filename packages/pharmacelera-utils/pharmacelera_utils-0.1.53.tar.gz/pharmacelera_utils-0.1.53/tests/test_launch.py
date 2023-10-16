import os
import glob
import shutil
import unittest
import subprocess
from pathlib import Path


class TestLaunch(unittest.TestCase):
    """pharmacelera-launch test cases."""

    path = Path().absolute()

    def tearDown(self) -> None:
        self.remove("input_molecules.sdf", "activities.csv")
        shutil.rmtree(os.path.join(self.path, "inputs"), ignore_errors=True)
        shutil.rmtree(os.path.join(self.path, "outputs"), ignore_errors=True)

    def test_A_yaml_config_arg_not_present(self):
        """Executing pharmacelera-launch command without argument of config file should return error message for missing yaml config."""
        print(self.shortDescription())
        out = subprocess.check_output("pharmacelera-launch")
        self.assertEqual(str(out, "UTF-8").rstrip(), "Please define yaml configuration file")

    def test_B_yaml_config_file_not_exist(self):
        """Executing command with config file argument that does not exist should return not found error."""
        print(self.shortDescription())
        process = subprocess.run(
            ["pharmacelera-launch", "configNotExist.yaml"],
            capture_output=True,
            text=True,
        )
        print(process.stderr)
        err = process.stderr.split("\n")[0]
        err_2 = process.stderr.split("\n")[2]
        self.assertEqual(err, "INFO:root:\x1b[1m\x1b[94mconfigNotExist.yaml file will be loading from local.\x1b[0m")
        self.assertEqual(err_2, "ERROR:root:[Errno 2] No such file or directory: 'configNotExist.yaml'")

    def test_C_yaml_config_file_s3_not_exist(self):
        """Executing command with s3 path that file is not exist to download should return not found error."""
        print(self.shortDescription())
        process = subprocess.run(
            ["pharmacelera-launch", "s3://pharmacelera-launch/pha-testing/configNotExist.yaml"],
            capture_output=True,
            text=True,
        )
        print(process.stderr)
        out_with_color = process.stderr.split("\n")[0]
        err_1 = process.stderr.split("\n")[-2]
        err_2 = process.stderr.split("\n")[-3]
        self.assertEqual(out_with_color, "INFO:root:\x1b[1m\x1b[94mconfigNotExist.yaml file will be downloading from S3\x1b[0m")
        self.assertEqual(err_1, "ERROR:root:Could not load experiments from config")
        self.assertEqual(err_2, "ERROR:root:[Errno 2] No such file or directory: 'configNotExist.yaml'")

    def test_D_incorrectly_formatted_yaml_config_file(self):
        """Executing command with a config file that yaml is not formatted correctly."""
        print(self.shortDescription())
        process = subprocess.run(
            ["pharmacelera-launch", "testMocks/config_incorrect.yaml"], capture_output=True, text=True
        )
        print(process.stderr)
        err_with_color = process.stderr.split("\n")[2]
        self.assertEqual(err_with_color, "ERROR:root:\x1b[91mYaml config file is malformed.\x1b[0m")

    def test_E_no_experiment_params_in_yaml_config_file(self):
        """Executing command with a config file that has no any experiment configuration."""
        print(self.shortDescription())
        process = subprocess.run(
            ["pharmacelera-launch", "testMocks/config_no_experiment.yaml"], capture_output=True, text=True
        )
        print(process.stderr)
        err_with_color = process.stderr.split("\n")[2]
        self.assertEqual(err_with_color, "ERROR:root:\x1b[91mNo experiment parameter is defined.\x1b[0m")

    def test_F_parameter_calculation(self):
        """Run a pharmQSAR experiment with config1"""
        print(self.shortDescription())
        outputs = []
        for line in self.execute(["pharmacelera-launch", "testMocks/config1.yaml"]):
            if line.strip():
                outputs.append(line.strip())
        self.assertTrue(Path(self.path, "outputs").is_dir())
        # Make sure 2 output files are downloaded
        outputs = glob.glob(os.path.join(self.path, "outputs/*/*"))
        self.assertEqual(len(outputs), 2)
        for file in outputs:
            self.assertTrue(Path(self.path, file).is_file())
            self.assertGreater(file.index("test_case_"), 0)
            self.assertGreater(Path(self.path, file).stat().st_size, 0)
        # Make sure best model zip file is generated
        generated_output = False
        for file in glob.glob(str(self.path) + "/*"):
            if file.endswith("_TEST_MODEL.zip"):
                generated_output = True
                output_file = file
        # delete zip file after test
        self.assertTrue(generated_output)
        if generated_output:
            self.remove(output_file)

    def test_J_model_generation_from(self):
        """Download experiment file from S3 and run model generate."""
        print(self.shortDescription())
        outputs = []
        for line in self.execute(["pharmacelera-launch", "testMocks/config4.yaml"]):
            if line.strip():
                outputs.append(line.strip())
        inputs = os.path.join(self.path, "inputs")
        self.assertTrue(os.path.isdir(inputs))

        # Make sure 2 output files are downloaded
        outputs = glob.glob(os.path.join(self.path, "outputs/*/*"))
        self.assertEqual(len(outputs), 2)
        for file in outputs:
            self.assertTrue(Path(self.path, file).is_file())
            self.assertGreater(file.index("test_case_"), 0)
            self.assertGreater(Path(self.path, file).stat().st_size, 0)

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
