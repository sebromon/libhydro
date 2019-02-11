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
from libhydro.processing import interpolation as _interpolation


def hauteur_corrigee(dte, hauteur, ccor):
    """Calcul de la hauteur corrigée à partir d'une courbe de correction

    Arguments:
        dte (datetime.datetime): date de la mesure à corriger
        hauteur (float): hauteur à corriger
        ccor (CourbeCorrection) : courbe de correction

    Return: float or None: hauteur corrigée

    """
    pi1 = None
    pi2 = None
    for pivot in ccor.pivots:
        if pivot.dte == dte:
            return hauteur + pivot.deltah
        elif pivot.dte < dte:
            pi1 = pivot
        else:
            pi2 = pivot
            break
    if pi1 is not None and pi2 is not None:
        deltah = _interpolation.interpolation_date(dt=dte,
                                                   dt1=pi1.dte, v1=pi1.deltah,
                                                   dt2=pi2.dte, v2=pi2.deltah)
        return hauteur + deltah

    # observation ultérieure au dernier point pivor
    if pi1 is not None and pi2 is None:
        return hauteur if pi1.deltah == 0 else None
    # observation antérieure au premier point pivots
    if pi1 is None and pi2 is not None:
        return hauteur if pi2.deltah == 0 else None


def courbetarage_active(courbestarage, dte):
    """Retourne la courbe de tarage active

    Arguments:
        courbestarage: a CourbeTarage or an iterable of CourbeTarage
        dte (datetime.datetime): date de rechercher

    Return : CourbeTarge or None : la première courbe de tarage active
    """
    if isinstance(courbestarage, CourbeTarage):
        courbestarage = [courbestarage]
    for ctar in courbestarage:
        if not isinstance(ctar, CourbeTarage):
            raise TypeError('courbestarage is not an iterable of CourbeTarage')
        if ctar.is_active(dte=dte):
            return ctar


def obsh_to_obsq(obsh, courbestarage):
    """Obtention d'une observation de débit
    à partir d'une observation de hauteur

    Arguments:
        obsh (obshydro.Observation) Observation hydro de hauteur
        courbestarage : iterbale of courbetarage.CourbeTarage

    Return obshydro.Observation Observation hydro de debit with a result
        which can be nan
    """
    methode = 8
    qualif = 16
    hauteur = obsh['res'].item()

    # cas hauteur non définie
    if _numpy.isnan(hauteur):
        debit = None
        cnt = 1
        qualif = 16
        return _obshydro.Observation(dte=obsh['dte'].item(),
                                     res=None, mth=methode, qal=qualif,
                                     cnt=cnt, statut=obsh['statut'].item())
    # Récupération courbe tarage active
    ctar = courbetarage_active(courbestarage, obsh['dte'].item())
    if ctar is None or not ctar.pivots:
        return _obshydro.Observation(dte=obsh['dte'].item(), res=None,
                                     mth=methode, qal=qualif, cnt=1,
                                     statut=obsh['statut'].item())

    # Cas hauteur en dessous de la courbe
    if hauteur < ctar.pivots[0].hauteur:
        debit = None
        cnt = 4
        qualif = 16
        return _obshydro.Observation(dte=obsh['dte'].item(),
                                     res=None, mth=methode, qal=qualif,
                                     cnt=cnt, statut=obsh['statut'].item())

    # Cas hauteur au dessus de la courbe de tarage
    if hauteur > ctar.pivots[-1].hauteur:
        debit = None
        cnt = 8
        qualif = 16
        return _obshydro.Observation(dte=obsh['dte'].item(), res=None,
                                     mth=methode, qal=qualif,
                                     cnt=cnt, statut=obsh['statut'].item())

    if ctar.typect == 0:
        debit, qualif_pivots = _debit_ctar_poly(hauteur, ctar)
    else:
        debit, qualif_pivots = _debit_ctar_puissance(hauteur, ctar)

    # calcul qualification entre la qualification des points pivots et celle
    # de l'observation'
    qualif = obsh['qal'].item() if obsh['qal'].item() is not None else 16
    qualif = min(qualif, qualif_pivots)

    # Vérification que la hauteur est bien dans la zone d'utilisation
    if ctar.limiteinf is not None:
        if hauteur <= ctar.limiteinf:
            qualif = 12
    if ctar.limitesup is not None:
        if hauteur >= ctar.limitesup:
            qualif = 12

    return _obshydro.Observation(dte=obsh['dte'].item(),
                                 res=debit,
                                 mth=methode,
                                 qal=qualif,
                                 cnt=obsh['cnt'].item(),
                                 statut=obsh['statut'].item())


def _debit_ctar_poly(hauteur, ctar):
    """Calcul du débit à partir d'une courbe de tarage active
    de type poly

    Arguments:
        hauteur (float)
        ctar (CourbeTarage) courbe de tarage poly à appliquer à la hauteur

    Return tuple debit,qualif (float or  None, int or None)
    """
    prev_pivot = None
    pivot = None
    for pivot in ctar.pivots:
        if pivot.hauteur == hauteur:
            debit = pivot.debit
            qualif = pivot.qualif if pivot.qualif is not None else 16
            return (debit, qualif)
        if prev_pivot is not None and pivot.hauteur == prev_pivot.hauteur:
            raise ValueError("Points pivots avec même hauteur")
        if pivot.hauteur > hauteur:
            break
        prev_pivot = pivot

    # cas à gauche de la courbe
    if prev_pivot is None or pivot is None:
        return (None, None)
    # cas à droite de la courbe
    if pivot.hauteur < hauteur:
        return (None, None)

    # entre deux points pivots regression linéaire
    # Q = a H + b entre les deux points pivots
    coefa = (pivot.debit - prev_pivot.debit) / \
        (pivot.hauteur - prev_pivot.hauteur)
    coefb = pivot.debit - coefa * pivot.hauteur
    debit = coefa * hauteur + coefb

    qualif1 = prev_pivot.qualif if prev_pivot.qualif is not None else 16
    qualif2 = pivot.qualif if pivot.qualif is not None else 16
    qualif = min(qualif1, qualif2)

    return (debit, qualif)


def _debit_ctar_puissance(hauteur, ctar):
    """Calcul du débit à partir d'une courbe de tarage active
    de type puissance

    Arguments:
        hauteur (float)
        ctar (CourbeTarage) courbe de tarage puissance à appliquer à la hauteur

    Return tuple debit,qualif (float or  None, int or None)
    """
    # Parcours des points pivots
    # Recherche du premier pivot avec h >= hauteur
    index = 0
    pivot = None
    for index, pivot in enumerate(ctar.pivots):
        # h = hauteur du premier point
        # le calcul est réalisé avec le 2ème point
        if index == 0 and pivot.hauteur == hauteur:
            continue
        if pivot.hauteur >= hauteur:
            break
    # à gauche de la courbe
    if index == 0:
        return
    # A droite de la courbe
    if index == (len(ctar.pivots) - 1) and pivot.hauteur < hauteur:
        return (None, None)
    if hauteur < pivot.varh:
        raise ValueError("hauteur {} inférieure à h0 {}".format(hauteur,
                                                                pivot.varh))
    debit = 1000 * pivot.vara * (hauteur-pivot.varh)**pivot.varb
    qualif = pivot.qualif if pivot.qualif is not None else 16
    return (debit, qualif)

def correction_hauteurs(seriehydro, courbecorrection, pivots=False):
    """Correction des hauteurs à partir d'une courbe de correction

    Arguments:
        seriehydro (obshydro.Serie): serie hydro
        ccor (CourbeCorrection) : courbe de correction à appliquer à la série
        pivots (bool): si True ajoute des points au niveau des pivots
        de la courbe de correction

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
                    hcor = hauteur_corrigee(dte=pivot.dte,
                                            hauteur=hauteur,
                                            ccor=courbecorrection)
                    obss_hcor.append(_obshydro.Observation(
                            dte=pivot.dte, res=hcor, mth=8,
                            cnt=obs.cnt, qal=obs.qal,
                            statut=obs.statut))

        hcor = hauteur_corrigee(dte=obs.Index,
                                hauteur=obs.res,
                                ccor=courbecorrection)

        obss_hcor.append(_obshydro.Observation(dte=obs.Index, res=hcor, mth=8,
                                               cnt=obs.cnt, qal=obs.qal,
                                               statut=obs.statut))
        prev_obs = obs

    # print(len(obss_hcor))
    return _obshydro.Serie(
        entite=seriehydro.entite,
        grandeur=seriehydro.grandeur,
        dtdeb=seriehydro.dtdeb,
        dtfin=seriehydro.dtfin,
        dtprod=_datetime.datetime.utcnow().replace(microsecond=0),
        observations=_obshydro.Observations(* obss_hcor))

def serieh_to_serieq(seriehydro=None, courbestarage=None,
                     courbecorrection=None, pivots=False):
    """Conversion d'une série hydro de hauteur en une série hydro de débit

    Arguments:
        seriehydro (_obshydro.Serie): une serie hydro
        courbestarage (an iterable of CourbeTarage): courbes de tarages
        courbecorrection (CourbeCorrection or None): courbe de correction
        pivots (bool): si True ajoute des points au niveau des pivots des
        courbes de tarage et de correction

    Return: (_obshydro.Serie): une serie hydro de débit
    """
    # check seriehydro
    if not isinstance(seriehydro, _obshydro.Serie):
        raise TypeError('incorrect seriehydro')
    if seriehydro.grandeur != 'H':
        raise ValueError('incorrect grandeur')
    if seriehydro.observations is None:
        serie = _copy.copy(seriehydro)
        serie.dtprod = _datetime.datetime.utcnow().replace(microsecond=0)
        return serie
    if courbestarage is None:
        courbestarage = []
    elif isinstance(courbestarage, CourbeTarage):
        courbestarage = [courbestarage]

    if courbecorrection is not None:
        seriehydro = correction_hauteurs(seriehydro, courbecorrection, pivots)

    prev_obsq = None
    prev_obstuple = None
    obssq = []
    for obstuple in seriehydro.observations.itertuples():
        observation = _obshydro.Observation(dte=obstuple.Index,
                                            res=obstuple.res,
                                            mth=obstuple.mth,
                                            qal=obstuple.qal,
                                            cnt=obstuple.cnt,
                                            statut=obstuple.statut)

        ctar = courbetarage_active(courbestarage, obstuple.Index)
        ctars = [ctar] if ctar is not None else []
        if pivots:
            # ajout des points intermédiaires de la courbe de tarage
            if prev_obstuple is not None and ctar is not None \
                    and len(ctar.pivots) > 0:

                if prev_obstuple.res <= obstuple.res:
                    hmin = prev_obstuple.res
                    hmax = obstuple.res
                else:
                    hmax = prev_obstuple.res
                    hmin = obstuple.res
                pivots_ctar = ctar.get_pivots_between_hauteurs(
                    hmin=hmin, hmax=hmax)
                if prev_obstuple.res > obstuple.res:
                    pivots_ctar = reversed(pivots_ctar)
                for pivot in pivots_ctar:
                    if pivot.hauteur > hmin and pivot.hauteur < hmax:
                        # interpolation de la date
                        dte = _interpolation.interpolation_date_from_value(
                            val=pivot.hauteur, dt1=prev_obstuple.Index,
                            val1=prev_obstuple.res, dt2=obstuple.Index,
                            val2=obstuple.res)
                        if prev_obsq is not None \
                                and prev_obsq['dte'].item() == dte:
                            # avoid points with same date
                            continue
                        observation_pivot = _obshydro.Observation(
                                dte=dte,
                                res=pivot.hauteur,
                                mth=obstuple.mth,
                                qal=obstuple.qal,
                                cnt=obstuple.cnt,
                                statut=obstuple.statut)
                        obsq = obsh_to_obsq(obsh=observation_pivot,
                                            courbestarage=ctars)
                        # Calcul continuite en fonction de l'observation précédente
                        cnt = obsq['cnt'].item()
                        if cnt != 1 and prev_obsq is not None:
                            prev_debit = prev_obsq['res'].item()
                            if _numpy.isnan(prev_debit):
                                obsq['cnt'] = prev_obsq['cnt'].item()

                        obssq.append(obsq)
                        prev_obsq = obsq
        if prev_obsq is not None \
                and prev_obsq['dte'].item() == observation['dte'].item():
            # avoid points with same date
            continue
        obsq = obsh_to_obsq(obsh=observation,
                            courbestarage=ctars)

        # Calcul continuite en fonction de l'observation précédente
        cnt = obsq['cnt'].item()
        if cnt != 1 and prev_obsq is not None:
            prev_debit = prev_obsq['res'].item()
            if _numpy.isnan(prev_debit):
                obsq['cnt'] = prev_obsq['cnt'].item()

        obssq.append(obsq)
        prev_obsq = obsq
        prev_obstuple = obstuple

    return _obshydro.Serie(
        entite=seriehydro.entite,
        grandeur='Q',
        dtdeb=seriehydro.dtdeb,
        dtfin=seriehydro.dtfin,
        dtprod=_datetime.datetime.utcnow().replace(microsecond=0),
        observations=_obshydro.Observations(* obssq))
