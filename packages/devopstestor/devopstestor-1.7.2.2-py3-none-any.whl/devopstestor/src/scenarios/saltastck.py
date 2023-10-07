def initialise_context(machine_provisionner, init_contexte, pillar, **kwarg):
    # Reinitialise les pillars a partir des donnes fournis pas le testcase
    statut, stdout = machine_provisionner.set_pillars(init_contexte, merge=False)
    if statut == False: # Cas d'erreur
        return statut, stdout # inutils de continuer le scenario

    # Ajout des pillars specifiques
    return machine_provisionner.set_pillars(pillar)

def appliquer_etats(machine_provisionner, init_contexte={}, sls_cible=None, saltenv=None, pillar={}, **kwarg):
    statut, stdout = initialise_context(machine_provisionner, init_contexte, pillar)
    # Ajout du role
    if statut == False: # Cas d'erreur
        return statut, stdout # inutils de continuer le scenario

    # Lancement du deploiement
    statut, stdout = machine_provisionner.runStateApply(
        saltenv=saltenv,
        sls_cible=sls_cible
    )

    return statut, stdout
