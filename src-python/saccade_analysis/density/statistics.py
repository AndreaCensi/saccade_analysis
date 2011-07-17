
def compute_joint_statistics(stats, saccades_stats):
    for k in stats: 
        if k in saccades_stats:
            print('Warning, %r in both' % k)
    stats.update(**saccades_stats)
    count = stats['count']
    total = saccades_stats['total']
    num_left = saccades_stats['num_left']
    num_right = saccades_stats['num_right']
    dt = 1.0 / 60
    T = count * dt

    T[count == 0] = 1
    stats['rate_saccade'] = total * 1.0 / T
    stats['rate_saccade_left'] = num_left * 1.0 / T
    stats['rate_saccade_right'] = num_right * 1.0 / T
 
    return stats
