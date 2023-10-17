# Installation

seEvo1D is python based lib available at pypi
```
python -m pip install seEvo1D
```
dependecies will be installed with program

# Usage

To run program simply type in command line
```
python -m seEvo1D
```
basicly seEvo is standalone program which provides possibility to simulate slighlty effect evolution in one dimension - slightly advantegous, slightly deleterious

# Instructions

Program contains 4 main views and main status UI

![Screenshot 2023-01-21 221838](https://user-images.githubusercontent.com/110567171/213887717-d77b2c92-37ec-46e0-974a-23aec88f0338.jpg)
![Screenshot 2023-01-21 221912](https://user-images.githubusercontent.com/110567171/213887739-cb461642-3300-4692-b326-96494b5223cc.jpg)

Output buttons provides possibility to draw images from saved files. Each file should have extension '.npz' as default from program. User can create multiple figures from multiple files. Each picture will be save to same directory from which file is loaded, in folder 'Figures'. 

population growth plot demands selection of multiple files to track population size.
combined mutation wave plot provides possibility to draw both analytic and simulated mutation wave on one plot. multiple files can be selected to draw on one figure.

![Screenshot 2023-01-21 221925](https://user-images.githubusercontent.com/110567171/213887744-cb66086b-56e8-4a57-b9ef-68d498ca4458.jpg)
![Screenshot 2023-01-21 221939](https://user-images.githubusercontent.com/110567171/213887745-0524bb73-77cf-4366-9140-f0191e2c28af.jpg)
![Screenshot 2023-01-21 221956](https://user-images.githubusercontent.com/110567171/213887746-efbc3573-9bd3-404c-a656-400e2e9b2c8d.jpg)

# License
  
GNU GENERAL PUBLIC LICENSE  Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
 
 ## Disclaimer
 
 seEvo - slighltly effect evolution simulator basing on Gillespie algorithm.
    Copyright (C) 2022 by Jarosław Gil

  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Author

Jarosław Gil, Silesian Univeristy of Technology, Department of Computer Graphics, Vision and Digital Systems.
