# Directory-Utilities

The script is intended to support directory utilities, such as
* Recursively traverse a directory to find n-largest files by size.
* Given a cluttered directory, sort the files based on *extension* and store them in user defined paths.

Directory-Utilities is currently supported on **Windows** and **Linux** platforms.

## Internal Working

### LocalData
The LocalData class is the base class for handling operations of storage and retriveal of local application data used by the script.


### ConfigFile
The configFile class derived form the *LocalData* class handles the config file required for the utility. The config file supports **get** and **set** functions to help the user in updating and retrieving infromation into and from the config file. The config file stores the following informations:
* #### Root
The *Root* indicates the base directory from which the utility should start scanning files to find n largest files. The default value is the users profile path.
* #### SourcePath
The *SourcePath* indicates the path for the source directory from which cluttering is to be removed. The default value is the **Desktop** directory of the user.
* #### DestinationPath
The *DestinationPath* indicates the path for the destination directory in which the cluttered files are to be sorted. The default value is the **Documents** directory of the user.
* #### ExcludedPattern
The *ExcludedPattern* stores a list of user defined glob patterns which are to be excluded from any operation on the directory files.

### ExtensionFile
The ExtensionFile class derived from the *LocalData* class handles the extensions required for sorting cluttered directories. The extension are stored as,
```
{
  <directory>: <list of extensions>,
  ...
}
```
**directory** is the directory name into which the files are to be stored and **list of extensions** indicates the the acceptable extensions for the particular directory.
The ExtensionClass supports **add**, **update**, **delete** methods to add a new category of extensions, update the extension list of a previously defined category or delete a category.

#### Note:
In case of a single extension belonging to more than one category, the extension will be assumed to be only with the lexicographically smallest *directory* name.

### LargestFile
The LargestFile class is responsible for computing n largest files by size in a directory. The class stores a **min-heap** of size *n* and based on the **Root** path specified in the config file scans *accepatble* files and returns the *n* largest files in the directory.

### ClutterRemover
The clutterRemover class is responsible for removing clutter from the *SourcePath* directory and storing the files in the *DestinationPath* directory. 
