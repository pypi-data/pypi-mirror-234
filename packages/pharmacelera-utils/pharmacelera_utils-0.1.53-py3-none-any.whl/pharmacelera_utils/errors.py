import sys
import logging
import botocore
import requests
from .utils import Colors


class Errors:
    def __init__(self) -> None:
        pass

    def requestException(self, error):
        if isinstance(error, requests.exceptions.RequestException):
            logging.error("Request failed")
            logging.error(f"{Colors.FAIL}{str(error)}")

    def S3Exception(self, error):
        if isinstance(error, botocore.exceptions.ClientError):
            logging.error(f"{Colors.FAIL}{str(error)}{Colors.ENDC}")
            if "Not Found" in str(error):
                logging.info(f"{Colors.FAIL}File from S3 not found.{Colors.ENDC}")
        elif isinstance(error, botocore.exceptions.NoCredentialsError):
            logging.error(f"{Colors.FAIL}AWS credentials not found.{Colors.ENDC}")
        else:
            logging.error(f"{Colors.FAIL}{Colors.BOLD}Unhandled error occured: {type(error).__name__}{Colors.ENDC}")

        logging.error(f"{Colors.FAIL}Download from S3 failed.{Colors.ENDC}")

    def fileNameException(self):
        logging.error(
            f"{Colors.FAIL}If 'GET_CONF_FROM_S3' parameter is defined as true, then 'FILENAME' must be defined in config yaml.{Colors.ENDC}"
        )
        sys.exit(0)

    def bucketNameException(self):
        logging.error(f"{Colors.FAIL}S3_BUCKET parameter is not defined in configuration yaml.{Colors.ENDC}")
        sys.exit(0)

    def S3FolderPathException(self):
        logging.error(f"{Colors.FAIL}S3_FOLDER parameter is not defined in configuration yaml.{Colors.ENDC}")
        sys.exit(0)

    def inputFileNameException(self):
        logging.error(
            f"{Colors.FAIL}If 'GET_CONF_FROM_S3' parameter is defined as true, then 'EXP_1_INPUT' must be defined in config yaml.{Colors.ENDC}"
        )
        sys.exit(0)

    def inputFilesException(self, fileConf):
        logging.error(
            f"{Colors.FAIL}Input files could not be loaded. Please check the path and name of the files.{Colors.ENDC}\n{str(fileConf)}"
        )
        sys.exit(0)

    def downloadFilesException(self, exp):
        logging.error(f"{Colors.FAIL}Download files failed.{Colors.ENDC}\n{str(exp.message)}")
        sys.exit(0)

    def yamlParseException(self, exp):
        logging.error(f"{Colors.FAIL}Yaml config file is malformed.{Colors.ENDC}")