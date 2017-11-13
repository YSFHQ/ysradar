##############################################################################

	AirTrafficController for YSFlight System

					Client
					Ver.02/05/07
					wtr(mailto:atc_ysflight@yahoo.co.jp)

##############################################################################


This is an ATC radar for YSFLIGHT(http://www.ysflight.com/)

This program is under testing.
The server program of this program is running on "minmin-ys.ddo.jp" server.

*About minmin-ys.ddo.jp server*
The administrator is minmin.
This server is mainly for civilian airplanes but including some JASDF airplanes.
Currently used map is "KINKI MAP" at http://stargear.web.fc2.com/ (Japanese site).


*Disclaimer*
There is no warranty, expressed or implied, associated with this product.
Use at your own risk.


*QuickStart*
1.Execute "client.exe".
2.A small window ,I'll call it "standby window",will appear.
3.From the menu,select "Power->Connect to ATCserver"
4.Success massage should appear.Then select "Power->RadarOn".

*PAR*
This is so called "Precise Approach Radar".
Select ".par file" (which define the runway's heading and position.)
The glidepath is showed above,and the localizer is showed below.
Arrival airplane(s) in 10miles will be showd with the altitude and the course direction like "Left of course".

*Radar*
Airplanes under 100ft are not showed.

Left click on an airplane or the data tag to remove the airplane from the radar screen for a few second.
Left click with "Alt" pressed on a "point" (which is defined in *.point files) to move the center position to the point.
Left click with "Shift" pressed at two position to calculate distance(mile) and degree between the two clicked point.
Center click on an airplane or the data tag to move the tag.(4direction:northeast,northwest,southwest,southeast)
Right click on a "point" to remove it till restarting the radar window.

*Settings*
Select RadarSetting->range to set range of the radar.
Input positive numeral such as 1,3,or 0.2 and press "enter".

Select RadarSetting->read .point(.line/.dash) to read *.point(*.line/*.dash) files.
If you already open the radar window,you have to restart it to reflect the data.(do not close the standby window)

Select RadarSetting->initialize to initialize all settings.

See also pictures folder.

*How to edit *.point, *.line and *.dash files*

*History*

