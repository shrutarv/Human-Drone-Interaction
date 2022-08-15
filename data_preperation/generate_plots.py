import numpy as np
import matplotlib.pyplot as plt

gesture_data_path = '/home/violet/Master_Thesis/Human-Drone-Interaction/data_preperation/gesture_data.npy'
gesture_data_rescaled_path = '/home/violet/Master_Thesis/Human-Drone-Interaction/data_preperation/gesture_data_rescaled.npy'
gesture_data = np.load(gesture_data_rescaled_path)

# Data visualisation - calculate the average of each gesture and plot the avg gesture 
swipe_left= gesture_data[0:280,:,:] 
swipe_right= gesture_data[280:560,:,:] 
swipe_up= gesture_data[560:840,:,:] 
swipe_down= gesture_data[840:1120,:,:] 
h_cw_crl= gesture_data[1120:1400,:,:] 
h_ccw_crl= gesture_data[1400:1680,:,:] 
v_cw_crl= gesture_data[1680:1960,:,:] 
v_ccw_crl= gesture_data[1960:2240,:,:] 

gesture_avgs = {
'swipe_left_avg' : np.average(swipe_left,axis=0),
'swipe_right_avg' : np.average(swipe_right,axis=0),
'swipe_up_avg' : np.average(swipe_up,axis=0),
'swipe_down_avg' : np.average(swipe_down,axis=0),
'h_cw_crl_avg' : np.average(h_cw_crl,axis=0),
'h_ccw_crl_avg' : np.average(h_ccw_crl,axis=0),
'v_cw_crl_avg' : np.average(v_cw_crl,axis=0),
'v_ccw_crl_avg' : np.average(v_ccw_crl,axis=0),
}

plots_path = '/home/violet/Master_Thesis/Human-Drone-Interaction/data_preperation/plots/'
for key in gesture_avgs.keys():
    fig, axs = plt.subplots(2)
    fig.suptitle(key)
    axs[0].plot(gesture_avgs[key][:,0],label='x')
    axs[0].plot(gesture_avgs[key][:,1],label='y')
    axs[0].plot(gesture_avgs[key][:,2],label='z')
    axs[0].legend(loc='upper right')
    axs[0].set_title('Accelerometer')
    axs[0].set(xlabel='Time steps')
    axs[1].plot(gesture_avgs[key][:,3],label='x')
    axs[1].plot(gesture_avgs[key][:,4],label='y')
    axs[1].plot(gesture_avgs[key][:,5],label='z')
    axs[1].legend(loc='upper right')
    axs[1].set_title('Gyroscope')
    axs[1].set(xlabel='Time steps')
    fig.tight_layout()
    plt.savefig(plots_path+key+'.jpg')