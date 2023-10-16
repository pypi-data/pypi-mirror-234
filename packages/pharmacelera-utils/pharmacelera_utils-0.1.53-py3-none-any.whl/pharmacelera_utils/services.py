import os
import time
import json
import shutil
import zipfile
import pathlib
import requests
from .errors import Errors

#
# Copyright (c) 2021 Pharmacelera S.L.
# All rights reserved.
#
# Description: Pharmacelera API calls
#


class Calls:
    """Pharmacelera API calling class."""

    def __init__(self, params):
        """Initialize configured parameters"""
        self.__errors = Errors() or None
        self.__path = params.get("MODEL_NAME") or ""
        self.__port = os.getenv("PORT") or params.get("PORT")
        self.__url = f"{params.get('URI')}:{self.__port}"

    def upload(self, files):
        """Upload binary and license inside container."""
        url = f"{self.__url}/uploadBinary"
        response = requests.request(
            "POST",
            url,
            files=files,
        )
        result = json.loads(response.text)
        return result

    def launch(self, endpoint, payload, files):
        """Launch an experiment with given data."""
        url = f"{self.__url}/{endpoint}"
        try:
            response = requests.request(
                "POST",
                url,
                data=payload,
                files=files,
            )
            result = json.loads(response.text)
            return result
        except Exception as exp:
            self.__errors.requestException(exp)

    def get(self, id):
        try:
            """Get experiment status data."""
            url = f"{self.__url}?id={id}"
            response = requests.request(
                "GET",
                url,
            )
            result = json.loads(response.text)
            return result
        except Exception as exp:
            self.__errors.requestException(exp)

    def list(self, query_param):
        try:
            """List all experiments."""
            url = f"{self.__url}/list?{query_param}"
            response = requests.request(
                "GET",
                url,
            )
            result = json.loads(response.text)
            return result
        except Exception as exp:
            self.__errors.requestException(exp)

    def download(self, id, folder, path=None, outputs="outputs", count=0):
        """Download a completed experiment."""
        if count == 0:
            print("Downloading the latest experiment files...")
        url = f"{self.__url}/download?id={id}"
        zipName = folder + ".zip"
        try:
            with requests.request("GET", url, stream=True) as r:
                r.raise_for_status()
                if r.headers.get("content-type").startswith("application/json"):
                    time.sleep(count)
                    if count == 20:
                        print(json.loads(r.text).get("body").get("msg"))
                    count += 1
                    if count <= 20:
                        self.download(id, folder, path, outputs, count=count)
                    return
                zip_path = os.path.join(outputs, self.__path)
                pathlib.Path(os.path.join(path, zip_path)).mkdir(
                    parents=True, exist_ok=True
                )
                with open(os.path.join(zip_path, zipName), "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                if r.headers.get("content-type") == "application/zip":
                    self.extractFiles(zip_path, zipName)
                    print(f"{zipName} Downloaded")
        except Exception as exp:
            self.__errors.downloadFilesException(exp)

    def kill(self, id):
        """Stop the running experiment manually."""
        try:
            url = f"{self.__url}/kill?id={id}"
            response = requests.request("GET", url)
            result = json.loads(response.text)
            return result
        except Exception as exp:
            self.__errors.requestException(exp)

    def remove(self, id):
        """Remove experiment, stop first if running and delete data and files."""
        try:
            url = f"{self.__url}/remove?id={id}"
            response = requests.request("DELETE", url)
            result = json.loads(response.text)
            return result
        except Exception as exp:
            self.__errors.requestException(exp)

    def extractFiles(self, zip_path, zipName):
        """Extract sdf files from compressed files."""
        dirname = pathlib.Path().absolute()
        with zipfile.ZipFile(os.path.join(dirname, zip_path, zipName)) as zipped:
            for file in zipped.namelist():
                if (
                    file.endswith((".sdf", "mol2"))
                    and file.find("erroneous") < 0
                    and file.find("reference_molecules") < 0
                ):
                    filename = zipName.rsplit(".", 1)[0]
                    path = os.path.join(dirname, "tmp", filename)
                    zipped.extract(file, path)
                    ext = "." + file.split(".")[-1]
                    target = filename + ext
                    shutil.move(
                        os.path.join(path, file),
                        os.path.join(dirname, "tmp", target),
                    )
                    os.rmdir(path)

    def clearFiles(self):
        """Clear input and output files from container
        after finish and download the experiment.
        """
        url = f"{self.__url}/clearAll"
        response = requests.request("DELETE", url)
        result = json.loads(response.text)
        return result
