import os
import logging
logger = logging.getLogger(__name__)

import matplotlib.pyplot as plt

import utils

from distr import distr, get_params, decorate_ax
from grped_distr import grped_distr

@utils.is_plot_type
def alx(data, A, C, **kw):
    """because the data structure of data is the same as that of distr"""
    distr(data, A, C, **kw)

@utils.is_plot_type
def grped_alx(data, A, C, **kw):
    grped_distr(data, A, C, **kw)
