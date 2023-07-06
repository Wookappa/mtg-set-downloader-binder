# MTG Set Scryfall Downloader

This repository contains two Python scripts that allow you to download Magic: The Gathering card images from the Scryfall API using a specific set code. Additionally, it includes a script to generate a `.HTML` file for Binder.

## Scripts

- `MTG_Set_ScryfallDownloader.py`: This script enables you to download card images for a specific Magic: The Gathering set from the Scryfall API. It prompts the user to enter the set code and SSL verification preference, then proceeds to download the card images into the `art` directory within the repository. The script relies on the Scryfall API for accessing card data.

- `Binder_Generator.py`: Generates an `.HTML` page that represents a card binder for the Magic: The Gathering cards downloaded using the MTG Set Scryfall Downloader script. The generated HTML file, named `binder.html`, provides a visual representation of the downloaded cards, organized in a grid-like format. It includes interactive features such as image previews, pagination, and navigation buttons to browse through the card collection.

## Prerequisites

Before using the scripts, make sure you have Python (version 3.x) installed on your system. Also, ensure that you have the following Python packages installed:

- `requests`
- `ijson`

These packages can be installed using the Python package manager, pip:

```shell
pip install -r requirements.txt
```

## Usage

1. Clone the repository to your local machine:

   ```shell
   git clone https://github.com/Wookappa/mtg-set-dowloader-binder.git
   ```

2. Navigate to the repository directory:

   ```shell
   cd mtg-set-dowloader-binder
   ```

3. Run the desired script:

   - For downloading card images:

     ```shell
     python MTG_Set_ScryfallDownloader.py
     ```

   - For generating Binder:

     ```shell
     python Binder_Generator.py
     ```
        This will prompt you to select an image folder containing the downloaded Magic: The Gathering card images.
        
        1. Select the image folder:        
          You will be presented with a list of folders in the `art/` directory.
          Enter the number corresponding to the desired image folder.
        2. Specify the grid size:
          Enter the number of rows and columns you want to display in the grid.
        3. The default grid size is 8 rows and 4 columns.
        4. The binder.html file will be generated based on your selections.
        
        Open the binder.html file in a web browser to view the card binder representation of the downloaded Magic: The Gathering cards.
        
        The generated HTML page provides an interactive and visually appealing way to browse through your downloaded card collection. It allows you to view card images, navigate between pages, and explore the cards within the binder.
        
        Please note that the `Binder_Generator.py` script should be executed after running the `MTG_Set_ScryfallDownloader.py` script to download the card images. Ensure that the downloaded card images are present in the designated art directory before running `Binder_Generator.py`.
        
        For more details on the MTG Set Scryfall Downloader script and its usage, refer to the MTG Set Scryfall Downloader section in the README.

## Note

- Make sure to comply with the terms of use of the Scryfall API and the API usage policies when using the scripts.
- The proper functioning of the scripts relies on the availability of the Scryfall API. Ensure that the API is accessible and operational before running the scripts.
- These scripts are provided "as is" without any warranty. The author assumes no responsibility for any damages arising from the use of these scripts.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
