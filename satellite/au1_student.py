"""
Program for simulation of satellite docking between satellite 1 and
satellite 2.

Parameters:
docked = 0      # Flag for controlling if the satellites
                # have docked (docked = 1) or not (docked = 0)
                
F = 300         # Initial force affecting satellite 1
            
m1 = 500        # Mass of satellite 1
x1 = -100       # Initial position of satellite 1
v1 = 10         # Initial velocity of satellite 1

m2 = 1000       # Mass of satellite 2
x2 = 0          # Initial position of satellite 2
v2 = 0          # Initial velocity of satellite 2

dt              # Time step. Updated in each iteration and given as
                # the difference in (absolute) time between current iteration
                # and previous iteration.

Task: Modify the function update_sat so that the positions and velocities 
of the satellites are updated corrected and obeying the laws of physics.
(see further instructions inside function update_sat).

Last update
Jorgen Ekman, 13 January 2023
"""
#import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import time

docked = 0  # Flag for controlling if the satellites
            # have docked (docked = 1) or not (docked = 0)
t_lim = 40  # The duration in seconds the simulation lasts.
            # Should be around 40 s at hand in, but can be changed during
            # the development of the function.
def update_sat(x1,x2,v1,v2,F,dt):
     
    global docked
    if docked == 1:     # Om satellit 1 har dockat med Satellit 2.
        mtot = m1 + m2          # Total massa
        vnew1 = v1 + F/mtot*dt  # Ny hastighet för satellit
        vnew2 = vnew1           # Satellit 2 får samma hastighet
        xnew1 = x1 + v1*dt      # Nytt läge för satellit 1
        xnew2 = xnew1 + 5       # Samma läge för satellit 2,
                               # men åtskilda med 5 meter
    else:
        vnew1 = v1 + F/m1*dt    # Ny hastighet för satellit 1
        vnew2 = v2              # Satellit 2 får samma hastighet som innan.
        xnew1 = x1 + v1*dt      # Ny hastighet för satellit 1
        xnew2 = x2 + v2*dt      # Ny hastighet för satellit 2
       
        if abs(xnew2-xnew1) < 5:     # Om avståndet mellan satelliterna är mindre än 5 m
            if abs(vnew2-vnew1) < 2.5: # Om skillnaden i satelliternas hastighet är mindre än 2 m/s.
                docked = 1           # Sätt variabel docked till 1. Inelastisk stöt har skett.
                vnew1 = m1*v1/(m1+m2) # den nya hastigheten
                vnew2 = vnew1 # Eftersom satelliterna är sammankopplade, är satellit 1s hastighet lika med satellit 2.
                xnew1 = x1 + vnew1 * dt  # uppdatering av positionen.
                xnew2 = xnew1 + 5 # Vi sätter de två satelliterna fem meter isär för att urskilja dem.
               
            else:   # i fallet av en elastisk stöt
               vnew1 = ((m1 - m2) * v1 + 2 * m2 * v2) / (m1 + m2)
               vnew2 = ((m2 - m1) * v2 + 2 * m1 * v1) / (m1 + m2)
             
               xnew1 = x1 + vnew1 * dt
               xnew2 = x2 + vnew2 * dt


           
    return xnew1,xnew2,vnew1,vnew2


# Initialisation of some parameters (don't change)

F = 300

m1 = 500
x1 = -100
v1 = 0

m2 = 1000
x2 = 0
v2 = 0

fig, ax = plt.subplots()
# Adjust figure to make room for buttons
fig.subplots_adjust(bottom=0.25)

# Create button which decrease force with 50 N.
decrax = fig.add_axes([0.2, 0.05, 0.2, 0.08])
decr_button = Button(decrax, 'Decrease Thrust', hovercolor='0.975')

def decr(event):
    global F
    F = F - 50.0
    
decr_button.on_clicked(decr)

# Create button which increase force with 50 N.
incrax = fig.add_axes([0.65, 0.05, 0.2, 0.08])
incr_button = Button(incrax, 'Increase Thrust', hovercolor='0.975')

def incr(event):
    global F
    F = F + 50.0
    
incr_button.on_clicked(incr)

tstart = time.time()
telapsed = 0
told = tstart
# Main loop startshere
while telapsed <= t_lim:
    # Deduce time and time step
    tnew = time.time()
    dt = tnew - told
    told = tnew
    
    # Call to function update_sat
    x1,x2,v1,v2 = update_sat(x1,x2,v1,v2,F,dt)
    
    telapsed = time.time() - tstart
    
    # Update plot
    ax.plot(x1,0,'wo')
    ax.plot(x2,0,'ro',markersize=10)
    ax.set_xlabel('x (m)',fontsize=12)
    ax.set_xlim([-150,50])
    ax.set_facecolor("black")
    ax.tick_params(labelsize=12, left = False, labelleft = False)
    
    # Update text
    textstr = '\n'.join((
    'Time: %6.2f s' % (telapsed,),
    'Distance: %6.2f m' % (abs(x2-x1), ),
    'Relative  velocity: %6.2f m/s' % (abs(v2-v1), )))
    props = dict(boxstyle='round', facecolor='wheat', alpha=1.0)
    ax.text(0.25, 0.9, textstr, transform=ax.transAxes, fontsize=12,
        verticalalignment='top', bbox=props)
    textstr2 = ('Force: %4.1f N' % (F))
    ax.text(0.4, -0.225, textstr2, transform=ax.transAxes, fontsize=12,
        verticalalignment='top')
    
    # If succesful docking
    textstring = "Docking succesful!!"
    if docked == 1:
        ax.text(0.5, 0.2, textstring, transform=ax.transAxes, color="white", fontsize=12,
        verticalalignment='top')
        
    plt.pause(0.1)
    
    # Don't clear the last plot
    if telapsed < t_lim:
        ax.cla()
    

    
    