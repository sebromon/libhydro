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
        debitmin = _htoq._debit_ctar_puissance(hauteur=ctar.pivots[0].hauteur,
                                               ctar=ctar)[0]
        debitmax = _htoq._debit_ctar_puissance(hauteur=ctar.pivots[-1].hauteur,
                                               ctar=ctar)[0]

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

    if ctar.typect == 0:
        hauteur, qualif_pivots = _hauteur_ctar_poly(debit, ctar)
    else:
        hauteur, qualif_pivots = _hauteur_ctar_puissance(debit, ctar)

    # Erreur de calcul 
    if hauteur is None:
        return _obshydro.Observation(dte=obsq['dte'].item(), res=None,
                                     mth=methode, qal=qualif,
                                     cnt=cnt, statut=obsq['statut'].item())

    # calcul qualification entre la qualification des points pivots et celle
    # de l'observation'
    qualif = obsq['qal'].item() if obsq['qal'].item() is not None else 16
    qualif = min(qualif, qualif_pivots)

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


def _hauteur_ctar_poly(debit, ctar):
    """Calcul de la hauteur à partir d'une courbe de tarage active
    de type poly

    Arguments:
        debit (float)
        ctar (CourbeTarage) courbe de tarage poly à appliquer à la hauteur

    Return tuple hauteur,qualif (float or  None, int or None)
    """
    prev_pivot = None
    pivot = None
    for pivot in ctar.pivots:
        if pivot.debit == debit:
            hauteur = pivot.hauteur
            qualif = pivot.qualif if pivot.qualif is not None else 16
            return (hauteur, qualif)
        if prev_pivot is not None and pivot.debit == prev_pivot.debit:
            raise ValueError("Points pivots avec même débit")
        if pivot.debit > debit:
            break
        prev_pivot = pivot

    # cas à gauche de la courbe
    if prev_pivot is None or pivot is None:
        return (None, None)
    # cas à droite de la courbe
    if pivot.debit < debit:
        return (None, None)

    # entre deux points pivots regression linéaire
    # H = a Q + b entre les deux points pivots
    coefa = (pivot.hauteur - prev_pivot.hauteur) / \
        (pivot.debit - prev_pivot.debit)
    coefb = pivot.hauteur - coefa * pivot.debit
    hauteur = coefa * debit + coefb

    qualif1 = prev_pivot.qualif if prev_pivot.qualif is not None else 16
    qualif2 = pivot.qualif if pivot.qualif is not None else 16
    qualif = min(qualif1, qualif2)

    return (hauteur, qualif)


def _hauteur_ctar_puissance(debit, ctar):
    """Calcul de la hauteur à partir d'une courbe de tarage active
    de type puissance

    Arguments:
        debit (float)
        ctar (CourbeTarage) courbe de tarage puissance à appliquer à la hauteur

    Return tuple hauteur,qualif (float or  None, int or None)
    """
    # Parcours des points pivots
    # Recherche du premier pivot avec h >= hauteur
    index = 0
    pivot = None
    for index, pivot in enumerate(ctar.pivots):
        # on ignore le premier point
        if index == 0:
            continue
        # calcul du débit du point pivot
        pivot_debit = _htoq._debit_ctar_puissance(
            hauteur=ctar.pivots[index].hauteur, ctar=ctar)[0]
        if pivot_debit >= debit:
            break

    # à gauche de la courbe
    if index == 0:
        return
    # A droite de la courbe
    if index == (len(ctar.pivots) - 1) and pivot_debit < debit:
        return (None, None)

    # if hauteur < pivot.varh:
    #     raise ValueError("hauteur {} inférieure à h0 {}".format(hauteur,
    #                                                             pivot.varh))
    if pivot.varb <= 0:
        raise ValueError('var b must be stricly positive')
    if pivot.vara <= 0:
        raise ValueError('var a must be strictly positive')
    hauteur = pivot.varh + (debit / (1000 * pivot.vara)) ** (1 / pivot.varb)
    # debit = 1000 * pivot.vara * (hauteur-pivot.varh)**pivot.varb
    qualif = pivot.qualif if pivot.qualif is not None else 16
    return (hauteur, qualif)


def annuler_correction_hauteurs(seriehydro, courbecorrection):
    """Annule la correction des hauteurs à partir d'une courbe de correction

    Arguments:
        seriehydro (obshydro.Serie): serie hydro
        ccor (CourbeCorrection) : courbe de correction à appliquer à la série

    Return a serie hydro (obshydro.Serie)
    """
    if seriehydro.grandeur != 'H':
        raise ValueError('incorrect grandeur')
    if seriehydro.observations is None:  # or len(seriehydro.observations) == 0:
        return _copy.copy(seriehydro)
    obss_hcor = []
    for obs in seriehydro.observations.itertuples():
        # obs.res or hcor can be nan
        hcor = _htoq.hauteur_corrigee(dte=obs.Index,
                                hauteur=obs.res,
                                ccor=courbecorrection)
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
                     courbecorrection=None):
    """Conversion d'une série hydro de débit en une série hydro de hauteur

    Arguments:
        seriehydro (_obshydro.Serie): une serie hydro
        courbestarage (an iterable of CourbeTarage): courbes de tarages
        courbecorrection (CourbeCorrection or None): courbe de correction

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
    obssh = []
    for obstuple in seriehydro.observations.itertuples():
        observation = _obshydro.Observation(dte=obstuple.Index,
                                            res=obstuple.res,
                                            mth=obstuple.mth,
                                            qal=obstuple.qal,
                                            cnt=obstuple.cnt,
                                            statut=obstuple.statut)
        obsh = obsq_to_obsh(obsq=observation,
                            courbestarage=courbestarage)

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
        seriehydro = annuler_correction_hauteurs(seriehydro, courbecorrection)

    return seriehydro
