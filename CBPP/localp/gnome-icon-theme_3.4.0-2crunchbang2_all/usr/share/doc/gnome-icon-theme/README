The age of hackers supplying their own artwork is over. For the sake of our
users, please leave the pixelpushin' to the artists. Please file a request
instead.

Bugs and Requests
-----------------

Requests for icons that will be useful for more than a a single application and
it makes sense to share it in an icon theme should be filed in GNOME bugzilla
(bugzilla.gnome.org) under the gnome-icon-theme module.


High resolution icons
=====================

Application launcher icons and filetype icons in general will benefit in
providing a high resolution variant. For Tango, the canvas size is 256x256 pixels.

We suggest creating artwork for this large canvas as vectors. It may require
more time as vector art with filter effects tends to be very computentionally
intensive, but the benefit is that it allows to create derivative works easily.
In addition, if we need a higher resolution than 256x256 in future, it's simply
a matter of re-rendering the icons.

Due to the large canvas a lot of the guidelines discussed elsewhere in this document do not apply. What still stands is the use of colors, the perspective and lighting. 

FIXME: outlines (strokes alternative - wip)
FIXME: highlights (inner stroke alternative)
FIXME: shadows (wip)

Inkscape workflow tips:
-----------------------

* The 256x256 icon needs to be nice when scaled down to 64x64 (25% zoom), so, in inkscape, it's necessary to use a 1x1 pixels grid with major lines every 4. Lining up the main objects to the major lines of the grid will help making the icon less blurry when scaled down.

* Text: the best trick we found (atm) for text in high resolution icons is to use the text tool to write something (lorem ipsum, funny things, nonsenses and so on:-)) using the Bitstream Vera Sans typeface with a 6pt size, trying to have the main bodies of the letters between two horizontal major grid lines, then we convert the text object to path and simplify (ctrl+l) 3 times. In case the text is not visible enough when scaling down overlaying the line with a very subtle rectangle 4px tall will help (see text-x-generic).

* Outlines: to make the things stand out we darken the edges using various tecniques. Lapo's favourite is to group the all objects costituting the shape; copy, paste in place, ungroup and make the boolean union to obtain the silouhette  [ctrl+c, crtl+alt+v, ctrl+u, ctrl++]; copy again; set this path fill to none, set the stroke from 0.5 to 2 pixels in a dark color (usaully black) and set blur from 1 to 2 points; group it with the previous group; paste in place and select the new group and the pasted path apply a clipping mask (the pasted path will be used as a clipping mask) [Object -> Clip -> Set]. Now you can do group editing with the clipping mask in place [ctrl+enter to "enter" the group]. You can play with various stroke width and color or gradients and with different blur settings.

* Shadows: there's usually two shadow objects, one darker, less blurred, less offset. The other very fuzzy, very transparent. So you get a nice soft, non-linear falloff.
