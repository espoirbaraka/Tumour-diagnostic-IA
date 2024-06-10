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
            headache=int(request.POST.get('tete'))
            cancer=int(request.POST.get('cancer'))
            calcium=int(request.POST.get('calcium'))
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
        variables=['Tumour'],
        evidence={
            'Headache': headache,
            'Metastatic': cancer,
            'Coma': coma,
            'Serum': calcium
        })

        if answer is not None:
            max_prob_index = answer.values.argmax()  # Récupérer l'indice de la probabilité maximale
            max_state = answer.state_names['Tumour'][max_prob_index]  # Récupérer l'état correspondant
            max_prob = answer.values[max_prob_index]
            if(max_state==0):
                res=f"Tu n'as pas la tumeur. La probabilité de ne pas l'avoir est de {max_prob*100} %"
            elif(max_state==1):
                res=f"Tu as une probalibilte d'avoir la tumeur. La probabilité de l'avoir est de {max_prob*100} %"
        else:
             print("Erreur de retour")

        context = {
            'res': res,
            'etat':max_state
        }

        template = 'tumour_result.html'
        return render(request, template, context)


def cancer_result(request):
    if request.method=='POST':
        try:
            coma=int(request.POST.get('coma'))
            headache=int(request.POST.get('tete'))
            tumour=int(request.POST.get('tumour'))
            calcium=int(request.POST.get('calcium'))
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
        variables=['Metastatic'],
        evidence={
            'Headache': headache,
            'Tumour': tumour,
            'Coma': coma,
            'Serum': calcium
        })

        if answer is not None:
            max_prob_index = answer.values.argmax()  # Récupérer l'indice de la probabilité maximale
            max_state = answer.state_names['Metastatic'][max_prob_index]  # Récupérer l'état correspondant
            max_prob = answer.values[max_prob_index]
            if(max_state==0):
                res=f"Tu n'as pas la tumeur. La probabilité de ne pas l'avoir est de {max_prob*100} %"
            elif(max_state==1):
                res=f"Tu as une probalibilte d'avoir la tumeur. La probabilité de l'avoir est de {max_prob*100} %"
        else:
             print("Erreur de retour")

        context = {
            'res': res,
            'etat':max_state
        }

        template = 'tumour_result.html'
        return render(request, template, context)
