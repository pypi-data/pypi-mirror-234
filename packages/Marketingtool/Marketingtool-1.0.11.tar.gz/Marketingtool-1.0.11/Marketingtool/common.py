# -*- coding: utf-8 -*-
import ntpath

def path_leaf(path):
    """
    get the file name from the path
    """
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)