from django.shortcuts import render
from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
import networkx as nx
from pgmpy.sampling import BayesianModelSampling
from pgmpy.inference import VariableElimination
import pylab as plt

def tumour_result(request):
    if request.method=='POST':
        coma=request.POST.get('coma')
        headache=request.POST.get('headache')
        medical_model = BayesianNetwork([
        #cause       effet
        ("Metastatic","Serum"),
        ("Metastatic","Tumour"),
        ("Serum","Coma"),
        ("Tumour","Coma"),
        ("Tumour","Headache"),
        ])

        cpd_metastic = TabularCPD(
            variable="Metastatic",
            variable_card=2, #Cardinalite 2 car nous avons juste 0 et 1 (Vrai ou faux)
            #       False(0)    True(1)
            values=[[0.8],[0.2]]
        )

        cpd_serum = TabularCPD(
            variable="Serum",
            variable_card=2,
            #       1-P(Serum)                   P(Serum)                   
            values=[[0.8, 0.2], [0.2, 0.8]],
            evidence=["Metastatic"],
            evidence_card=[2]
        )

        cpd_tumour = TabularCPD(
            variable="Tumour",
            variable_card=2,
            #       1-P(Tumour)                   P(Tumour)                   
            values=[[0.95, 0.8], [0.05, 0.2]],
            evidence=["Metastatic"],
            evidence_card=[2]
        )
        cpd_coma = TabularCPD(
            variable="Coma",
            variable_card=2,
            #       1-P(Coma)                   P(Coma)                   
            values=[[0.95, 0.2, 0.2, 0.2], [0.05, 0.8, 0.8, 0.8]],
            evidence=["Serum","Tumour"],
            evidence_card=[2,2]
        )

        cpd_headache = TabularCPD(
            variable="Headache",
            variable_card=2,
            #       1-P(Tumour)                   P(Tumour)                   
            values=[[0.4, 0.2], [0.6, 0.8]],
            evidence=["Tumour"],
            evidence_card=[2]
        )

        medical_model.add_cpds(
            cpd_metastic,
            cpd_serum,
            cpd_tumour,
            cpd_coma,
            cpd_headache
        )
        # Create your views here.

        template = 'afficher.html'
        return render(request, template)
