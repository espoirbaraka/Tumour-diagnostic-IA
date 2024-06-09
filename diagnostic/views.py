from django.shortcuts import render
from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
import networkx as nx
from django.http import HttpResponseBadRequest
from pgmpy.sampling import BayesianModelSampling
from pgmpy.inference import VariableElimination
import pylab as plt

def tumour_result(request):
    if request.method=='POST':
        try:
            coma=int(request.POST.get('coma'))
            headache=int(request.POST.get('headache'))
        except (ValueError, TypeError):
            return HttpResponseBadRequest("Invalid input. Please enter valid integers for coma and headache.")
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

        inference = VariableElimination(medical_model)
        answer = inference.query(
        variables=['Coma'],
        evidence={
            'Tumour': coma,
            'Serum': headache
        })

        if answer is not None:
            # result_list = []
            # for state, prob in zip(answer.state_names['Tumour'], answer.values):
            #         result_list.append(f"Tumour({state}): {prob:.4f}")
            max_prob_index = answer.values.argmax()  # Récupérer l'indice de la probabilité maximale
            max_state = answer.state_names['Coma'][max_prob_index]  # Récupérer l'état correspondant
            max_prob = answer.values[max_prob_index]
            if(max_state==0):
                res=f"Tu n'as pas la tumeur. Tu as une une probabilité de {max_prob}"
            elif(max_state==1):
                res=f"Tu as une probalibilte d'avoir la tumeur. Tu as une une probabilité de {max_prob}"
        else:
             print("Erreur de retour")

        context = {
            'res': res
        }
        # Create your views here.

        template = 'tumour_result.html'
        return render(request, template, context)
