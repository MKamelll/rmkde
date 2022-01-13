#!/usr/bin/env python3

import os, subprocess

class Zypper:
    def __init__(self):
        self.zypper = ["zypper"]
        self.cmds = []
        self.flags = []
        self.operands = []

    def _add_flag(self, flag):
        self.flags.append(flag)
    
    def _add_cmd(self, cmd):
        self.cmds.append(cmd)
    
    def _add_operand(self, operand):
        self.operands.append(operand)

    def _assemble(self):
        return self.zypper + self.cmds + self.flags + self.operands
    
    def _clean(self):
        self.cmds = []
        self.flags = []
        self.operands = []
    
    def search(self, pkg_name, installed=False):
        self._add_cmd("se")

        if installed:
            self._add_flag("-i")

        self._add_operand(pkg_name)        
        
        return self
    
    def commit(self, stdout=False):
        runable_cmd = self._assemble()

        if stdout:
            res = subprocess.run(runable_cmd)
        else:
            res = subprocess.run(runable_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        
        self._clean()
        return res.returncode


def check_root():
    if os.getegid() != 0:
        exit("You don't have root privilages")


def read_pkgs_file(file_name):
    data = []
    with open(f"{file_name}.txt") as f:
        for line in f:
            d = line.split()
            if len(d) > 0:
                data.extend(d)
    return data


def main():
    to_be_removed = []
    #check_root()
    cmd = Zypper()
    pkgs = read_pkgs_file("list")
    pkgs_count = len(pkgs)

    print("Starting the search..")

    searched = 0
    found = 0

    for i in pkgs:
        if cmd.search(i, installed=True).commit() == 0:
            to_be_removed.append(i)
            found += 1
        
        searched += 1
        
        print(f"finished: {i} || searched: {searched} || remaining: {pkgs_count - searched} || found: {found}")

    print(to_be_removed)


if __name__ == "__main__":
    main()

