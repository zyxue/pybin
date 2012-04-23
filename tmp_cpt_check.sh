#!/bin/bash

ls ${i} > tmp_cpt_check
gmxcheck_batch.py -f tmp_cpt_check --tmpf > tmp_cpt_check_result 