# Garm (Generator of Animated Robot Model)

Garm is a library which transforms a robot model in [URDF][URDF],
which is the file format of robot in [ROS][ROS], 
into various 3D file formats with animation.

# Features

- converting robot model in [URDF][URDF] to 3D file formats [glTF][glTF] and [USD][USD].
- generating 3D animation files of robot in [glTF][glTF] and [USD][USD] from robot model in [URDF][URDF].
- converting robot model in [URDF][URDF] to other robot model.
- generating a template of [garm file](#GarmFile) from robot model in [URDF][URDF].

# Installation

Garm can be installed from [PyPI][PyPI] using `pip`:

    pip install garm

# Example Usage

## converting URDF to 3D files formats and vice versa.

### converting urdf to other formats

Here is an example on how to convert robot model in [URDF][URDF] to 3D file formats.

    from garm import garm
    garm.convert('robot.urdf', 'robot.glb')
    garm.convert('robot.urdf', 'robot.gltf')
    garm.convert('robot.urdf', 'robot.usdz')
    garm.convert('robot.urdf', 'robot.usda')

### converting other formats to urdf.

Here is an example on how to convert 3D file formats to robot model in [URDF][URDF].

    from garm import garm
    garm.convert('robot.glb', 'robot.urdf')
    garm.convert('robot.gltf', 'robot.urdf')

## generating 3D animation files of robot

Here is an example on how to generate 3D animation files of robot from robot model in [URDF][URDF].
We give a [garm file](#GarmFile) in [YAML][YAML] format, which is described below, as the third parameter to the function `convert`.

    from garm import garm
    garm.convert('robot.urdf', 'robot.glb', 'robot.garm')
    garm.convert('robot.urdf', 'robot.gltf', 'robot.garm')
    garm.convert('robot.urdf', 'robot.usdz', 'robot.garm')
    garm.convert('robot.urdf', 'robot.usda', 'robot.garm')

## converting urdf to other robot model and vice versa.

Here is an example on how to convert robot model in [URDF][URDF] to other robot model.

    from garm import garm
    garm.convert('robot.urdf', 'robot.mk3d')
    garm.convert('robot.urdf', 'robot.rdtf')
    garm.convert('robot.urdf', 'robot.usdr')

### converting other robot model to urdf

Here is an example on how to convert other robot model to robot model in [URDF][URDF].

    from garm import garm
    garm.convert('robot.mk3d', 'robot.urdf')
    garm.convert('robot.rdtf', 'robot.urdf')
    garm.convert('robot.usdr', 'robot.urdf')

<a id="GarmFile"></a>
# Garm file

Garm file is written in [YAML][YAML] format.

## Parameter of garm file

| Name             | Function          | Possible values         |
| ---------------- | ----------------- | ----------------------- |
| version          | number of version | number                  |
| asset (optional) | asset             | [*asset*](#asset)       |
| sources          | a set of source   | [*source*](#source)     |
| behaviors        | a set of behavior | [*behavior*](#behavior) |

### Example

    version: 0.3
    asset:
        ...............
    sources:
        ...............
    behaviors:
        ...............

<a id="asset"></a>
## *asset*

### Parameter of *asset*

| Name        | Function    | Possible values  |
| ----------- | ----------- | ---------------- |
| title       | title       | character string |
| copyright   | copyright   | character string |
| year        | year        | number           |
| license     | license     | character string |
| generator   | generator   | character string |
| attribution | attribution | character string |

### Example of *asset*

    asset:
      title: "Single Pendulum"
      copyright: "Copyright (C) 2023 MKLab.org (Koga Laboratory)"
      year: 2023
      license: "CC BY 4.0"

<a id="source"></a>
## *source*

### Parameter of *source*

| Name                  | Function                                             | Possible values                                                        |
| --------------------- | ---------------------------------------------------- | ---------------------------------------------------------------------- |
| name                  | name of source                                       | character string started with a alphanumeric character                 |
| url                   | filename, url of data                                | filename or URL (*csv*, *txt*, *mat*)                                  |
| numbers (optional)    | column numbers of data to be loaded                  | a list of column number separated by `,` and surrounded by `[` and `]` |
| timeShift (optional)  | shift the time so that the initial time is 0 if true | *true* or *false*                                                      |
| timeScale (optional)  | scale of time (default value is 1)                   | real number                                                            |

### Example of *source*

    sources:
     - name: "s1"
       url: "Simulation.mat"
     - name: "s2"
       url: "joint_states.csv"
       numbers: "[1, 7, 8]"
       timeShift: "true"
       timeScale: "1.0E-9"       

<a id="behavior"></a>
## *behavior*

### Parameter of *behavior*

| Name    | Function          | Possible values                           |
| ------- | ----------------- | ----------------------------------------- |
| name    | name | character string started with a alphanumeric character |
| actions | a set of action   | [*action*](#action)                       |

<a id="action"></a>
### Parameter of *action*

| Name      | Function             | Possible values                                        |
| --------- | -------------------- | ------------------------------------------------------ |
| name      | name                 | character string started with a alphanumeric character |
| timeRange | time range of action | startingTime and endingTime separated by `:`           |
| time      | time of action       | mathematical expression with [*source*](#source) variables and the time variable `t`                |
| motions   | a set of motion      | [*motion*](#motion)                                    |

<a id="motion"></a>
### Parameter of *motion*

| Name   | Function             | Possible values                   |
| -------| ---------------------| --------------------------------- |
| target | joint to be moved    | id (name) of joint in robot model |
| type   | type of motion       | *translation* or *rotation*       |
| value  | value of joint   | `"[dx, dy, dz]"`                  |

An element of *value* in [*motion*](#motion) is a mathematical expression with [*source*](#source) variables and the time variable `t`, where `s(2)` means the second element of the source data with name of "s". The mathematical expression can include the operations, such as '+', '-', '*', and '/', and many fundamental function, such as 'sin', 'cos', and 'exp'.

### Example of *behavior*

    behaviors:
    - name: "simulation"
      actions:
      - name: action1
        timeRange: 0:12
        time: s1(1)
        motions:
        - target: pendulum
          type: rotation
          value: "[s1(3), 0, 0]"
        - target: cart
          type: translation
          value: "[0, s1(2), 0]"
    - name: "experiment"
      actions:
      - name: "action1"
        time: "s2(1)"
        motions:
        - target: "base.joint"
          type: "translation"
          value: "[0, s2(2),  0]"
        - target: "cart.joint"
          type: "rotation"
          value: "[s2(3), 0, 0]"

# Generating a template of garm file

It is tedious work to write a [garm file](#GarmFile) from scratch.
We can generate a template of garm file from robot model and
modify a part of the file to complete.

### generating a template of garm file from robot model.

Here is an example on how to generate a template of garm file from robot model.

    from garm import garm
    garm.convert('robot.urdf', 'robot_urdf.garm')
    garm.convert('robot.mk3d', 'robot_mk3d.garm')

# Dependencies

Garm depends on the following Java libraries.
[GraalVM](https://www.graalvm.org/) was used to build shared libraries, which is called from python program, from Java libraries.

## [MK-LAB](https://www.mk.ces.kyutech.ac.jp/) libraries

- [jmatx](https://jmatx.mklab.org/index.html)
- [mikity3D](https://mikity3d.mk.ces.kyutech.ac.jp/)
- nfc
- [wheels](https://wheels.mklab.org/)

## Other libraries

- [jackson](https://github.com/FasterXML/jackson)  (Apache License Version 2.0)
- [simple-xml](https://sourceforge.net/projects/simple/) (Apache License Version 2.0)
- [snakeyaml](https://github.com/snakeyaml/snakeyaml) (Apache License Version 2.0)

# License

Garm is licensed under [Apache License Version 2.0](https://www.apache.org/licenses/LICENSE-2.0).

# Author

Garm was written by Masanobu Koga (<koga@ices.kyutech.ac.jp>) in 2022.

[glTF]:https://www.khronos.org/gltf/
[PyPI]:https://pypi.org/
[ROS]:https://wiki.ros.org/ 
[URDF]:http://wiki.ros.org/urdf
[USD]:https://openusd.org/release/index.html
[YAML]:https://yaml.org/
