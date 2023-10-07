# Python Secp256k1 Library
import platform, os, ctypes


class Core:
    def __init__(self):
        self.Fuzz = None
        self.load_library()

    def load_library(self):
        if 'win' in platform.platform().lower():
            dirPath = os.path.dirname(os.path.realpath(__file__))
            secFile = os.path.join(dirPath, '_secp256k2.dll')
            if os.path.isfile(secFile):
                dllPath = os.path.realpath(secFile)
                self.Fuzz = ctypes.CDLL(dllPath)
            else:
                raise ValueError(f"File {secFile} not found")

        elif 'linux' in platform.platform().lower():
            dirPath = os.path.dirname(os.path.realpath(__file__))
            secFile = os.path.join(dirPath, '_secp256k2.so')
            if os.path.isfile(secFile):
                dllPath = os.path.realpath(secFile)
                self.Fuzz = ctypes.CDLL(dllPath)
            else:
                raise ValueError(f"File {secFile} not found")
        else:
            raise EnvironmentError("Unsupported platform")


# from Loader import Core
# lib = Core()
# Fuzz = lib.Fuzz

