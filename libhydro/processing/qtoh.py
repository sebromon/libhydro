# -*- coding: utf-8 -*-
"""Module de conversion de données de hauteur en données de débit"""

# -- imports ------------------------------------------------------------------
from __future__ import (
    unicode_literals as _unicode_literals, absolute_import as _absolute_import,
    division as _division, print_function as _print_function)

import datetime as _datetime
import copy as _copy
import numpy as _numpy

from libhydro.core import obshydro as _obshydro
from libhydro.core.courbetarage import CourbeTarage
from libhydro.processing import (interpolation as _interpolation,
                                 htoq as _htoq)


def obsq_to_obsh(obsq, courbestarage):
    """Obtention d'une observation de hauteur
    à partir d'une observation de débit

    Arguments:
        obsh (obshydro.Observation) Observation hydro de débit
        courbestarage : iterbale of courbetarage.CourbeTarage

    Return obshydro.Observation Observation hydro de hauteur with a result
        which can be nan
    """
    methode = 8
    qualif = 16
    debit = obsq['res'].item()

    # cas hauteur non définie
    if _numpy.isnan(debit):
        hauteur = None
        cnt = 1
        qualif = 16
        return _obshydro.Observation(dte=obsq['dte'].item(),
                                     res=None, mth=methode, qal=qualif,
                                     cnt=cnt, statut=obsq['statut'].item())
    # Récupération courbe tarage active
    ctar = _htoq.courbetarage_active(courbestarage, obsq['dte'].item())
    if ctar is None or not ctar.pivots:
        return _obshydro.Observation(dte=obsq['dte'].item(), res=None,
                                     mth=methode, qal=qualif, cnt=1,
                                     statut=obsq['statut'].item())

    if ctar.typect == 0:
        debitmin = ctar.pivots[0].debit
        debitmax = ctar.pivots[-1].debit
    else:
        debitmin = ctar.debit(hauteur=ctar.pivots[0].hauteur)
        debitmax = ctar.debit(hauteur=ctar.pivots[-1].hauteur)

    # Cas débit en dessous de la courbe
    if debit < debitmin:
        hauteur = None
        cnt = 4
        qualif = 16
        return _obshydro.Observation(dte=obsq['dte'].item(),
                                     res=None, mth=methode, qal=qualif,
                                     cnt=cnt, statut=obsq['statut'].item())

    # Cas débit au dessus de la courbe de tarage
    if debit > debitmax:
        hauteur = None
        cnt = 8
        qualif = 16
        return _obshydro.Observation(dte=obsq['dte'].item(), res=None,
                                     mth=methode, qal=qualif,
                                     cnt=cnt, statut=obsq['statut'].item())

    hauteur = ctar.hauteur(debit=debit)

    # Erreur de calcul
    if hauteur is None:
        return _obshydro.Observation(dte=obsq['dte'].item(), res=None,
                                     mth=methode, qal=qualif,
                                     cnt=cnt, statut=obsq['statut'].item())

    # calcul qualification entre la qualification des points pivots et celle
    # de l'observation'
    qualif = obsq['qal'].item() if obsq['qal'].item() is not None else 16

    # Vérification que la hauteur est bien dans la zone d'utilisation

    if ctar.limiteinf is not None:
        if hauteur <= ctar.limiteinf:
            qualif = 12
    if ctar.limitesup is not None:
        if hauteur >= ctar.limitesup:
            qualif = 12

    return _obshydro.Observation(dte=obsq['dte'].item(),
                                 res=hauteur,
                                 mth=methode,
                                 qal=qualif,
                                 cnt=obsq['cnt'].item(),
                                 statut=obsq['statut'].item())


def annuler_correction_hauteurs(seriehydro, courbecorrection, pivots=False):
    """Annule la correction des hauteurs à partir d'une courbe de correction

    Arguments:
        seriehydro (obshydro.Serie): serie hydro
        ccor (CourbeCorrection) : courbe de correction à appliquer à la série
        pivots (bool) : interpolation d'observations au niveau des pivots des
            courbes de tarage et de correction

    Return a serie hydro (obshydro.Serie)
    """
    if seriehydro.grandeur != 'H':
        raise ValueError('incorrect grandeur')
    if seriehydro.observations is None:  # or len(seriehydro.observations) == 0:
        return _copy.copy(seriehydro)
    obss_hcor = []
    prev_obs = None
    for obs in seriehydro.observations.itertuples():

        # Ajout d'observations au niveau des pivots de la courbe de correction
        if pivots and prev_obs is not None:
            pivots_cc = courbecorrection.get_pivots_between_dates(
                prev_obs.Index, obs.Index)
            for pivot in pivots_cc:
                if pivot.dte > prev_obs.Index and pivot.dte < obs.Index:
                    hauteur = _interpolation.interpolation_date(
                            dt=pivot.dte, dt1=prev_obs.Index, v1=prev_obs.res,
                            dt2=obs.Index, v2=obs.res)
                     # obs.res or hcor can be nan
                    hcor = courbecorrection.hauteur_corrigee(
                        dte=pivot.dte, hauteur=hauteur)
                    if hcor is not None:
                        hsanscor = hauteur - (hcor - hauteur)
                        cnt = obs.cnt
                    else:
                        hsanscor = None
                        cnt = 1
                    obss_hcor.append(_obshydro.Observation(
                            dte=pivot.dte, res=hsanscor, mth=8,
                            cnt=cnt, qal=obs.qal,
                            statut=obs.statut))
        
        prev_obs = obs
        # obs.res or hcor can be nan
        hcor = courbecorrection.hauteur_corrigee(
            dte=obs.Index,hauteur=obs.res)
        if hcor is not None:
            hsanscor = obs.res - (hcor - obs.res)
            cnt = obs.cnt
        else:
            hsanscor = None
            cnt = 1
        obss_hcor.append(_obshydro.Observation(dte=obs.Index, res=hsanscor,
                                               mth=8, cnt=cnt, qal=obs.qal,
                                               statut=obs.statut))

    # print(len(obss_hcor))
    return _obshydro.Serie(
        entite=seriehydro.entite,
        grandeur=seriehydro.grandeur,
        dtdeb=seriehydro.dtdeb,
        dtfin=seriehydro.dtfin,
        dtprod=_datetime.datetime.utcnow().replace(microsecond=0),
        observations=_obshydro.Observations(* obss_hcor))

def serieq_to_serieh(seriehydro=None, courbestarage=None,
                     courbecorrection=None, pivots=False):
    """Conversion d'une série hydro de débit en une série hydro de hauteur

    Arguments:
        seriehydro (_obshydro.Serie): une serie hydro
        courbestarage (an iterable of CourbeTarage): courbes de tarages
        courbecorrection (CourbeCorrection or None): courbe de correction
        pivots (bool) : interpolation d'observations au niveau des pivots des
            courbes de tarage et de correction

    Return: (_obshydro.Serie): une serie hydro de hauteur
    """
    # check seriehydro
    if not isinstance(seriehydro, _obshydro.Serie):
        raise TypeError('incorrect seriehydro')
    if seriehydro.grandeur != 'Q':
        raise ValueError('incorrect grandeur')
    if seriehydro.observations is None:
        serie = _copy.copy(seriehydro)
        serie.dtprod = _datetime.datetime.utcnow().replace(microsecond=0)
        return serie
    if courbestarage is None:
        courbestarage = []
    elif isinstance(courbestarage, CourbeTarage):
        courbestarage = [courbestarage]

    prev_obsh = None
    prev_obstuple = None
    obssh = []
    for obstuple in seriehydro.observations.itertuples():
        observation = _obshydro.Observation(dte=obstuple.Index,
                                            res=obstuple.res,
                                            mth=obstuple.mth,
                                            qal=obstuple.qal,
                                            cnt=obstuple.cnt,
                                            statut=obstuple.statut)
        ctar = _htoq.courbetarage_active(courbestarage, obstuple.Index)
        ctars = [ctar] if ctar is not None else []
        if pivots:
            # ajout des points intermédiaires de la courbe de tarage
            if prev_obstuple is not None and ctar is not None \
                    and len(ctar.pivots) > 0:

                if prev_obstuple.res <= obstuple.res:
                    qmin = prev_obstuple.res
                    qmax = obstuple.res
                else:
                    qmax = prev_obstuple.res
                    qmin = obstuple.res
                pivots_ctar = _htoq.ctar_get_pivots_between_debits(
                    ctar=ctar, qmin=qmin, qmax=qmax)
                if prev_obstuple.res > obstuple.res:
                    pivots_ctar = reversed(pivots_ctar)
                for pivot in pivots_ctar:
                    if ctar.typect == 0:
                        debit_pivot = pivot.debit
                    else:
                        debit_pivot = ctar.debit(hauteur=pivot.hauteur)
                    if debit_pivot > qmin and debit_pivot < qmax:
                        dte = _interpolation.interpolation_date_from_value(
                            val=debit_pivot, dt1=prev_obstuple.Index,
                            val1=prev_obstuple.res, dt2=obstuple.Index,
                            val2=obstuple.res)
                        if prev_obsh is not None \
                                and prev_obsh['dte'].item() == dte:
                            # avoid points with same date
                            continue
                        obsh = _obshydro.Observation(
                                dte=dte,
                                res=pivot.hauteur,
                                mth=obstuple.mth,
                                qal=obstuple.qal,
                                cnt=obstuple.cnt,
                                statut=obstuple.statut)
                        # Calcul continuite en fonction
                        # de l'observation précédente
                        cnt = obsh['cnt'].item()
                        if cnt != 1 and prev_obsh is not None:
                            prev_debit = prev_obsh['res'].item()
                            if _numpy.isnan(prev_debit):
                                obsh['cnt'] = prev_obsh['cnt'].item()

                        obssh.append(obsh)
                        prev_obsh = obsh

        prev_obstuple = obstuple

        if prev_obsh is not None \
                and prev_obsh['dte'].item() == observation['dte'].item():
            # avoid points with same date
            continue
        obsh = obsq_to_obsh(obsq=observation,
                            courbestarage=ctars)

        # Calcul continuite en fonction de l'observation précédente
        cnt = obsh['cnt'].item()
        if cnt != 1 and prev_obsh is not None:
            prev_debit = prev_obsh['res'].item()
            if _numpy.isnan(prev_debit):
                obsh['cnt'] = prev_obsh['cnt'].item()

        obssh.append(obsh)
        prev_obsh = obsh

    seriehydro = _obshydro.Serie(
        entite=seriehydro.entite,
        grandeur='H',
        dtdeb=seriehydro.dtdeb,
        dtfin=seriehydro.dtfin,
        dtprod=_datetime.datetime.utcnow().replace(microsecond=0),
        observations=_obshydro.Observations(* obssh))

    if courbecorrection is not None:
        seriehydro = annuler_correction_hauteurs(seriehydro, courbecorrection,
                                                 pivots)

    return seriehydro
