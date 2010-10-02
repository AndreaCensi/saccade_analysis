from saccade_analysis.markov.first_order import first_order_analysis
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
