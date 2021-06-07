
# Data Structure Editor (DSE)

This is a Web-application for creation of data structures and interface descriptions of IIoT devices.
It can generate source code for application services running on the Arrowhead Framework (https://github.com/arrowhead-f/core-java-spring).
This software has been developed as proof of concepts developed in the Productive 4.0 project (https://productive40.eu/).
It is not production safe code.
One of the next tasks would be to update this concept demonstrator to the newest version of the Arrowhead Framework.


## Scope

In distributed applications like IoT networks, information is exchanged between participants of a communication network by use of symbols.
These symbols may indicate a name (address) or a value of information and they are encoded as patterns of bits and bytes.
The information sink evaluates the symbols received from the information source.
For that purpose, it needs prior knowledge about the semantics of at least some symbols, which can be created by the information source.
Technical systems acting as information source are therefore described e.g. by a description of the server API in a client/server architecture or by descriptions of messages appearing in a publisher/subscriber architecture.

The DSE is a Web application, which allows a forms based description of API's of servers.
Additionally, the DSE provides partial source code (skeletons) for the API implementation of the servers, which is generated based on the API descriptions.
The current version of the DSE uses the a 2020 available version of the Arrowhead Framework (<https://github.com/arrowhead-f/core-java-spring>) as target communication platform.


## Terminology

**Data Structure:**
This is a collection of simple numerical and textual data types, other referenced structs and lists of previously mentioned data types.
All members of the struct are communicated at once.

**Data Block:**
This is a collection of data block members.
Each data block member defines a simple numerical or textual data type, references a data structure or a list of previously mentioned data types.
Data block members are communicated separately and have their own transmission characteristics and further attributes.

**Data Structure and Block Library:**
This is a formal description of data structures and blocks.
An XML schema is used to define the structure of such a library.

**Equipment:**
This is a technical system implementing a server at run-time.

**Equipment Type:**
This is an abstract term used to describe a server at design-time, which is later on deployed on a concrete technical equipment.

**Equipment Type Interface Description:**
This is a formal description of an interface of an equipment type.
It contains references to well defined data blocks.
An XML schema is used to define the structure of such an equipment type interface description.

**Skeleton:**
A skeleton is a part of the server-side source code.
It implements an equipment type interface description.
The business logic has to be added.


## Test environment

We used a development and test environment with following main properties:

  - Kubuntu 18.04 - a KDE-based Linux
  - Git v2.17.1 - version control system
  - Python v3.9.5 - server backend programming language (we didn't used special features of 3.9, so earlier versions of Python3 should work too)
  - Node.js v15.1.0 - frontend programming language (JavaScript)
  - npm v7.0.8 - Node.js package manager
  - Vue.js v2.6.10 - frontend framework
  - Arrowhead Framework - repository https://github.com/arrowhead-f/core-java-spring, commit 7e89135648ab00de68c481fddf0c7a0ac8381afa

You have to follow the steps described in the README file of the Arrowhead Framework repository to get all necessary core services running (serviceregistry, authorization, orchestrator).
It might be necessary to adapt the ./backend/data/generic_application.zip file from a newer version of the demo-car example of the official examples (https://github.com/arrowhead-f/sos-examples-spring), since the development of the Arrowhead Framework is going faster than this application, 


## Management of the frontend application

You have to enter the fronend directory:

```
cd ./frontend
```

In this directory you have to install the necessary libraries:

```
npm install @vue/cli
npm install
```

For checking of errors you may lint your program:

```
npm run lint
```

In order to minify and prepare the fronend application for production:

```
npm run build
```


## Management of the backend application


You have to enter the fronend directory:

```
cd ./backend
```

If you use jetbrains PyCharm, then you have to create a virtual environment from inside of this IDE and to install the libraries described in requirements.txt.
For example you can use "Help/Find Action" and search for "Create VirtualEnv", add a new Python interpreter and follow the proposed steps to create a new virtual environment.
Then open "requirements.txt" in PyCharm and near the top line you will be prompted to install the requirements.

In the general case, you should use the standard approach to create a virtual environment and install the requirements:

```
python3 -m venv ./venv
```

Activate the virtual environment:

```
source venv/bin/activate
```

All following commands are considered to be performed in the activated virtual environment.

Update pip:

```
pip install --upgrade pip
```

Install the libraries:

```
pip install -r requirements.txt
```

You can deactivate your environment simply by executing:

```
deactivate
```

## How to use the software

### Preface

The software available here is developed for concept testing within the Productive 4.0 project (https://productive40.eu/).
The concepts to be tested concern the following functions:

  - Defining data structures that can be used later when describing device interfaces.
  - Describing device interfaces using the defined data structures.
  - Generating source code for devices from the descriptions of device interfaces.
  
Other supporting concepts have been partially implemented.
This concerns e.g. the automated version management of the data structure and device descriptions.
As soon as a new description of data structures or of devices is created, a Git repository is also created at the same time.
Other actions, such as the automated creation of commits after changes to the files, would still need to be added.

Similarly, role-based user management is provided in the backend.
This would allow each HTTP-based REST service on the backend to be assigned which roles can run that service.
For a production deployment, it would need to be decided which roles can run which services.
Also, a list of users would need to be maintained to which appropriate roles are assigned.
Currently, we assume that one logs in as an administrator and operates the application.
Since the application is currently configured to run only on the local machine (localhost), the administrator's password is immediately entered in the corresponding input field.
This would of course have to be changed in productive use.

The following sections describe how the core concepts can be tested with the software available here.


### Starting the server and opening the user frontend

It is assumed that all necessary software libraries of the frontend and backend applications have been installed.

If you want to use the example data structures, blocks and equipment type interface descriptions, then you can unzip the data.zip file, so that the folders "backend", "frontend" and "data" are on the same base folder.
On Linux you could use the following command:

```
unzip data.zip
```

Once you have unzipped the examples, you can play with data structure libraries and equipment type interfaces.
The imaginary "Industrie 4.0 Consortium" (see Library Folders) has some libraries from which at least "Hydraulic Pump" has data structures and blocks.
The "DepartmentHydraulics" (see Equipment Type Interfaces / Repositories) provides an equipment interface description "PumpDescription" with references to data blocks of the "Hydraulic Pump" library.
The "PumpDescription" has a cloud-download button, where you can trigger the code generation and download.

Now you can start the server in the backend directory:
```
source venv/bin/activate
python api.py
```

Then you can call the URL "http://localhost:8081/" in the address bar of a web browser.
In the displayed login dialog the already entered password can be confirmed.
The login password is currently fixed in the file "DataStructureEditor.vue".
This would have to be removed in productive operation.


### Defining data structures and blocks

On the left side of the application you will find a navigation bar.
Data structures and data blocks are defined in the section "Data Structure and Block Libraries".
This concerns in detail:

  - **Library Folders**: This is a folder where the libraries are stored. Version management is also maintained at this level. In large companies, there are often independent organizational units (business units) that develop software independently of one another. However, it is also possible that other companies or standardization organizations define some of the data structures to be used. For such organizational units, one would create appropriate folders. A library can be pulled from a URL (cloud symbol in the "Data Structure and Block Library Folders" line). A push-back is currently not implemented (cloud-up-arrow). You can create (+ sign), select (check symbol), edit (pen symbol) or delete (trash can symbol) a library folder.

  - **Libraries**: A library defines a self-contained set of data structures and data blocks. Such a library is stored in a file. You can create (+ sign), select (check symbol), edit (pen symbol) or delete (trash can symbol) a data structure library.

  - **Data Structure Definitions**: A data structure is comparable to a record in common programming languages (C - struct, Pascal - record, Java/C# - class, ...). A data structure contains members to which simple data types or array data types are assigned. You can create (+ sign), select (check symbol), edit (pen symbol) or delete (trash can symbol) a data structure.

  - **Data Block Definitions**: A data block also contains entries to which data types are assigned. In contrast to the members of the data structures, however, additional communication parameters are assigned to each entry of a data block, e.g. the direction of communication (in/out/in-out) or the transfer characteristic (cyclic, acyclic). So to transmit a complex data structure as a unit one would first define the data structure and then define an entry in a data block whose data type refers to the data structure definition. The transfer parameters are then assigned to this block entry. You can create (+ sign), select (check symbol), edit (pen symbol) or delete (trash can symbol) a data block.


### Defining device interface descriptions

Device interface descriptions are defined in the section "Equipment Type Interfaces".
This concerns in detail:

  - **Repositories**: This is a folder where the equipment interface descriptions are stored. Version management is also maintained at this level. Enterprise business units can maintain their interface descriptions in different of those repositories. A repository can be pulled from a URL (cloud symbol in the "Equipment Description Folders" line). A push-back is currently not implemented (cloud-up-arrow). You can create (+ sign), select (check symbol), edit (pen symbol) or delete (trash can symbol) an equipment description repository.

  - **Equipment Interface Descriptions**: An interface description defines the interface of a technical equipment. It contains references to data blocks defined in the data structure and block libraries. An equipment interface description library is stored in a file. You can create (+ sign), select (check symbol), edit (pen symbol) or delete (trash can symbol) an equipment interface description.

  - **Data Block Instances**: A data block instance is a part of an equipment interface description. They refer to data blocks defined in the data structure and block libraries. You can create (+ sign), select (check symbol), edit (pen symbol) or delete (trash can symbol) a data block reference.


### Generating and testing device interface code

The section "Equipment Interface Descriptions" contains for each interface description an additional 'cloud-arrow-down' symbol.
If you click on it, then it will download a "generic_application.zip" file.
You should extract it in a separate folder.

It contains a modified "demo-car" project from the Arrowhead examples GitHub page (https://github.com/arrowhead-f/sos-examples-spring).

We have not changed much in the structure of the project.
Therefore, the Java source codes are still arranged in the package structure defined by the authors of the demo-car project (apparently by AITIA http://www.aitia.ai/).
For production, this package structure should be adapted anyway by the company generating the source code.

The essential file that was generated is located here:

    application_framework/<description>/src/main/java/ai/aitia/demo/car_provider/controller/GenericEquipmentInterface.java

The two lines are to be understood as a common file path.
The <description> contains the name of the description from which you started the download by pressing the 'cloud-arrow-down'-symbol.

The file "GenericEquipmentInterface.java" contains 3 essential functions:

  - **getData(blockName, entryName)**: This is the method to access the device data. The complex "if" statement contained in it initially returns preset values for the addressed block entry.

  - **getInterfaceDescription()**: This method returns a self-description about all blocks and entries provided by this device.
  
  - **test()**: This method returns an HTML page that provides links to the self-description and to each block entry of the device. Following the links gives JSON representations of the self-description and the current values of the block entries.
  
This interface code must now be extended by the device developer.
If, for example, one wants to represent a MODBUS TCP device via Arrowhead services, then one must include a corresponding communication library in the generated Java project (e.g. http://easymodbustcp.net).
Then in the target file "GenericEquipmentInterface.java" the developer must first get the values, e.g. of the MODBUS TCP holding register, in the "getData" method.
Then the "dummy_float64", "dummy_int64", ... values must be replaced by values obtained from the MODBUS TCP data.
This is a very simple way of implementation, which can be further improved e.g. by caching strategies.


## Acknowledgements

The research  work leading to  this demonstrator has received  grants as project Productive 4.0 from the European H2020 research and innovation programme and the ECSEL  Joint  Undertaking under  grant  agreement  no. GAP-737459 – 999978918 as well as from the German Federal Ministry of Education and Research (FKZ 16ESE0185). We are grateful to have been given that opportunity for our research activities.


## References

An article is available about the why, what and how of this tool: Thron, M.; Zipper, H.; Bangemann, Th.: Efficient Engineering of IIoT Systems Based on Interoperability Standards, Materials, Methods & Technologies, Volume 14, 2020; online available: https://www.scientific-publications.net/en/article/1002061/ (last visited 2021-04-30).


## Copyright and License Information

Copyright (c) 2021, Institut für Automation und Kommunikation e.V. (ifak e.V.).
See the LICENSE file for licensing conditions (MIT license).
