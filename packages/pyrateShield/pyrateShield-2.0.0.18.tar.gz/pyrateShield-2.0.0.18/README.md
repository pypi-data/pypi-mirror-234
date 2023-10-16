# Pyrateshield

An application to perform complex radiation shielding calculations for nuclear medicine and radiology departments.

![mainscreen](img/mainscreen.png)

## Introduction

Pyrateshield is a python application that performs radiation shielding calculations for nuclear medicine and radiology departments in hospitals. The application has a user friendly graphical interface and no python coding or commandline intereactions are needed at all.

The application is intended to calculate the (necessary) radiation shielding in entire radiology and nuclear medicine departments. Nuclear Medicine sources, CT sources and Xray sources can be defined and positioned on a floorplan in the GUI.  Walls with a defined thickness and material can be drawn using the mouse. The radiation dose rate can be visualized as heatmaps and (dose) isocontours on the floorplan. Critical points can be added to calculate the exact dose rate in specific points. Critical point results can be easily exported to Excel.

## Table of contents

[toc]



## Intended users 

(Medical) physicists and radiation protection officers who are working at a nuclear medicine or radiology department in a hospital. 

## Installation & getting started

### Windows

For windows standalone executables are distributed. To obatain a standalone executable, check the Downloads section in the repository:

[standalone windows executables](https://bitbucket.org/MedPhysNL/pyrateshield/downloads/)


### Cross Platform

Use 'pip install pyrateshield' to install the package in a python environment of your choice. Type 'pyrateshield' to start the application. Pyrateshield requires python version 3.8 or later. Python savy users can also install directly from our [repository](https://bitbucket.org/MedPhysNL/pyrateshield).


When using an anaconda environment and having spyder installed within that environment may cause issues with spyder. Best practice is not to install pyrateshield and spyder within the same anaconda environment. A workaround could be reinstalling pyqt5 after installing pyrateshield('pip install pyqt5==version', with version the required version by spyder). 

### Examples

Pyrateshield projects can be saved as a .zip file. There are a few examples available on the repository. The example zip files can be obtained from the Downloads section in the repository:

[examples](https://bitbucket.org/MedPhysNL/pyrateshield/downloads/)

There is no need to extract the .zip files. In pyrateshield select load from the toolbar and select the .zip file to open the project.

### Legacy

Older version of pyrateshield use .psp files to store projects. They can still 
be read by later version of pyrateshield and saved as the newer .zip files

## Using Pyrateshield

### Toolbar

At the top of pyrateshield is a toolbar with icons. Loading, Saving and adding elements is started from the toolbar. 

![toolbar](img/toolbar.png)

Below a brief explanations of all icons in the toolbar:

Item|Description
----|---
pyShield|Calculate a dosemap and display the dosemap over the floorplan with the pyshield engine
Radtracer|The same but using the Radtracer engine
New|Start a brand new pyrateshield project
Image|Load a bitmap image as floorplan
Floorplan|Remove the displayed heatmap and show the (clean) floorplan
Reset|Reset Zooming and Panning to the default view
Pan|Pan the image by using the mouse (left click and hold)
Zoom|Draw a rectangular selection box on the floorplan to define the region to zoom in to
Move|Move all pyrateshield objects (Wall, sources and critical points) while keeping the floorplan in place. Usefull to align objects with a new floorplan
Source NM|Select and click on the floorplan to add a new Source NM. See section Source NM
Source CT|Select and click on the floorplan to add a new Source CT. See section Source CT
Source Xray|Select and click on the floorplan to add a new Source Xray. See section Source Xray
Wall|Select and draw a new wall on the floorplan (click and hold left mouse button, see section Wall)
Critical Point|Select and click on the floorplan to add a new Critical Point. See section Critical Point
Delete|Delete the selected / highlighted pyrateshield object from the floorplan (and project). Action cannot be undone(!)
Snapshot|Take a snapshot of the floorplan (and dosemap if displayed) and save as a bitmap image
Load|Load a pyrateshield project file (.zip) from disk
Save|Save pyrateshield project to disk
Save As|Save pyrateshield project to disk and select (new) filename
Calculator|Simple calculator to calculate the shielding properties of a wall with a single material and thickness. Useful for quick calculations and to inspect differences between the pyshield and Radtracer engine.
Dosemap Style|Styling properties for the dosemap that is displayed on top of the floorplan image
Isotopes|Inspect the isotope definitions for pyrateshield (energies and abundances). New isotopes cannot be added at this moment.


### Toolbox

On the left side of the interface a toolbox is displayed that allows inspecting and modifying properties of all pyrateshield objects. 

![toolbox](img/toolbox.png)



Below an explanation of all different objects and their properties.

#### NM Sources

By clicking in the toolbar on Source NM icon a Nuclear Medicine source can be added to the floorplan. Click on the floorplan to position the new Nuclear Medicine Source.

A Nuclear Medicine Source has the following properties:

Property|Description
--------|-----------
Name| Name of the source 
Number of exams| Number of times for which the source is present in the room (per year)
Activity [MBq]| Activity of the Source in MBq
Isotope| Isotope
Self shielding| Self shielding of source (None, Body or factor)
Factor| Manual self selfshielding or correction factor (available when Self shielding is set to Factor)
Duration [h]| Duration for which a source is present in the room
Apply decay correction| Correct for physical decay during duration for which the source is present
Clearance Model| Select biological clearance model name (See section Clearance)
Position| Position in cm of the source on the floorplan
Enabled| When unchecked source is disabled and excluded from calculations

#### Clearance

Clearance models are optional and mainly used to define a source that represents a therapy patient who stays overnight in a nuclear medicine therapy facility. The clearance model allows to correct for excretion of radioactivity.

The clearance model can be defined as an monoexponentional or biexponential model. Physical decay is always applied (if the decay correction property of the NM Source is checked). The exponentials can be split by a fraction or by a time. When split by fraction and  the fractions (or the single fraction for a monoexponential model) do not add up to 1, the remaining fraction is corrected for phsyical decay (if the decay correction property of the NM Source is checked). When the exponentials are split in time the first fraction will be integrated until the defined split time and the second fraction from split time. Integration is always stopped after source duration (see section NM Sources). By default a set of decay models are available that are prescribed int the Dutch guidelines ('werken met therapeutische hoeveelheden radionucliden').

Property|Description
--------|-----------
Name| Name of the clearance model
Fraction 1| If applied the fraction (between 0 and 1) for the first exponential.
Halflife [h]| The corresponding (biological) halflife for the first exponential
Fraction 1| If applied the fraction (between 0 and 1) for the second exponential.
Halflife [h]| The corresponding (biological) halflife for the second exponential.
Split fractions by time| Set the time where both exponentials are split. When applied fraction 1 and fraction 2 are always 1.

Click Add to add a new clearance model and click delete to delete the selected clearance model.


#### Sources CT

For the calculation of CT sources a simple model for secondary scatter is implemented, based on Wallace et.al. 2012: Establishment of scatter factors for use in shielding calculations and risk assessment for computed tomography facilities. A single scatter factor of 0.36 uGy per unit of DAP (mGy cm) for body and 0.14 uGy/(mGy cm) for head is used for all directions, at 1 m from the scanner isocenter. To add a Source CT select the Source CT icon form the toolbar and click on the floorplan to add the source at that location.

Property|Description
--------|-----------
Name| Name of the source 
kVp| The kVp setting of the CT
Number of exams| Number of times the exam is repeated (per year)
Body part| The CTDI model (Head or Body) <reference needed>
DLP [mGycm]| The dose length product for this exam in mGy cm
Position| Position in cm of the source on the floorplan
Enabled| When unchecked source is disabled and excluded from calculations

#### Sources Xray

For the calculation of Xray sources a simple model for secondary scatter is implemented, based on NCRP report 147 Fig. C.1. To add a Source Xray select the Source Xray icon form the toolbar and click on the floorplan to add the source at that location.

Property|Description
--------|:----------
Name| Name of the source 
kVp| The kVp setting of the Xray machine
Number of exams| Number of times the exam is repeated (per year)
DAP [mGycm2]| The dose area product for this exam in mGy cm2
Position| Position in cm of the source on the floorplan
Enabled| When unchecked source is disabled and excluded from calculations

#### Walls

Walls are lines that can be drawn by selecting the Wall icon from the toolbar. Left click and hold left mouse button to start drawing the wall on the floorplan. Release the left mouse button to finish. 

Property|Description
--------|:----------
Shielding| The shielding assigned to this wall (see section shieldings)
X1, Y1, X2, Y2| Position in cm of the source on the floorplan

Select a wall with the left mouse button on the floorplan. Subsequently use the right mouse button on one of the square walls for additional drawing options.

Action| Description
---------|----------------
Delete| Delete selected wall
Copy | Copies the wall (yaml) definition to clipboard as text (for debugging or advanced use)
Continue Wall Here| Continue drawing of the wall from the selected wall ending
Snap to: | Snap selected wall ending to the nearest wall ending in range

#### Shieldings

Shieldings consist of one or two materials with a corresponding thickness. Shieldings are a preset and can be assigned to a wall (see section wall). A wall can therefore consist out of two different materials (e.g. lead and gypsum). When you change a shielding all the walls with the assigned shielding will also update

Property|Description
--------|:----------
Name| Name of the shielding
Material 1| Name of the first material (set to None to disable shielding)
Thickness 1 [cm] | Thickness of the first material
Material 2| Name of the first material (set to None to disable shielding)
Thickness 2 [cm] | Thickness of the second material
Select Color| Select the color of the shielding (to show the walls with this shielding assigned)
Linewidth [pt]| Line width of the shielding (to show the walls with this shielding assigned)

Click on Add to add a new shielding defintion or click on delete to delete the shielding definition. Shieldings can only be deleted when there are no walls that have this shielding assigned.


#### Materials

The material section shows the properties and implementation of the available materials in the Radtracer and pyshield engine. Materials can be added or modified to a limited extent. Radtracer has a limited set of materials available and pyshield has attenuation and buildup tables for an even more limited set of materials available. Pyshield for example uses the buildup table of Concrete for Concrete-Barite which is at best a rough approximation.

Property|Description
--------|:----------
Name| Name of the material
Density [g/cm^3]| Density of the material in [g/cm^3]
Radtracer Material| Material as defined in Radtracer (by default the same as the Name property)
Pyshield Attenuation Table| The attenuation table that pyshield will use
Pyshield Buildup Table| The buildup table that pyshield will use

Click on Add to add a new material defintion or click on delete to delete the material definition. Materials can only be deleted when there are no shieldings that have this material assigned.

Changing or adding materials is mostly usefull to accommodate for using materials with slightly different densities. Variations in density are handled well by both pyshield and Radtracer. The other options serve as main purpose to make the user aware of the approximations in pyshield.

#### Critical points

To add a Critical Point select the Critical Point icon from the toolbar and click on the floorplan to add the critical point at that location. Critical Points are points for which the dose will be calculated in the Critical Point Report (see section Critical Point Report).

Property|Description
--------|:----------
Name| Name of the critical point
Occupancy Factor| Correction factor for occupancy. Use 1 to not correct for occupancy
Position| Position in cm of the source on the floorplan
Enabled| When unchecked critical point is excluded from the critical point report 



#### Pixel Size [cm]

A typical project starts with loading a floorplan image. The floorplan images are loaded as bitmap images and lack any information regarding scale. To define the scale on the floorplan the pixel size is set in cm, the real world length in cm that corresponds to one pixel of the bitmap image. The pixel size can be set by hand or by defining a line on the floorplan for which length the real world length in [cm] is used. For example the distance between columns.

Any changes to the pixel size are applied after clicking confirm (!)

##### Set Fixed

Property| Description
---|---
Pixel size [cm]| Set the pixel size manually in cm

##### Measure

Click on Measure On Floorplan to select two points for which the real world distance in cm is known. After clicking on the button, click on the floorplan with the left mouse button to select the first point. Release the left mouse button and subsequently click on the second point.  

Property| Description
---|---
Real world distance [cm]| The known distance in cm in the real world
Distance [pixels]| The distance in pixels between the selected points (read only)
Pixel size [cm]| The calculated pixel size in cm (read only)

### Calculations

#### Dosemap

To calculate a dosemap with isodose contours select the canvas tab and click on the pyShield or Radtracer icon in the toolbar. 

#### Critical points

To calculate the results for Critical Points select the Critical Point Report Tab. Use the Calculate Critical Points button to display the results in a table. The table can be exported to Excel using the Save To Excel button.

The table is not automatically updated (!) 

When changing anything in your project recalculate the critical point report explicitly by using the Calculate Critical Points button.

## Implementation (pyshield and Radtracer)

Pyrateshield implements two independently developed engines to perform the dose calculations: pyShield and Radtracer. The main difference between these engines lies in the way in which photon fluence behind the barriers (i.e. transmission) due to NM sources is calculated. The conversion from photon fluence to dose is handled in a similar way for both engines.

The first, pyshield uses buildup and attenuation tables and calculates the dose rate behind a wall (or multiple walls) by calculating the contribution of each gamma ray defined for the isotope. 

Radtracer uses presimulated results for the available materials and isotopes using [MCNP](https://mcnp.lanl.gov), a Monte Carlo simulator for particle transport. 


Dose rates due to Xray and CT sources are always handled in the same way, irrespective of whether pyshield or Radtracer is selected. The scatter fractions (i.e. DAP or DLP to scattered dose conversion) and the transmission parameters are obtained from literature.


### Limitations (pyshield and Radtracer)

#### Skyshine and multiple scatter

For nuclear medicine sources no secundary scatter contributions are included (skyshine). Skyshine cannot always be neglected. Skyshine heavily depends on the 3D geometry of the rooms. For Xray and CT sources only secondary radiation is included in the calculations (scatter from the body / object in the scanner). Primary radiation (leakage) or tertiary scatter is not included.

#### Attenuation through multiple materials

Changes in energy spectrum by transmission through multiple walls is ignored. If all walls through which the transmission takes place are of the same material, the thickness is summed first ensuring an accurate calculation. However when walls consist of different materials a (safe) over estimation of the transmission is calculated by multiplying the transmission for each material and thickness without taking changes in the spectrum into account. Since the changes to the spectrum are ignored it also does not matter through which wall the radiation is transmitted first. 

#### Self shielding

Pyrateshield has an option self shielding for Sources NM. Pyshield implements this by adding transmission through 10 cm of water for each point (or point in the dosemap). Since buildup in water can be considerable and changes in the energy spectrum (see limitation 3) are ignored the doserate might even increase when setting self shielding to body. For pyshield 10cm of water is for some isotopes a very inaccurate representation of the self shielding of a patient. It is preferred to set a manual self shielding factor for Sources NM. It also possible to use the calculator in the toolbar to calculate the transmission through e.g. 15 cm or 20 cm of water and use that factor as a manual self shielding factor. 

In Radtracer, self shielding due to a patients body is implemented by surrounding the point source with a water filled shpere of radius 15 cm, prior to running the MCNP simulations. This ensures that buildup and hardening of the spectrum is properly accounted for. The obvious limitation of this method is that the assumption that a patient (and the activity distribution within the patient) can be estimated as a point source in a sphere might not be entirely accurate.

Due to the very different implementation of self shielding for pyshield and radracer, large differences may occur (!)

#### Materials

Pyshield has a limited set of tables for buildup and attenuation at present. Some materials are approximated by combining attenuation tables and buildup tables. The available materials are defined as follows in pyshield:

Material|Attenuation Table|Buildup Table
:-:|:-:|:-:
Lead|Lead|Lead
Concrete|Concrete|Concrete
Water|Water|Water
Concrete-Barite|Concrete-Barite|Concrete
Gypsum|Gypsum|Concrete
Brick|Brick|Concrete

Attenuation tables are derived from [NIST XCOM](https://physics.nist.gov/PhysRefData/Xcom/html/xcom1.html). Buildup tables were published by Shimizu et. al. [1]

#### Multiple gamma rays

For Radtracer, the entire esmission spectrum of the radio-isotope is simulated in MCNP. For a range of barrier thicknesses, the spectrum at a point behind the barrier is recorded and converted to an effective dose. These are stored in a lookup table which is used by Radtracer during execution.

Pyshield sums the contribution of each gammaray during each new calculation and therefore accurately accounts for multiple gamma rays. Pyshield neglects gammarays below 30 keV because no buildup data is available for these low energies. For unshielded sources with gamma rays below 30 keV differences between pyshield and Radtracer may be observed. When shielded these low energy gamma rays usually don't contribute to the dose.``

## References

[1] Shimizu A, Onda T, Sakamoto Y. Calculation of gamma-ray buildup factors up to depths of 100 mfp by the method of invariant embedding, (III) Generation of an improved data set. J Nucl Sci Technol 41: 413–424; 2004.



## Contact 

Developers:

Marcel Segbers, GUI architect and developer of pyshield, (m.segbers@erasmusmc.nl) 
Rob van Rooij, Co-developer and developer of Radtracer, (r.vanrooij-3@umcutrecht.nl)

Feature requests and bug reports please use the issue tracker of the repository:

https://bitbucket.org/MedPhysNL/pyrateshield
