2020-03-20

I wrote this in about 20 minutes to download lidar data from DOGAMI.
Now I have published it to Wildsong's github so I will have to polish it up.
Improving open source, that's what pandemics are for.

--Brian

I think I generated the CSV from the DOGAMI map viewer,
or I might have done it in ArcGIS Pro? Struggling to remember now.
Give me a few minutes and I'll get back to you.

### Environment

    conda create --name=osgeo
    conda activate osgeo
    conda install -c forge --file=requirements.txt

Note this installs python 3.6.10 because there are screwy things
in Windows at python 3.8 and some libraries will not load.

