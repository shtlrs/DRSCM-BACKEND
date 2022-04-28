from typing import List
from drscm.proxies import InvoiceProxy
from drscm.models import Project, FixedTravel, HourlyTravel, WorkSession


def create_random_invoice(
    project: Project = None,
    work_sessions: List[WorkSession] = None,
    fixed_travels: List[FixedTravel] = None,
    hourly_travels: List[HourlyTravel] = None,
    save=False,
):

    invoice = InvoiceProxy()

    if project:
        invoice.project = project

    if work_sessions:
        invoice.work_sessions.set(work_sessions)

    if fixed_travels:
        invoice.fixed_travels.set(fixed_travels)

    if hourly_travels:
        invoice.hourly_travels.set(hourly_travels)

    if save:
        invoice.save()

    return invoice
