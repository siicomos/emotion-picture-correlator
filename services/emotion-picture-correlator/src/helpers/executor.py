#!/bin/env python3

# Python version: 3.8.3
# Author: Liam Ling
# Contact: liam_ling@sfu.ca
# File name: excutor.py
# Description:
"""This class implements an interface of running external command.
"""

import subprocess
import shlex
import logging

logger = logging.getLogger(__name__)


class Executor:
    @staticmethod
    def __run(cmd, cwd=None, shell=False, verbose=False):
        try:
            if shell:
                logger.debug(cmd)
                complete_process = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True)
            else:
                logger.debug(shlex.split(cmd))
                complete_process = subprocess.run(
                    shlex.split(cmd), cwd=cwd, shell=False, capture_output=True
                )

            if verbose:
                logger.info(f"Command exited with {complete_process.returncode}")
            if complete_process.stdout:
                if verbose:
                    logger.info(f"stdout:\n{complete_process.stdout.decode()}")
            if complete_process.stderr:
                if verbose:
                    logger.info(f"stderr:\n{complete_process.stderr.decode()}")
            return (
                complete_process.returncode,
                complete_process.stdout.decode(),
                complete_process.stderr.decode(),
            )
        except Exception as e:
            logger.error(e)

    @staticmethod
    def run(cmd, cwd=None, shell=False, verbose=False):
        """
        Return process's return code, stdout, stderr
        """
        if cmd:
            return Executor.__run(cmd=cmd, cwd=cwd, shell=shell, verbose=verbose)
        else:
            logger.info("No command specified")
