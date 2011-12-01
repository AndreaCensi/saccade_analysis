from reprep import Report
from flydra_db.db_extra import safe_flydra_db_open
from . import np

from saccade_analysis.density.report_saccades import plot_arena_with_circles

def report_traj_sample(rid, rows):
    r = Report(rid)

    print rows.dtype    
    x = rows['position'][:, 0]
    y = rows['position'][:, 1]
    
    f = r.figure()
    with f.plot('xy') as pl:
        pl.plot(x, y, '.', markersize=0.8)
        
        center = [0.18, 0.45]
        plot_arena_with_circles(pl, center, radius=1, col='g-')
        
        
        pl.axis('equal')
        
    r.text('length', '%s' % len(rows))
    return r


def report_traj(confid, flydra_db_directory, db_group, version):
    with safe_flydra_db_open(flydra_db_directory) as db:
        
        r = Report('%s_traj' % confid)
        samples = db.list_samples_for_group(db_group)
        
        for i, sample in enumerate(samples):
            print(i, sample)
            with db.safe_get_table(sample, table='rows', version=version) as rows:
                ri = report_traj_sample(sample, np.array(rows[:]))
                r.add_child(ri) 
             
        return r
