#!/bin/bash

# just for checking cpt files temparorily to see if they have been corrupted or not

ls $* > tmp_cpt_check
gmxcheck_batch.py -f tmp_cpt_check --tmpf > tmp_cpt_check_result 