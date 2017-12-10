#!/usr/bin/env python

import os
import sys

import django
import numpy as np

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
sys.path.insert(0, os.getcwd())
django.setup()

import airmass
import transformation_coefficient as tf

from imageflow.models import Reduction, ImageFilter

def supporting_calculations(analysis, reduction):
    '''Compute airmass and transformation coefficient.
    '''
    # Airmass
    reduction.reduced_stars = airmass.annotate_with_airmass(analysis, reduction)

    # Transformation coefficient
    computed_tf, tf_graph_url = tf.compute_tf_for_analysis(analysis, reduction, save_graph=True)
    reduction.transformation_coefficient = computed_tf
    reduction.tf_graph_url = tf_graph_url


def run_reductions(analysis):
    '''Run reductions on a given AnalysisResult.
    '''
    reduction, _ = Reduction.objects.get_or_create(analysis=analysis)

    supporting_calculations(analysis, reduction)

    # Now put it all together.
    for i in xrange(len(reduction.reduced_stars)):
        # TODO(ian): Eliminate the outer loop. We only need to do this for the
        # unknown. Computing standard mag for each catalog star will help us
        # know our % error, though.
        star = reduction.reduced_stars[i]
        # Mt = (mt - mc) - k"f Xt (CIt - CIc) + Tf (CIt - CIc) + Mc
        estimates = []
        for j in xrange(len(reduction.reduced_stars)):
            if i == j:
                continue
            comparison_star = reduction.reduced_stars[j]
            term1 = star['instrumental_mag'] - comparison_star['instrumental_mag']
            ci_target = star[reduction.color_index_1.urat1_key] - star[reduction.color_index_2.urat1_key]
            ci_comparison = comparison_star[reduction.color_index_1.urat1_key] - comparison_star[reduction.color_index_2.urat1_key]
            ci_diff = (ci_target - ci_comparison)
            term2 = reduction.second_order_extinction * comparison_star['airmass'] * ci_diff
            term3 = reduction.tf * ci_diff
            combined = term1 - term2 + term3 + comparison_star[analysis.image_filter.urat1_key]
            estimates.append(combined)

        reduction.reduced_stars[i]['mag_standard'] = np.mean(estimates)

    reduction.status = Reduction.COMPLETE
    reduction.save()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage: reductions.py <submission id>'
        sys.exit(1)

    import os
    import django
    from django.core.exceptions import ObjectDoesNotExist
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
    sys.path.insert(0, os.getcwd())
    django.setup()

    from imageflow.models import AnalysisResult
    subid = sys.argv[1]

    try:
        result = AnalysisResult.objects.get( \
                astrometry_job__submission__subid=subid, \
                status=AnalysisResult.COMPLETE)
    except ObjectDoesNotExist:
        print 'Could not find submission', subid
        sys.exit(1)

    run_reductions(result)
