## FGO drop screen parser

[![Discord server invite](https://discordapp.com/api/guilds/502554574423457812/embed.png)](https://discord.gg/TKJmuCR)

#### Settinngs and ref files layout
```
├── input
    ├── quest_1
        ├── files
            ├── material_ref_1
            ├── material_ref_2
            ├── currency_ref_1
            ├── ...
        ├── settings.json
        ├── quest_1_drop_screen_1.png
        ├── quest_1_drop_screen_2.jpg
        ├── ...
    ├── quest_2
        ├── ...
    ├── ...
```

#### Manually parse files

```
> python fgo_mat_counter.py -h
usage: fgo_mat_counter.py [-h] [-v] [-d] [-nc] [-i IMAGE]

Helper Script that uses basic image recognition via opencv to count mat drops in FGO Screenshots

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Enables printing info level messages
  -d, --debug           Enables printing debug level messages and creation of temporary images useful for debug
  -nc, --nocharSearch   Disable search and labeling for characters in images (improves performance outside events)
  -i IMAGE, --image IMAGE
                        Path to image to process
```
If you have the layout above, the script will use the `settings.json` and `files` ref folder. If the script can not find the `files` ref folder at the same level as the `--image`, the script will use the default refs and settings at `ref/` and `ref/settings.json`.

Example:
```
> python fgo_mat_counter.py -v -i input/quest_1/quest_1_drop_screen_1.png
``` 


#### Continously monitor the input folder
```
> python frontend.py -h
usage: frontend.py [-h] [-j NUM_PROCESSES] [-p POLLING_FREQUENCY]

optional arguments:
  -h, --help            show this help message and exit
  -j NUM_PROCESSES, --num_processes NUM_PROCESSES
                        Number of processes to allocate in the process pool
  -p POLLING_FREQUENCY, --polling_frequency POLLING_FREQUENCY
                        how often to check for new images in seconds
```
You can either run this script manually or you can run the Dockerfile. The script will monitor the `/input` folder, parse, move the parsed images and write the output jsons to `/output`. `/input` must have the layout above.
