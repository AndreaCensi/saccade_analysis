import numpy

def create_letter_sequence(saccades):
    letters = []
    for saccade in saccades:
        if saccade['sign'] == 1:
            letters.append('L')
        elif saccade['sign'] == -1:
            letters.append('R')
        else: 
            assert False
    return "".join(letters)



def iterate_over_samples(saccades):
    ''' yields  sample_id, saccades_for_sample '''

    samples = numpy.unique(saccades['sample'])
    
    
    for sample in samples:
        select = saccades['sample'] == sample
        
        saccades_for_sample = saccades[select]
        
        yield sample, saccades_for_sample
        
        
def attach_description(report, text):
    ''' Attaches a general description to the report
        such that it will be recognized by combine_reports()
        and used as a description for the whole page. '''
        
    report.text('description', text, mime='text/x-rst')

