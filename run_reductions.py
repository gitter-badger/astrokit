#!/usr/bin/env python
#
# Usage: ./reductions.py [analysis_id]
#

import os
import sys

import django
import numpy as np

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
sys.path.insert(0, os.getcwd())
django.setup()

import airmass
import transformation_coefficient as tf

from imageflow.models import Reduction, ImageAnalysis, ImageFilter

def supporting_calculations(analysis, reduction):
    '''Compute airmass and transformation coefficient.
    '''
    # Airmass
    reduction.reduced_stars = airmass.annotate_with_airmass(analysis, reduction)

    # Transformation coefficient
    computed_tf, tf_graph_url = tf.compute_tf_for_analysis(analysis, reduction, save_graph=True)
    reduction.tf = computed_tf
    reduction.tf_graph_url = tf_graph_url


def run_reductions(analysis):
    '''Run reductions on a given ImageAnalysis.
    '''
    try:
        reduction = Reduction.objects.get(analysis=analysis)
    except Reduction.DoesNotExist:
        reduction = Reduction(analysis=analysis)

    supporting_calculations(analysis, reduction)

    # Get the URAT1 keys for each CI band. eg. 'Bmag', 'jmag'
    filter_key = analysis.image_filter.urat1_key
    ci1_key = reduction.color_index_1.urat1_key
    ci2_key = reduction.color_index_2.urat1_key

    # Now put it all together.
    for i in xrange(len(reduction.reduced_stars)):
        # TODO(ian): Eliminate the outer loop. We only need to do this for the
        # unknown. Computing standard mag for each catalog star will help us
        # know our % error, though.
        star = reduction.reduced_stars[i]
        if filter_key not in star:
            print 'Skipping star %d because it does not have filter key %s' % (i, filter_key)
            continue

        # Mt = (mt - mc) - k"f Xt (CIt - CIc) + Tf (CIt - CIc) + Mc
        estimates = []
        for j in xrange(len(reduction.reduced_stars)):
            if i == j:
                continue

            comparison_star = reduction.reduced_stars[j]

            if not (ci1_key in star and ci2_key in star and \
                    ci2_key in comparison_star and ci2_key in comparison_star and \
                    filter_key in comparison_star):
                print 'Skipping a star pair (%d, %d) due to incomplete data' % (i, j)
                continue

            term1 = star['mag_instrumental'] - comparison_star['mag_instrumental']
            # FIXME(ian): CI calculation is not correct. Need to use companion image analysis.
            ci_target = star[ci1_key] - star[ci2_key]
            ci_comparison = comparison_star[ci1_key] - comparison_star[ci2_key]
            ci_diff = (ci_target - ci_comparison)
            term2 = reduction.second_order_extinction * comparison_star['airmass'] * ci_diff
            term3 = reduction.tf * ci_diff
            combined = term1 - term2 + term3 + comparison_star[filter_key]
            estimates.append(combined)

        star['mag_standard'] = np.mean(estimates)

        # Set mag_catalog to the URAT1 magnitude in this band.
        star['mag_catalog'] = star[filter_key]
        star['mag_error'] = star['mag_standard'] - star['mag_catalog']

    reduction.status = Reduction.COMPLETE
    reduction.save()

    reduction.analysis.status = ImageAnalysis.REDUCTION_COMPLETE
    reduction.analysis.save()

def process_pending_reductions():
    pending = Reduction.objects.all().filter(
            status=Reduction.PENDING)
    for reduction in pending:
        run_reductions(reduction.analysis)

if __name__ == '__main__':
    import os
    import django
    from django.core.exceptions import ObjectDoesNotExist
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
    sys.path.insert(0, os.getcwd())
    django.setup()

    from imageflow.models import ImageAnalysis

    if len(sys.argv) > 1:
        subid = sys.argv[1]
        try:
            result = ImageAnalysis.objects.get( \
                    astrometry_job__submission__subid=subid, \
                    status=ImageAnalysis.COMPLETE)
        except ObjectDoesNotExist:
            print 'Could not find submission', subid
            sys.exit(1)
        run_reductions(result)
    else:
        # Run all pending reductions.
        process_pending_reductions()
