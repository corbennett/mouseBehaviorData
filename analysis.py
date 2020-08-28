import numpy as np
import glob, os
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches

def checkforMouseBehaviorObject(directory, mouseID):

	print('checking {} for mouse object pkl'.format(directory))
	pkllist = [f for f in os.listdir(directory) if '.pkl' in f]
	mouseID = str(mouseID)
	pklpath = None
	for pkl in pkllist:
		if pkl[:6]==mouseID:
			pklpath = os.path.join(directory, pkl)
			print('Found existing mouseBehaviorObject'
			' for mouse {}'.format(mouseID))
	if pklpath is None:
		print('Did not find existing' 
			'mouseBehaviorObject for mouse {}'.format(mouseID))
	return pklpath


def plot_weight_over_time(beh_df):

	fig, ax = plt.subplots()
	ax.plot(beh_df['session_datetime_local'], beh_df['Wt_g'], 'k-o')
	ax.set_title('Wt_g')
	ax.tick_params(axis='x', labelrotation=45)

def plot_water_allotment(beh_df):

	fig, ax = plt.subplots()
	ax.plot(beh_df['session_datetime_local'], beh_df['WE_ml'], 'b-o')
	ax.plot(beh_df['session_datetime_local'], beh_df['WS_ml'], 'r-o')
	ax.plot(beh_df['session_datetime_local'], beh_df['WE_ml']+beh_df['WS_ml'], 'k-o')
	ax.legend(['WE_ml', 'WS_ml', 'Total'])
	ax.tick_params(axis='x', labelrotation=45)


def plot_inferred_presession_weight(beh_df, water_loss_during_session=0.3):

	post_wt = beh_df['Wt_g'].astype(float)
	earned_wt = beh_df['WE_ml'].astype(float)
	inferred_wt = post_wt - earned_wt + water_loss_during_session

	fig, ax = plt.subplots()
	ax.plot(beh_df['session_datetime_local'], inferred_wt, 'g-o')
	ax.set_title('Wt_g - WE_ml + {}: inferred pre-session weight'.format(water_loss_during_session))
	ax.tick_params(axis='x', labelrotation=45)


def plotSessionHistory(beh_df):
    
        def getColorAlphaFill(row):
            a = 1.0
            f = 'full'
            if 'NP' not in row['rig']:
                c = 'k'
            elif 'HAB' in row['stage']:
                c = 'm'
            else:
                c = 'g'
            
            if 'low_volume' in row['stage']:
                a = 0.3
                f = 'none'
            return c,a,f

        
        fig, ax = plt.subplots()
        artists_for_legend = []
        labels_for_legend = []
        colors_used = []
        for ir, row in beh_df.iterrows():  
            num_rewards = row['trials']['cumulative_reward_number'].max()
            c,a,f = getColorAlphaFill(row)
            ax.plot(row['session_datetime_local'], num_rewards, c+'o', alpha=a, fillstyle=f, mew=3)
        
        ax.set_xlabel('Sessions')
        ax.set_ylabel('num rewards')
        ax.set_xticks([row['session_datetime_local'] for _,row in beh_df.iterrows()][::2])
        ax.set_xticklabels([row['session_datetime_local'].date() for _,row in beh_df.iterrows()], rotation=90)
        plt.tight_layout()
        
        k_patch = mpatches.Patch(color='k', label='NSB')
        m_patch = mpatches.Patch(color='m', label='HAB')
        g_patch = mpatches.Patch(color='g', label='EPHYS')

        ax.legend(handles=[k_patch, m_patch, g_patch])