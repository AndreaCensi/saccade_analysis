from optparse import OptionParser
from saccade_analysis.analysis201009.datasets import load_datasets
from saccade_analysis import logger

def  create_letter_sequence(saccades):
    letters = []
    for saccade in saccades:
        if saccade['sign'] == 1:
            letters.append('L')
        elif saccade['sign'] == -1:
            letters.append('R')
        else: 
            assert False
    return "".join(letters)
            
def main():
    parser = OptionParser()
    parser.add_option("--data", help="Main data directory", default='.')
    parser.add_option("--output", help="Output filename")
    (options, args) = parser.parse_args()


    datasets = load_datasets(options.data)
    
    for name, dataset in datasets.items():
        saccades = dataset['saccades']
        
        num_samples = saccades['sample_num'].max()
        
        for i in range(num_samples):
            saccades_for_sample = saccades[saccades['sample_num'] == i]
            
            print 'dataset %15s, sample %4d: %5d saccades' % (name, i, len(saccades_for_sample))
    
            letters = create_letter_sequence(saccades)
            
            
if __name__ == '__main__':
    main()
