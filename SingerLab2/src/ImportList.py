'''
Created on Aug 17, 2016

@author: Nao
'''
import math, os, re, csv, sys, pprint
import lxml.etree as ET
import numpy as np
from numpy import pi
from numpy.linalg import inv
from scipy.spatial import convex_hull_plot_2d
from scipy.spatial import ConvexHull
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from matplotlib.pyplot import *
from shapely.geometry import Polygon


