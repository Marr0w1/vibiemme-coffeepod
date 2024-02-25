# vibiemme-coffeepod
A 'daughterboard' to add 'automatic' functionality to manual espresso machines (auto-shot, reservoir tracker, temp control)

Latest Changes:
25/02/2024: first concept code for a 'menu' system added. This keeps the 'state' concept, but allows us to switch between modes using the rotary encoder. Currently the four modes are 1) sleep mode 2) display mode (eventually to include water level and boiler temp) 3) brew mode (eventually to include the brew function) and 4) set mode (where the rotary encoder is used to set the shot time used in brew mode)
25/02/2024: Use of a rotary potentiometer is now replaced by a rotary encoder. This provides multiple benefits, including increased granularity/range of setting brew time, integrating the button with the dial, allowing for 'menu' style navigation, and also freeing up one of our limited 'analog' inputs on the pico.
Feb 2024: Instead of using reservoir weight using a sliding potentiometer, we are using a Time-Of-Flight sensor (laser rangefinder) mounted on top of the reservoir. As water level drops, the distance between the surface and sensor increases, giving our water level. 

Currently in prototype stage, with pump activation emulated by an LED, while we wait for our donor machine to arrive.
![image](https://github.com/Marr0w1/vibiemme-coffeepod/assets/89231104/8534674c-b137-4569-ba6b-d84577b508cf)
