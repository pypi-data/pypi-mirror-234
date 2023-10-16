if __name__ == '__main__':
    from .FiniteDifferenceFormula import FDFormula, fd
    print("Object fd is available. You may run commands like\n",
          "fd.compute(2, range(-10,11))\n",
          "fd.compute(1, [0, -1, -2, 3, 4, 7])\n",
          "fd.activatepythonfunction()\n",
          "fd.truncationerror()", sep = '')
