#HEADS UP
Keep in mind, as the distro is currently based off of the Debian netinst, an internet connection will be required.
This is in no way a finished product. The Beta is currently more of a proof-of-concept than a full fledged release. As such, some breakage may arise through normal use. Regardless, experienced users and those familiar with the issues between Jessie and the #! metapackage will likely be familiar with the issues and should have no problem using this as a daily driver.
While we don't forsee any serious issues at this time, INSTALL AT YOUR OWN RISK. We are not responsible for any loss of data or otherwise unexpected consequences. VMs would be the safest choice until we can test further.

##INSTALL
The simplest way to get the Beta up and running would simply be to download via torrent.

##BUILDING
However, if you intend to build from our source, here are the steps:
(We recommend using a Jessie-based Debian distro for building)

1. apt-get install simple-cdd
2. Download our source and extract the .zip
   --Note, the packages are no longer located on this github repo. However, the torrent distributed from crunchbangplusplus.org includes the source .debs that were used for that iso.
3. cd into CBPP_beta_02132015_src/
4. ./build.sh to start the build process with our configuration

And of course, while you're here, have a stroll through the packages, configs, and scripts! Feel free to fork the project and send up any changes if you find any way to improve the project. There's a lot of work to do, and Linux is all about sharing ;)

##PROBLEMS BUILDING?
Here's a few fixes for snags we've come across:
  
  Missing Package Errors - 
	rm -r tmp/ images/
	(clears out any previous build information)

	apt-get clean
	(in the case any cached packages are the source of the issue)
	
  GPG Signature Failure -
	This just seems to happen every now and again. The Debian Repo seems to resign every 2hrs. or so, hang in there. (Or if you know how to take care of it, let us know!)
