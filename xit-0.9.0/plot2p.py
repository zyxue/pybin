import logging
logger = logging.getLogger(__name__)
from collections import OrderedDict

import prop
import utils
import plot
import plot_types

def plot2p(A, C, core_vars):
    h5 = utils.get_h5(A, C)
    pt_objs = [prop.Property(i) for i in A.analysis]
    data = OrderedDict()
    for pt_obj in pt_objs:
        data[pt_obj.name] = OrderedDict()
        grps = plot.groupit(core_vars, pt_obj, A, C, h5)
        logger.info("Groups: {0}".format(grps.keys()))

        plot.calc_fetch_or_overwrite(grps, pt_obj, data[pt_obj.name], A, C, h5)

    func = plot_types.PLOT_TYPES[A.plot_type]
    func(data, A, C)
