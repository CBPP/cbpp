## cbpp
# #!++, A CrunchBang revival project.

NEW: It's becoming increasingly clear that the packages should be split into their own separate repos. Starting with cb-configs (now cbpp-configs), I'm going to start moving packages out into CBPP/(wheretheybelong). This will streamline the repos and make them easier to keep track of. I'm also changing the way I build the packages, so you'll be able to directly download individual repos, run a single command, and get the .deb out of it for testing. As it stands now, we're looking at the package contents extracted from the .deb files. With the new repos, we'll be looking at them _before_ the build.

Philip Newborough -- Corenominal -- has officially discontinued his efforts with the fast and light distro. While Philip believes that the project no longer serves the Linux space in the way he had originally intended, we believe that #! still has great potential and serves the Linux community as the perfect combination of elegance and efficiency.

So far, we're still only just finishing our 'Jessie-proofing' of the #! metapackage. While we intend to keep the distro very much the same as it has been over the years, some changes must be made to adapt to newer dependencies. Most notably, #!++ will have a new gtk theme (by xoraxiom) and a new default iconset using the faenza-crunchbang-icon-theme package from the #! repo.

A few more changes have been made under the hood, but stay tuned to our website at crunchbangplusplus.org for further updates. We look forward to bringing further fixes and enhancements to the project and documenting our methods and progress along the way.

Lastly, we'd like to thank Philip for all his hard work through the years, the legacy he's created, and the bar he's set for sleek high-performance distros.
