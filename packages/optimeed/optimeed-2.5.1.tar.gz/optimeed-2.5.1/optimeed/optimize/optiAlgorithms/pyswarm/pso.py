import numpy as np


def _is_feasible(theList):
    return np.all(np.array(theList) <= 0)


def _format_fx_fs(objectives_pop, constraints_pop):
    fx = np.zeros(len(objectives_pop))
    fs = np.zeros(len(constraints_pop), dtype=bool)
    for i in range(len(fx)):
        fx[i] = objectives_pop[i][0]
        fs[i] = _is_feasible(constraints_pop[i])
    return fx, fs


def pso(lb, ub, initialVectorGuess, theEvaluator, terminationCondition, callback_generation=lambda objectives, constraints: None, swarmsize=100, omega=0.5, phip=0.5, phig=0.5):
    """Perform a particle swarm optimization (PSO)

    :param lb: List. Lower bounds of each parameter
    :param ub: List. Upper bounds of each parameter
    :param initialVectorGuess: List. initial vector guess for the solution (to be included inside population)
    :param theEvaluator: object define before
    :param terminationCondition: Termination condition with shouldTerminated method
    :param callback_generation: function lambda (objectives (as list), constraints (as list)) per step
    :param swarmsize: Int. The number of particles in the swarm (Default: 100)
    :param omega: Float. Particle velocity scaling factor (Default: 0.5)
    :param phip: Float. Scaling factor to search away from the particle's best known position (Default: 0.5)
    :param phig: Float. Scaling factor to search away from the swarm's best known position (Default: 0.5)
    :return: (g) array The swarm's best known position (optimal design). (f) scalar, the objective value at (g)
    """

    lb = np.array(lb)
    ub = np.array(ub)

    vhigh = np.abs(ub - lb)
    vlow = -vhigh

    # Initialize the particle swarm ############################################
    S = swarmsize
    D = len(lb)  # the number of dimensions each particle has
    x = np.random.rand(S, D)  # particle positions
    # v = np.zeros_like(x)  # particle velocities
    p = np.zeros_like(x)  # best particle positions
    # fx = np.zeros(S)  # current particle function values
    # fs = np.zeros(S, dtype=bool)  # feasibility of each particle
    fp = np.ones(S)*np.inf  # best particle function values
    # g = []  # best swarm position
    fg = np.inf  # best swarm position starting value
    fsg = True

    # Initialize the particle's position
    x = lb + x*(ub - lb)

    x[0, :] = initialVectorGuess[:]  # inserted initial guess in population

    # Calculate objective and constraints for each particle
    results = theEvaluator.evaluate_all(x)
    obj = np.array([result['objectives'] for result in results])
    cons = np.array([result['constraints'] for result in results])
    fx, fs = _format_fx_fs(obj, cons)

    # Store particle's best position (if constraints are satisfied)
    i_update = np.logical_and((fx < fp), fs)
    p[i_update, :] = x[i_update, :].copy()
    fp[i_update] = fx[i_update]

    # Update swarm's best position
    i_min = np.argmin(fp)
    if fp[i_min] < fg:
        fg = fp[i_min]
        g = p[i_min, :].copy()
    else:
        # At the start, there may not be any feasible starting point, so just
        # give it a temporary "best" point since it's likely to change
        g = x[0, :].copy()

    # Initialize the particle's velocity
    v = vlow + np.random.rand(S, D)*(vhigh - vlow)

    # Iterate until termination criterion met ##################################
    while not terminationCondition.shouldTerminate():
        rp = np.random.uniform(size=(S, D))
        rg = np.random.uniform(size=(S, D))

        # Update the particles velocities
        v = omega*v + phip*rp*(p - x) + phig*rg*(g - x)
        # Update the particles' positions
        x = x + v
        # Correct for bound violations
        maskl = x < lb
        masku = x > ub
        x = x*(~np.logical_or(maskl, masku)) + lb*maskl + ub*masku

        # Update objectives and constraints
        results = theEvaluator.evaluate_all(x)
        obj = np.array([result['objectives'] for result in results])
        cons = np.array([result['constraints'] for result in results])

        fx, fs = _format_fx_fs(obj, cons)

        callback_generation(obj, cons)
        # Store particle's best position (if constraints are satisfied)
        i_update = np.logical_and((fx < fp), fs)
        p[i_update, :] = x[i_update, :].copy()
        fp[i_update] = fx[i_update]

        # Compare swarm's best position with global best position
        i_min = np.argmin(fp)
        if fp[i_min] < fg:
            p_min = p[i_min, :].copy()
            g = p_min.copy()
            fg = fp[i_min]
            fsg = fs[i_min]
    return g, fg, fsg

