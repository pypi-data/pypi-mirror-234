import robust
import argparse

def robust_bias_aware(**kwargs):
    if not('seeds' in kwargs.keys()) or not('outfile' in kwargs.keys()):
        if not('seeds' in kwargs.keys()):
            raise ValueError("Missing required parameter: 'seeds'")
        if not('outfile' in kwargs.keys()):
            raise ValueError("Missing required parameter: 'outfile'")
    else:
        seeds=kwargs['seeds']
        outfile=kwargs['outfile']
    try:
        network=kwargs['network']
    except:
        network='BioGRID'
    try:
        namespace=kwargs['namespace']
    except:
        namespace='GENE_SYMBOL'
    try:
        alpha=kwargs['alpha']
    except:
        alpha=0.25
    try:
        beta=kwargs['beta']
    except:
        beta=0.9
    try:
        n=kwargs['n']
    except:
        n=30
    try:
        tau=kwargs['tau']
    except:
        tau=0.1
    try:
        study_bias_scores=kwargs['study_bias_scores']
    except:
        study_bias_scores='BAIT_USAGE'
    try:
        gamma=kwargs['gamma']
    except:
        gamma=1.0
    
    _ , _ = robust.run(seeds, network, namespace, alpha, beta, n, tau, study_bias_scores, gamma, outfile)