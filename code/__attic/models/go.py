from analysis import analyze_saccades
from create_models import create_models
from report_tools.node import ReportNode #@UnresolvedImport
from models import saccades_to_ndarray


def generate_saccade(model, num):
    sequence = model.sample_saccade_sequence(num)          
    return saccades_to_ndarray(sequence)

def create_report(id, children):
    return ReportNode(id=id, children=children)

def write_report(report, basename):
    report.to_latex_document(basename + '.tex')
    report.to_html_document(basename + '.html')


from compmake import comp, comp_prefix #@UnresolvedImport

models = create_models()

reports = []
for model_name, model in models:
    comp_prefix(model_name)
    saccades = comp(generate_saccade, model, num=10000)
    report = comp(analyze_saccades, report_id=model_name, saccades=saccades)
    reports.append(report)
    
comp_prefix()
report = comp(create_report, id='all_models', children=reports)
comp(write_report, report, 'all_models')

    
    
