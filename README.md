# patch-matcher

The purpose of this site is to allow users to match objects between our test and gallery datasets.

![image](https://user-images.githubusercontent.com/60249654/186547537-141c802c-b21c-4170-95ea-39c07db3cbea.png)

Currently, the site allows users to navigate through sets of hotels and object categories. 

Problems:
 - Information is stored in csvs
 - Patches are created, stored, then erased when a user changes index
 - There is no check for preventing users from viewing the same hotel / object pair
 
ToDo:
 1. Implement matching feature
 2. Include option to flag patch as not of the given category
 3. Add more predicted objects to img_objects.csv, and hotel / object pairs to hotel_ids.csv
 4. Launch on server
  
