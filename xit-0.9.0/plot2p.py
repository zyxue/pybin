import logging
logger = logging.getLogger(__name__)
from collections import OrderedDict

import prop
import utils
import plot
import plot2p_types

def plot2p(A, C, core_vars):
    h5 = utils.get_h5(A, C)
    prop_objs = [prop.Property(i) for i in A.properties]
    data = OrderedDict()
    for prop_obj in prop_objs:
        data[prop_obj.name] = OrderedDict()
        grps = plot.groupit(core_vars, prop_obj, A, C, h5)
        logger.info("Groups: {0}".format(grps.keys()))

        plot.calc_fetch_or_overwrite(grps, prop_obj, data[prop_obj.name], A, C, h5)

    func = plot2p_types.PLOT2P_TYPES[A.plot2p_type]
    func(data, A, C)
