from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from weasyprint import HTML
import os

def generate_ordre_mission_pdf(participation):
    """
    Génère un ordre de mission PDF pour une participation donnée.
    """
    context = {
        'participation': participation,
        'agent': participation.agent,
        'formation': participation.formation,
    }
    
    html_string = render_to_string('training/pdf/ordre_mission.html', context)
    html = HTML(string=html_string)
    pdf_file = html.write_pdf()
    
    filename = f"ordre_mission_{participation.id}_{participation.agent.matricule}.pdf"
    participation.ordre_mission.save(filename, ContentFile(pdf_file), save=True)
    return participation.ordre_mission.url
