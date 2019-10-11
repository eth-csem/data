import glob
import time
import yaml
import numpy as np
import matplotlib.pyplot as plt
import auxiliary as aux
import cartopy.crs as ccrs
import cartopy.feature as cfeature

start=time.time()

#==========================================================
#- General map settings.
#==========================================================

#- Scale and plot settings. -------------------------------

global_regional='regional'			#- 'regional' regional map, 'global' for global map.

event_markersize=7 				
event_marker='*'
event_color=[1.0, 0.0, 0.0]

station_markersize=5 				
station_marker='^'
station_color=[0.0, 1.0, 0.0]

ray_width=0.25

plot_sources_and_receivers=True
plot_rays=False

#- Regional maps (Mercator projection). -------------------
#- If these are vectors, then more than 1 map will be
#- produced.

lat_min=[20.0] 		#- Minimum latitude array [deg].
lat_max=[60.0] 		#- Maximum latitude array [deg].
lon_min=[-15.0] 	#- Minimum longitude array [deg].
lon_max=[55.0] 		#- Maximum longitude array [deg].

#- Global maps (Orthograpic projection). ------------------

lon_centre=[0.0]
lat_centre=[40.0]

#==========================================================
#- March through all the files and collect data.
#==========================================================

#- Open yaml file that contains the list of datasets in the right order.

fid=open('../Data/dataset_list.yml','r')
datasets=yaml.load(fid)
fid.close()

#- March through these datasets and make a list of region names and minimum periods.

periods=[]

evlo=[]
evla=[]
stlo=[]
stla=[]

n_region=[]

for dataset in range(len(datasets)):

	#- Open yaml file of that specific dataset.
	fid=open('../Data/'+datasets[dataset]['info_file'])
	info=yaml.load(fid)
	fid.close()
	periods.append(float(info['minimum_period']))

	#- Read source/receiver coordinates.
	evlo_tmp,evla_tmp,stlo_tmp,stla_tmp=aux.read_rays(datasets[dataset]['directory'])

	#- Print some statistics.
	n_events=aux.count_distinct_pairs(evla_tmp,evlo_tmp)
	n_stations=aux.count_distinct_pairs(stla_tmp,stlo_tmp)
	n_rays=len(evlo_tmp)
	string=datasets[dataset]['directory']+': rays: '+str(n_rays)+', stations: '+str(n_stations)+', events: '+str(n_events)
	print(string)

	#- Append to global list.
	evlo.append(evlo_tmp)
	evla.append(evla_tmp)
	stlo.append(stlo_tmp)
	stla.append(stla_tmp)
	n_region.append(len(evlo_tmp))

#- Statistics for all events.
n_events=aux.count_distinct_pairs([val for sublist in evla for val in sublist],[val for sublist in evlo for val in sublist])
n_stations=aux.count_distinct_pairs([val for sublist in stla for val in sublist],[val for sublist in stlo for val in sublist])
n_rays=len([val for sublist in evla for val in sublist])
string='total: rays: '+str(n_rays)+', stations: '+str(n_stations)+', events: '+str(n_events)
print(string)

#==========================================================
#- Loop over map settings. (Make a map for each setting.)
#==========================================================

if global_regional=='global':
	N=len(lon_centre)

elif global_regional=='regional':
	N=len(lat_min)

for n in np.arange(N):

	#- Set up the map. ----------------------------------------

	if global_regional=='regional':

		ax=plt.axes(projection=ccrs.Mercator(central_longitude=(lon_max[n]-lon_min[n])/2.0, min_latitude=lat_min[n], max_latitude=lat_max[n], globe=None, latitude_true_scale=None, false_easting=0.0, false_northing=0.0, scale_factor=None))
		ax.set_extent([lon_min[n],lon_max[n],lat_min[n],lat_max[n]])

	elif global_regional=='global':

		ax=plt.axes(projection=ccrs.Orthographic(central_longitude=lon_centre[n], central_latitude=lat_centre[n], globe=None))
		ax.set_global()

	ax.add_feature(cfeature.NaturalEarthFeature('cultural', 'admin_0_countries', '50m', edgecolor='black', facecolor=cfeature.COLORS['land']),zorder=2)
	ax.gridlines(zorder=3)

	evx=[]
	evy=[]
	stx=[]
	sty=[]

	#- Plot rays. ---------------------------------------------

	if plot_rays:

		print('plot rays')

		for idx in range(len(datasets)):

			if (datasets[idx]['directory']=='2017_Global'): 
				ray_color=(0.6,0.6,0.7)
			else:
				c=0.75*((periods[idx]-np.min(periods))/(np.max(periods)-np.min(periods)))
				ray_color=(c,c,c)

			#- Plot on map.
			for k in range(n_region[idx]):
				plt.plot([stlo[idx][k], evlo[idx][k]], [stla[idx][k], evla[idx][k]], color=ray_color, linewidth=ray_width, transform=ccrs.Geodetic() ,zorder=3)

	#- Plot events and stations. ------------------------------

	if plot_sources_and_receivers:

		print('plot sources and stations')

		for idx in range(len(datasets)):
			plt.scatter(stlo[idx][:],stla[idx][:],color=station_color, marker=station_marker, s=station_markersize, transform=ccrs.Geodetic(),zorder=4)
			plt.scatter(evlo[idx][:],evla[idx][:],color=event_color, marker=event_marker, s=event_markersize, transform=ccrs.Geodetic(),zorder=4)

	#- Finish. ------------------------------------------------

	ax.coastlines(resolution='50m',color='blue',zorder=5)
	end=time.time()
	print(['elapsed time: ', end-start, ' s'])

	plt.show()
	#plt.savefig('../Output/'+str(n)+'.png',format='png',dpi=700)
	#plt.close()
