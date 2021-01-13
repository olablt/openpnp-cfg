/**
 * Controls lighting for the two cameras using two named actuators. All
 * of the lights are turned off.
 */
 var upCamLights = machine.getActuatorByName("UpCamLights");
 var downCamLights = machine.getActuatorByName("DownCamLights");
 if (upCamLights) {
	upCamLights.actuate(false);
 }
 if (downCamLights) {
	downCamLights.actuate(false); 
 }
