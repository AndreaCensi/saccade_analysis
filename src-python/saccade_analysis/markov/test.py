from saccade_analysis.markov.first_order import first_order_analysis, \
    count_overlapping
import unittest


class MarkovTest(unittest.TestCase):
    
    
    def test_frequencies(self):
        results = dict(first_order_analysis('LR'))
        self.assertEqual(results['frequencies']['L'], 0.5)
        self.assertEqual(results['frequencies']['R'], 0.5)
        
        
    def test_invalid(self):
        first_order_analysis('LR')
        self.assertRaises(ValueError, first_order_analysis, '')
        self.assertRaises(ValueError, first_order_analysis, 'LER')


    def test_scipy(self):
        pass
        #binom.pmf(k, n, p) 

    def test_count_overlapping_invalid(self):
        self.assertRaises(ValueError, count_overlapping, 'LR', '')
        
    def test_count_overlapping(self):
        examples = [
            ('L', 'R', 0),
            ('LL', 'R', 0),
            ('LL', 'L', 2),
            ('LLL', 'LL', 2),
            ('LLLL', 'LLL', 2),
            ('LLLL', 'LL', 3),
            ('LRLR', 'LR', 2),
        ] 
        
        for string, sub, expected in examples:
            print 'String:', string.__repr__(), 'Sub:', sub.__repr__(), \
                 'Expect', expected
            self.assertEqual(count_overlapping(string, sub), expected)
