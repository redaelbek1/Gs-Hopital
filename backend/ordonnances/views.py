from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import Ordonnance
from .forms import OrdonnanceForm
from rendezvous.models import RendezVous


@login_required
def ordonnance_list(request):
    """Liste des ordonnances."""
    user = request.user
    if user.role == 'medecin':
        ordonnances = Ordonnance.objects.filter(medecin__user=user).select_related('rdv__patient__user')
    elif user.role == 'patient':
        ordonnances = Ordonnance.objects.filter(rdv__patient__user=user).select_related('medecin__user')
    else:
        ordonnances = Ordonnance.objects.all().select_related('rdv__patient__user', 'medecin__user')

    return render(request, 'ordonnances/list.html', {'ordonnances': ordonnances})


@login_required
def ordonnance_create(request, rdv_id):
    """Créer une ordonnance pour un rendez-vous."""
    rdv = get_object_or_404(RendezVous, pk=rdv_id)

    if request.method == 'POST':
        form = OrdonnanceForm(request.POST)
        if form.is_valid():
            ordonnance = form.save(commit=False)
            ordonnance.rdv = rdv
            ordonnance.medecin = request.user.medecin_profile
            ordonnance.save()
            messages.success(request, 'Ordonnance créée avec succès.')
            return redirect('ordonnances:detail', pk=ordonnance.pk)
    else:
        form = OrdonnanceForm()

    return render(request, 'ordonnances/create.html', {'form': form, 'rdv': rdv})


@login_required
def ordonnance_detail(request, pk):
    """Détail d'une ordonnance."""
    ordonnance = get_object_or_404(
        Ordonnance.objects.select_related('rdv__patient__user', 'medecin__user'),
        pk=pk,
    )
    return render(request, 'ordonnances/detail.html', {'ordonnance': ordonnance})


@login_required
def ordonnance_pdf(request, pk):
    """Télécharger l'ordonnance en PDF avec reportlab."""
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    import io

    ordonnance = get_object_or_404(
        Ordonnance.objects.select_related('rdv__patient__user', 'medecin__user', 'medecin__service'),
        pk=pk,
    )

    # Vérification accès : patient concerné, médecin concerné, ou admin
    user = request.user
    autorise = (
        user.role == 'admin' or
        (user.role == 'patient' and ordonnance.rdv.patient.user == user) or
        (user.role == 'medecin' and ordonnance.medecin.user == user)
    )
    if not autorise:
        messages.error(request, "Accès non autorisé.")
        return redirect('ordonnances:list')

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm,
    )

    styles = getSampleStyleSheet()
    story = []

    # Style personnalisés
    style_titre = ParagraphStyle('titre', parent=styles['Heading1'], fontSize=18,
                                  textColor=colors.HexColor('#1a73e8'), alignment=TA_CENTER, spaceAfter=6)
    style_sous_titre = ParagraphStyle('sous_titre', parent=styles['Normal'], fontSize=11,
                                       textColor=colors.grey, alignment=TA_CENTER, spaceAfter=12)
    style_section = ParagraphStyle('section', parent=styles['Heading2'], fontSize=13,
                                    textColor=colors.HexColor('#1a73e8'), spaceBefore=12, spaceAfter=6)
    style_normal = ParagraphStyle('normal', parent=styles['Normal'], fontSize=11, spaceAfter=4)
    style_contenu = ParagraphStyle('contenu', parent=styles['Normal'], fontSize=12,
                                    leading=18, spaceBefore=8, spaceAfter=8)

    medecin = ordonnance.medecin
    patient = ordonnance.rdv.patient

    # En-tête
    story.append(Paragraph("HÔPITAL — SYSTÈME DE GESTION", style_titre))
    service_nom = medecin.service.nom if hasattr(medecin, 'service') and medecin.service else "Service médical"
    story.append(Paragraph(f"Service : {service_nom}", style_sous_titre))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#1a73e8')))
    story.append(Spacer(1, 0.4*cm))

    # Titre ordonnance
    story.append(Paragraph(f"ORDONNANCE N° {ordonnance.id:04d}", style_section))
    story.append(Paragraph(f"Date : {ordonnance.date.strftime('%d/%m/%Y')}", style_normal))
    story.append(Spacer(1, 0.3*cm))

    # Infos médecin & patient
    data_table = [
        ['MÉDECIN', 'PATIENT'],
        [
            f"Dr {medecin.user.get_full_name()}\n{medecin.specialite if hasattr(medecin, 'specialite') else ''}",
            f"{patient.user.get_full_name()}\nTél : {patient.user.telephone or 'N/A'}"
        ],
    ]
    table = Table(data_table, colWidths=[8.5*cm, 8.5*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a73e8')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#f0f4ff'), colors.white]),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#1a73e8')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#ccddff')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(table)
    story.append(Spacer(1, 0.5*cm))

    # Contenu ordonnance
    story.append(Paragraph("PRESCRIPTION", style_section))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#ccddff')))
    story.append(Spacer(1, 0.2*cm))
    # Convertir les retours à la ligne en HTML
    contenu_html = ordonnance.contenu.replace('\n', '<br/>')
    story.append(Paragraph(contenu_html, style_contenu))
    story.append(Spacer(1, 1*cm))

    # Signature
    story.append(HRFlowable(width="100%", thickness=1, color=colors.grey))
    story.append(Spacer(1, 0.3*cm))
    sig_style = ParagraphStyle('sig', parent=styles['Normal'], fontSize=11, alignment=TA_RIGHT)
    story.append(Paragraph(f"Dr {medecin.user.get_full_name()}", sig_style))
    story.append(Paragraph(f"Date : {ordonnance.date.strftime('%d/%m/%Y')}", sig_style))

    doc.build(story)
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ordonnance_{ordonnance.id:04d}.pdf"'
    return response
