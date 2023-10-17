# LMCV Tools

## 1 - Introduction

LMCV Tools is a **command line tool**  that provides a series of useful functionalities for the day-to-day simulations of the "Laboratório de Mecânica Computacional e Visualização" of the "Universidade Federal do Ceará" (UFC).

### 1.1 - Build and Install from Source

```text
$ pip install build
$ python -m build
$ pip install dist/[name of wheel file].whl
```

### 1.2 - How to Use

Once installed, the basic form of the LMCV Tools commands is:

```text
$ lmcv_tools [command] [flags] [args]
```

To check the installed version, use the command below:

```text
$ lmcv_tools version
```

To get help, it's possible use the following command:

```text
$ lmcv_tools help
```

To start ***Interactive Mode***, do not type any command and then you can type multiple commands in sequence:

```text
$ lmcv_tools
[Welcome Message]
>> [command]
output
>> [other command]
other output
```

For more complex commands, check out the detailed descriptions in the next section.

---

## 2 - Complex Commands

Considering that the routine activities for which LMCV Tools was developed are quite varied, specific commands were developed for each one of them. These commands are:
- translate (in implementation)
- extract (in implementation)
- generate (in implementation)
- reorder (in implementation)

### 2.1 - Translate

The command **translate**, in short, aims to convert different types of files used in LMCV.

Its usage is quite simple:

```text
$ lmcv_tools translate [path/to/file] to [extension]
```

### 2.1.1 - Translate .inp to .dat

Abaqus is a suite for Finite Element Analysis (FEA) developed by "Dassault Systèmes", while FAST is a console based FEA tool developed by "Laboratório de Mecânica Computacional e Visualização" of "Universidade Federal do Ceará" (UFC). Both of these softwares can simulate complex problems, but FAST has a clear disadvantage: differently of Abaqus, it hasn't a native GUI to generate its meshes. With that in mind, this command specifically seeks to translate meshes generated in Abaqus and exported in .inp format into meshes in .dat format to be used in FAST simulations.

Example:
```text
$ lmcv_tools translate Job-1.inp to .dat
```

### 2.1.2 - Translate .dat to .svg

Articles for scientific publications in the LMCV study field generally require images of the used meshes. Generating bitmat images in PNG format is a valid possibility, but for very discretized meshes this approach results in loss of details. Thinking about it, this command translates .dat files of **plate and shell** meshes to the SVG (Scalable Vector Graphics) image format, which does not lose quality with zoom (perfect for meshes with many elements).

Example:
```text
$ lmcv_tools translate Plate.dat to .svg
```

In addition, this command variation has an optional argument to choose the projection type. The supported projection types are listed bellow:
- plane_xy (**default**)
- plane_yz
- plane_xz
- isometric

Example:
```text
$ lmcv_tools translate Plate.dat to .svg isometric
```

### 2.2 - Extract

The command **extract**, in short, aims to extract data from .pos files generate by FAST and save this data in CSV format).

Files with extension ".pos" are the standard output from FAST simulations. They can store data about nodal displacements, element stresses, gauss points stresses and other informations, all distributed over a series of steps. In some contexts, it is necessary to obtain specific data from these files, but the manual search can take a lot of time and still fail. Alternatively, this command allows to extract entire set of related atributes by a simple expression.

An extraction expression can be broken down into terms:
- Keywords
- Attributes
- Condition

**Keywords** are a set of words that define the commmand syntax. In this command, the keywords are "from", "where" and "to" (the last two are optional). Examples of valid syntaxes are:

```text
$ lmcv_tools extract [atributes] from [path/to/.pos]
$ lmcv_tools extract [atributes] from [path/to/.pos] to [path/to/.csv]
$ lmcv_tools extract [atributes] from [path/to/.pos] where [condition]
$ lmcv_tools extract [atributes] from [path/to/.pos] where [condition] to [path/to/.csv]
```

**Attributes** are names that represent a piece of data from a .pos file. They follow a simple pattern: "[set name].[attribute name]". The supported attributes are:

| Attribute        | Meaning                                                                  |
| ---              | ---                                                                      |
| step.id          | Integer that identify analisys step.                                     |
| step.factor      | Float point factor of a step.                                            |
| node.id          | Integer that identify a node.                                            |
| node.x           | Float point coordinate on x-axis of a node.                              |
| node.y           | Float point coordinate on y-axis of a node.                              |
| node.z           | Float point coordinate on z-axis of a node.                              |
| step.node.u      | Float point displacement on x-axis of a node in specific step.           |
| step.node.v      | Float point displacement on y-axis of a node in specific step.           |
| step.node.w      | Float point displacement on z-axis of a node in specific step.           |
| buckling.id      | Integer that identify analisys buckling mode.                            |
| buckling.factor  | Float point factor of a buckling mode.                                   |
| buckling.node.u  | Float point displacement on x-axis of a node in specific buckling mode.  |
| buckling.node.v  | Float point displacement on y-axis of a node in specific buckling mode.  |
| buckling.node.w  | Float point displacement on w-axis of a node in specific buckling mode.  |
| vibration.id     | Integer that identify analisys vibration mode.                           |
| vibration.factor | Float point factor of a vibration mode.                                  |
| vibration.node.u | Float point displacement on x-axis of a node in specific vibration mode. |
| vibration.node.v | Float point displacement on y-axis of a node in specific vibration mode. |
| vibration.node.w | Float point displacement on w-axis of a node in specific vibration mode. |

All attributes that belong the same set can be related by "[set name].id" and extracted together. To do this, type them separeted by space before "from" keyword. The attributes will be related in order which they were typed. Example:

```text
$ lmcv_tools extract step.id step.factor step.node.u from Example.pos
```

Some attributes belong to multiple sets at the same time (e.g. "step.node.u"). They can be used to relate attributes that would not normally be extracted together. Example:

```text
$ lmcv_tools extract step.id step.node.u node.x from Example.pos
```

**Condition** is a series of attribute constraints. They can be written intuitively using attributes, operators and test values after "from" keyword. The supported operators are:

| Operator | Meaning                              |
| ---      | ---                                  |
| and      | Logical and.                         |
| or       | Logical or.                          |
| =        | Relational equal to.                 |
| >        | Relational gerater than.             |
| <        | Relational less than.                |
| >=       | Relational gerater than or equal to. |
| <=       | Relational less than or equal to.    |
| !=       | Relational different from.           |
| in       | Relational membership.               |

Remembering that the symbols ">" and "<" must be encapsulated by quotes. Otherwise, they will be interpreted by the shell as ***redirection operators***.

Examples:

```text
$ lmcv_tools extract step.factor from Example.pos where step.id ">" 2
```

```text
$ lmcv_tools extract step.factor from Example.pos where step.id != 3 and step.factor ">" 3
```

### 2.3 - Generate

The command **generate**, in short, aims to create special artifacts.

Artifact is a broad term for anything that can be useful for LMCV simulations. They can be file templates, dynamically generated file parts or anything else that needs a shortcut to create.

Possible Syntaxes:

```text
$ lmcv_tools generate [artifact name]
$ lmcv_tools generate [artifact name] [args] [path/to/artifact]
```

Implemented artifacts are listed below:
- virtual_laminas

#### 2.3.1 - Virtual Laminas
Virtual Laminas (virtual_laminas) are a model that approximates the behavior of a Functionally Graded Material. The idea is to represent these materials as a stack of isotropic homogeneous laminas. The more laminas used, the more accurate the simulation results. However, tools like Abaqus or FAST do not have a fast and automated way to generate these laminas, so this artifact was developed as a solution.

This syntax below will start a graphical interface to facilitate the process of passing arguments:

```text
$ lmcv_tools generate virtual_laminas
```

Other syntax possible is based in a long and exaustive list of required arguments:

```text
$ lmcv_tools generate virtual_laminas [args] [path/to/artifact]
```

| Parameters            | Description                                          |
| ---                   | ---                                                  |
| Laminas Count         | Total number of laminas.                             |
| Laminas Thickness     | Thinkcness of laminas.                               |
| Power Law Exponent    | Exponent of Power Law.                               |
| Micromechanical Model | Model to calculate effective properties.             |
| Element Type          | Supported: Solid, Shell.                             |
| E1                    | Elastic Modulus of Material 1.                       |
| E2                    | Elastic Modulus of Material 2.                       |
| nu1                   | Poisson's Coefficient of Material 1.                 |
| nu2                   | Poisson's Coefficient of Material 2.                 |
| pho1                  | Density of Material 1.                               |
| pho2                  | Density of Material 2.                               |
| Smart Laminas         | If True, a new smart generation method will be used. |

**Supported Micromechanical Models:**
- voigt
- mori_tanaka
- hashin_shtrikman_lower_bound
- hashin_shtrikman_upper_bound

### 2.4 - Reorder

The command **reorder**, in short, aims to add a node solver order in .dat files to reduce the stiffiness matrix bandwidth and, consequently, the time spent to execute the simulation.

Considering that computational simulations based on the finite element method involve the solution of a system of linear equations, it is possible to reduce the execution time of these simulations by also reducing the bandwidth of the stiffness matrix that represents the linear system. A valid approach for this is the reordering of the nodes that make up the simulation mesh. Thus, this command allows generating a reordering of nodes (a new node solver order) from different methods.

Possible Syntax:
```text
$ lmcv_tools reorder [method] [path/to/.dat]
```

Example:
```text
$ lmcv_tools reorder rcm simulation.dat
```

**Possible Flags:**
| Flag         | Function                            |
| ---          | ---                                 |
| -i or --info | Show info about bandwidth. reduction |

**Supported Reordering Methods**:
| Keyword     | Method                                              |
| ---         | ---                                                 |
| rcm         | [[1]](#3---references) Reverse Cuthill-McKee        |
| sloan       | [[2]](#3---references) Sloan                        |
| boost_sloan | Boost C++ Library Implementation of Sloan Algorithm |

## 3 - References

- [1] CUTHILL, E.; MCKEE, J.. Reducing the bandwidth of sparse symmetric matrices. Proceedings of The 1969 24th National Conference, Washington, p. 157-172, 26 ago. 1969. ACM Press. http://dx.doi.org/10.1145/800195.805928.
- [2] SLOAN, S. W.. An algorithm for profile and wavefront reduction of sparse matrices. International Journal for Numerical Methods in Engineering, Newcastle, v. 23, n. 2, p. 239-251, fev. 1986. Wiley. http://dx.doi.org/10.1002/nme.1620230208.