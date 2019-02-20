# -*- coding: utf-8 -*-
"""Module de conversion de données élémentaire en débits moyens

Ce module permet de calculer des débits moyens journaliers et mensuels

"""

import numpy as _numpy
import datetime as _datetime
import calendar as _calendar


import libhydro.processing.htoq as _htoq
import libhydro.processing.interpolation as _interpolation
from libhydro.core import (obshydro as _obshydro,
                           obselaboreehydro as _obselaboreehydro)


def qmj_to_qmm(debitsjournaliers=None):
    """ Calcul de débits mensuels à partir de débits journaliers
    """
    obss = []
    # check type
    if isinstance(debitsjournaliers, _obselaboreehydro.SerieObsElab):
        if debitsjournaliers.typegrd != 'QmnJ':
            raise TypeError('typegrd of debitsjournaliers must be QmnJ')
        observations = debitsjournaliers.observations
    else:
        # TODO check Dataframe
        observations = debitsjournaliers

    if observations is None:
        return

    grouby_month = observations.groupby([observations.index.year,
                                         observations.index.month])
    month_count = grouby_month.count()  # Nombre de débits par mois non nuls
    month_min = grouby_month.min()  # min des colonnes
    month_max = grouby_month.max()  # min des colonnes
    month_sum = grouby_month.sum()  # somme des colonnes
    for debits_sum in month_sum.itertuples():
        year, month = debits_sum.Index
        dte = _datetime.datetime(year, month, 1)
        mth = 8
        qal = month_min.loc[debits_sum.Index]['qal']

        statut = month_min.loc[debits_sum.Index]['statut']
        # débit moyen continu si l'ensemble des débits sont continus
        cnt = month_max.loc[debits_sum.Index]['cnt']
        if cnt != 0:
            cnt = 1

        debits_count = month_count.loc[debits_sum.Index]['res']
        # mrange[1] nb jours du moiss
        mrange = _calendar.monthrange(year, month)
        if debits_count != mrange[1]:
            debit = _numpy.nan
        else:
            debit = debits_sum.res / debits_count
        obss.append(_obselaboreehydro.ObservationElaboree(
            dte=dte, res=debit, mth=mth, qal=qal, statut=statut, cnt=cnt))
    return _obselaboreehydro.ObservationsElaborees(*obss)


def serie_to_qmj(seriehydro=None, courbestarage=None,
                 courbecorrection=None):
    """ Calcul de débits moyens journalier à partir d'une série hydro
    et de courbes de tarage

    les courbes de tarage et la courbe de correction sont utilisés uniquement
    pour les séries H

    Pour les séries Q, on suppose que le débit évolue linéairement
    entre deux observations

    """
    obs1 = None
    prev_jour = None
    if seriehydro.observations is None:
        return

    if seriehydro.grandeur == 'H':
        # check courbestarage
        if courbestarage is None or not courbestarage:
            return
        # Correction des hauteurs si nécéssaire
        if courbecorrection is not None:
            # correction de la hauteur
            seriehydro = _htoq.correction_hauteurs(
                seriehydro=seriehydro,
                courbecorrection=courbecorrection)

    obss = []
    # Regroupement des observations en jours
    for obstuple in seriehydro.observations.itertuples():
        jour = obstuple.Index.date()
        obs2 = _obshydro.Observation(dte=obstuple.Index,
                                     res=obstuple.res,
                                     mth=obstuple.mth,
                                     qal=obstuple.qal,
                                     cnt=obstuple.cnt,
                                     statut=obstuple.statut)
        if obs1 is None:
            obs1 = obs2
            prev_jour = jour
            #  pas de calcul de débit moyen si la date de la prelière
            # n'est pas un jour rond
            if obstuple.Index.time() != _datetime.time():
                volume = _numpy.nan
            else:
                volume = 0.0
            statut = obstuple.statut
            qal = obstuple.qal
            continue

        # Changement de jour
        # calul du débit moyen des jours précédents
        # Réinitiliation diu débit moyen en cours de calcul
        while prev_jour != jour:
            # création des observations minuites afin de dissocier les volumes
            # avant et après minuit
            dte = _datetime.datetime(prev_jour.year,
                                     prev_jour.month,
                                     prev_jour.day) + \
                    _datetime.timedelta(days=1)
            res = _interpolation.interpolation_date(
                dt=dte,
                dt1=obs1['dte'].item(), v1=obs1['res'].item(),
                dt2=obstuple.Index, v2=obstuple.res)

            # création de l'observation minuit
            obs = _obshydro.Observation(
                dte=prev_jour + _datetime.timedelta(days=1),
                res=res,
                mth=obstuple.mth,
                qal=obstuple.qal,
                cnt=obstuple.cnt,
                statut=obstuple.statut)
            if seriehydro.grandeur == 'H':
                obsv = obsh_to_obsv(obs1, obs, courbestarage)
            else:
                obsv = obsq_to_obsv(obsq1=obs1, obsq2=obs)
            vel = obsv['res'].item()

            # TODO calcul du volume journalier
            volume += vel
            statut = min(statut, obsv['statut'].item())
            qal = min(qal, obsv['qal'].item())
            obselab_dte = _datetime.datetime(prev_jour.year,
                                             prev_jour.month,
                                             prev_jour.day)
            obselab = _obselaboreehydro.ObservationElaboree(
                dte=obselab_dte,
                res=volume / 86400,
                qal=qal,
                mth=8,
                statut=statut)
            obss.append(obselab)
            volume = 0.0
            statut = obstuple.statut
            qal = obstuple.qal
            obs1 = obs
            prev_jour += _datetime.timedelta(days=1)

        # calcul du volume élémentaire entre deux observations successives
        if seriehydro.grandeur == 'H':
            obsv = obsh_to_obsv(obsh1=obs1, obsh2=obs2,
                                courbestarage=courbestarage)
        else:
            obsv = obsq_to_obsv(obsq1=obs1, obsq2=obs2)

        # maj du débit oyen journalier
        vel = obsv['res'].item()
        volume += vel
        statut = min(statut, obsv['statut'].item())
        qal = min(qal, obsv['qal'].item())
        obs1 = obs2
        prev_jour = jour

    return _obselaboreehydro.ObservationsElaborees(*obss)


def obsh_to_obsv(obsh1, obsh2, courbestarage):
    """Retourne le volume élémentaire entre les deux points d'observations

    Le volume est calculé entre les deux observations en appliquant la courbe
    de tarage active
    """
    mth = 8
    if obsh1 is None or courbestarage is None:
        return _obshydro.Observation(dte=obsh2['dte'].item(),
                                     res=None,
                                     mth=mth,
                                     cnt=1)
    if obsh2 is None:
        raise TypeError('obsh2 must be not None')

    qal = min(obsh1['qal'].item(), obsh2['qal'].item())
    statut = min(obsh1['statut'].item(), obsh2['statut'].item())
    ctar = _htoq.courbetarage_active(courbestarage, obsh2['dte'].item())
    if ctar is None or not ctar.pivots:
        return _obshydro.Observation(dte=obsh2['dte'].item(),
                                     res=None,
                                     mth=mth,
                                     cnt=1,
                                     qal=qal,
                                     statut=statut)
    hauteur1 = obsh1['res'].item()
    hauteur2 = obsh2['res'].item()
    # cas hauteurs non définies
    if _numpy.isnan(hauteur1) or _numpy.isnan(hauteur2):
        return _obshydro.Observation(dte=obsh2['dte'].item(),
                                     res=None,
                                     mth=mth,
                                     cnt=1,
                                     qal=qal,
                                     statut=statut)

    # un des deux points en dessous de la courbe
    if min(hauteur1, hauteur2) < ctar.pivots[0].hauteur:
        return _obshydro.Observation(dte=obsh2['dte'].item(),
                                     res=None,
                                     qal=qal,
                                     mth=mth,
                                     cnt=4,
                                     statut=statut)
    # un des deux points au dessus
    if max(hauteur1, hauteur2) > ctar.pivots[-1].hauteur:
        return _obshydro.Observation(dte=obsh2['dte'].item(),
                                     res=None,
                                     qal=qal,
                                     mth=mth,
                                     cnt=8,
                                     statut=statut)

    if ctar.typect == 0:
        obsv = _htov_ctar_poly(obsh1, obsh2, ctar)
    else:
        obsv = _htov_ctar_puissance(obsh1, obsh2, ctar)
    # check zone de validite courbe de tarage
    if ctar.limiteinf is not None:
        if min(hauteur1, hauteur2) <= ctar.limiteinf:
            obsv['qal'] = 12
    if ctar.limitesup is not None:
        if max(hauteur1, hauteur2) >= ctar.limitesup:
            obsv['qal'] = 12
    return obsv


def obsq_to_obsv(obsq1, obsq2):
    """Retourne le volume élémentaire entre les deux points d'observations

    Le débit est linéaire entre les deux observations
    """
    mth = 8
    if obsq1 is None:
        return _obshydro.Observation(dte=obsq2['dte'].item(),
                                     res=None,
                                     mth=mth,
                                     cnt=1)

    if obsq2 is None:
        raise TypeError('obsq2 must be not None')

    qal = min(obsq1['qal'].item(), obsq2['qal'].item())
    statut = min(obsq1['statut'].item(), obsq2['statut'].item())
    debit1 = obsq1['res'].item()
    debit2 = obsq2['res'].item()
    # cas hauteurs non définies
    if _numpy.isnan(debit1) or _numpy.isnan(debit2):
        return _obshydro.Observation(dte=obsq2['dte'].item(),
                                     res=None,
                                     mth=mth,
                                     cnt=1,
                                     qal=qal,
                                     statut=statut)

    delta = (obsq2['dte'].item() - obsq1['dte'].item()).total_seconds()
    volume = 0.5 * (debit1 + debit2) * delta
    return _obshydro.Observation(dte=obsq2['dte'].item(),
                                 res=volume,
                                 mth=mth,
                                 qal=qal,
                                 cnt=0,
                                 statut=statut)


def _htov_ctar_poly(obsh1, obsh2, ctar):
    """calcul du volume

    Les hauteurs doivent être définies est compris dans la plage d'utilisation
    de la courbe

    """
    hauteur1 = obsh1['res'].item()
    hauteur2 = obsh2['res'].item()
    if hauteur1 > hauteur2:
        hauteur1 = hauteur2
        hauteur2 = obsh1['res'].item()
    statut = min(obsh1['statut'].item(), obsh2['statut'].item())
    deb1 = ctar.debit(hauteur=hauteur1)
    deb2 = ctar.debit(hauteur=hauteur2)
    qal = min(obsh1['qal'].item(), obsh2['qal'].item())
    mth = 8
    cnt = 0
    index1 = index_pivot_calcul(ctar, hauteur1)
    index2 = index_pivot_calcul(ctar, hauteur2)
    delta = (obsh2['dte'].item() - obsh1['dte'].item()).total_seconds()
    if delta == 0:
        return _obshydro.Observation(dte=obsh2['dte'].item(),
                                     res=0.0,
                                     qal=qal,
                                     mth=mth,
                                     cnt=cnt,
                                     statut=statut)
    volume = 0.0
    if index1 == index2:
        volume = (deb1 + deb2) * delta / 2
    else:
        prev_h = hauteur1
        prev_deb = deb1
        prev_t = 0
        for index in range(index1, index2):
            hauteur = ctar.pivots[index].hauteur
            debit = ctar.pivots[index].debit
            t = _interpolation.interpolation(x=hauteur, x1=hauteur1, y1=0,
                                             x2=hauteur2, y2=delta)
            volume += (debit + prev_deb) * (t - prev_t) / 2

            prev_h = hauteur
            prev_deb = debit
            prev_t = t
        # dernier point
        volume += (deb2 + prev_deb) * (delta - prev_t) / 2

    return _obshydro.Observation(dte=obsh2['dte'].item(),
                                 res=volume,
                                 qal=qal,
                                 mth=mth,
                                 cnt=cnt,
                                 statut=statut)


def _htov_ctar_puissance(obsh1, obsh2, ctar):
    """ Calcul du volume élémentaire entre les deux points

    Les hauteurs doivent être définies est compris dans la plage d'utilisation
    de la courbe

    """
    hauteur1 = obsh1['res'].item()
    hauteur2 = obsh2['res'].item()
    if hauteur1 > hauteur2:
        hauteur1 = hauteur2
        hauteur2 = obsh1['res'].item()

    mth = 8
    cnt = 0
    qal = min(obsh1['qal'].item(), obsh2['qal'].item())
    statut = min(obsh1['statut'].item(), obsh2['statut'].item())

    index1 = index_pivot_calcul(ctar, hauteur1)
    index2 = index_pivot_calcul(ctar, hauteur2)
    delta = (obsh2['dte'].item() - obsh1['dte'].item()).total_seconds()
    if delta == 0:
        return _obshydro.Observation(dte=obsh2['dte'].item(),
                                     res=0.0,
                                     qal=qal,
                                     mth=mth,
                                     cnt=cnt,
                                     statut=statut)
    volume = 0.0
    if index1 == index2:
        pivot = ctar.pivots[index1]
        # v = 1000 A (H-H0)^B * T
        if hauteur1 == hauteur2:
            volume = 1000 * pivot.vara * delta * \
                (hauteur1 - pivot.varh) ** pivot.varb
        else:
            coeff = (hauteur2 - hauteur1) / delta
            volume += 1000 * pivot.vara / (coeff * (pivot.varb + 1)) * \
                ((hauteur2 - pivot.varh) ** (pivot.varb + 1) -
                 (hauteur1 - pivot.varh) ** (pivot.varb + 1))
    else:
        prev_h = hauteur1
        # prev_deb = deb1
        prev_t = 0
        for index in range(index1, index2):
            pivot = ctar.pivots[index]
            hauteur = pivot.hauteur
            t = _interpolation.interpolation(x=hauteur, x1=hauteur1, y1=0,
                                             x2=hauteur2, y2=delta)
            coeff = (hauteur - prev_h) / (t - prev_t)
            volume += 1000 * pivot.vara / (coeff * (pivot.varb + 1)) * \
                ((hauteur - pivot.varh) ** (pivot.varb + 1) -
                 (prev_h - pivot.varh) ** (pivot.varb + 1))
            prev_h = hauteur
            # prev_deb = deb1
            prev_t = t
        # volume élémentaire entre le point pivot index2-1 et le dernier point
        pivot = ctar.pivots[index2]
        coeff = (hauteur2 - prev_h) / (delta - prev_t)
        volume += 1000 * pivot.vara / (coeff * (pivot.varb + 1)) * \
            ((hauteur2 - pivot.varh) ** (pivot.varb + 1) -
             (prev_h - pivot.varh) ** (pivot.varb + 1))
    return _obshydro.Observation(dte=obsh2['dte'].item(),
                                 res=volume,
                                 qal=qal,
                                 mth=mth,
                                 cnt=cnt,
                                 statut=statut)


def index_pivot_calcul(ctar, hauteur):
    """Retourne l'index du point pivot situé après la hauteur

    Cet index sert pour le calcul des volumes élémentaires

    """
    # absence de points
    if not ctar.pivots:
        return
    # en dessous de la courbe
    if hauteur < ctar.pivots[0].hauteur:
        return
    if hauteur > ctar.pivots[-1].hauteur:
        return
    for index, pivot in enumerate(ctar.pivots):
        if pivot.hauteur >= hauteur:
            # 1er point courbe ct puissance inutilisable
            if index == 0 and ctar.typect == 4:
                continue
            return index
