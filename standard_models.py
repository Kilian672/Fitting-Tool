def sir_model (xs, ts, ps, time_slot, parameter_list):
    
    try:   
        params = parameter_list
        beta = ps[params[0]+'_{}'.format(time_slot)].value
        gamma = ps[params[1]+'_{}'.format(time_slot)].value
    
    except:
        pass
        #beta, gamma = ps

    s, i, r,  = xs
    n = s+i+r

    

    #eval("-beta*s*i/n")
    return [-beta*s*i/n, beta*s*i/n-gamma*i, gamma*i]


def sird_model (xs, ts, ps, time_slot, parameter_list):
    
    try:   
        
        params = parameter_list
        beta = ps[params[0]+'_{}'.format(time_slot)].value
        gamma = ps[params[1]+'_{}'.format(time_slot)].value
        delta = ps[params[2]+'_{}'.format(time_slot)].value
 
    except:
        pass
        #beta, gamma = ps

    s, i, r, d = xs
    n = s+i+r+d
    return [-beta*s*i/n, beta*s*i/n-gamma*i-delta*i, gamma*i, delta*i]

def sis_model (xs, ts, ps, time_slot, parameter_list):
    
    try:   
        params = parameter_list
        beta = ps[params[0]+'_{}'.format(time_slot)].value
        gamma = ps[params[1]+'_{}'.format(time_slot)].value
    
    except:
        pass
        #beta, gamma = ps

    s, i  = xs
    n = s+i
    return [-beta*s*i/n+gamma*i, beta*s*i/n-gamma*i]

def seir_model (xs, ts, ps, time_slot, parameter_list):
    
    try:   
        params = parameter_list
        beta = ps[params[0]+'_{}'.format(time_slot)].value
        epsilon = ps[params[1]+'_{}'.format(time_slot)].value
        gamma = ps[params[2]+'_{}'.format(time_slot)].value
    
    except:
        pass
        #beta, gamma = ps

    s, e, i, r,  = xs
    n = s+e+i+r
    return [-beta*s*i/n, beta*s*i/n-epsilon*e, epsilon*e-gamma*i, gamma*i]

def sirs_model (xs, ts, ps, time_slot, parameter_list):
    
    try:   
        params = parameter_list
        beta = ps[params[0]+'_{}'.format(time_slot)].value
        gamma = ps[params[1]+'_{}'.format(time_slot)].value
        tau = ps[params[2]+'_{}'.format(time_slot)].value
    
    except:
        pass
        #beta, gamma = ps

    s, i, r,  = xs
    n = s+i+r
    return [-beta*s*i/n+tau*r, beta*s*i/n-gamma*i, gamma*i-tau*r]

def seirs_model (xs, ts, ps, time_slot, parameter_list):
    
    try:   
        params = parameter_list
        beta = ps[params[0]+'_{}'.format(time_slot)].value
        epsilon = ps[params[1]+'_{}'.format(time_slot)].value
        gamma = ps[params[2]+'_{}'.format(time_slot)].value
        tau = ps[params[3]+'_{}'.format(time_slot)].value
    
    except:
        pass
        #beta, gamma = ps

    s, e, i, r,  = xs
    n = s+e+i+r
    return [-beta*s*i/n+tau*r, beta*s*i/n-epsilon*e, epsilon*e-gamma*i, gamma*i-tau*r]
