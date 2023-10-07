# MorphoNet

This is an API is used to interact with MorphoNet with python script.
You can find more help and tutorials on the MorphoNet website : http://www.morphonet.org

Help pages : https://morphonet.org/help_api

How to use : https://morphonet.org/helpfiles/API/index.html

Pip Project :https://pypi.org/project/morphonet/


This git contains :
- API(Net+Plot)
- Help API
- Script Build API Package to Pip

## Installation
This API work on python 3.7
You can simply install the MorphoNet API using   `pip install morphonet`

### Dependencies
The package will automatically install some dependencies :
* [numpy](https://pypi.org/project/numpy/)
* [scikit-image](https://pypi.org/project/scikit-image/)
* [scipy](https://pypi.org/project/scipy/) 
* [vtk](https://pypi.org/project/vtk/) (to convert the segmentation in meshes)
* [requests](https://pypi.org/project/requests/) (to interrogate the morphonet server)
* [imageio](https://pypi.org/project/imageio/) (for Image Handling)
* [nibabel](https://pypi.org/project/nibabel/) (to load and save in nii format)

## Examples

Some examples are here to help you get started in the [examples](examples) directory.
For example, [TestConnection.py](examples/basic/TestConnection.py)

## Authors

Emmanuel Faure  [1,2]

Benjamin Gallean [1,2]

Tao Laurent [2]


with theses affiliations

[1] Centre de Recherche de Biologie cellulaire de Montpellier, CRBM, CNRS, Université de Montpellier, France.
[2] Laboratoire d'Informatique, de Robotique et de Microélectronique de Montpellier (LIRMM), LIRMM, Univ Montpellier, CNRS, Montpellier, France.

*Correspondence should be addressed to Emmanuel Faure (emmanuel.faure@lirmm.fr)

## License
This project is licensed under the CeCILL License - see the [LICENSE](LICENSE) file for details
