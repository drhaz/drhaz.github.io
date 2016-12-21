---
layout: post
title: "Suppressing pupil ghost and other internal reflections in the WIYN One Degree Imager"
date: 2016-12-21
comments: true

---

Formation of a pupil ghost in ODI images
===

Reflections of the optical surfaces within [WIYN One Degree Imager (ODI)](http://www.wiyn.org/ODI/index.html) produce internal ghosting, i.e., flat fields[^1] or exposures of the night sky will produce an image of the telescope pupil. Thanks to anti-reflection coatings on the optics, each reflection is suppressed to about about 1%-2% level, depending on the actual wavelength of the light, but the residual light is still capable of producing a significant ghosting component. ODI's dewar window is concave, and paired with the plane surface of the passband filter forms an imaging system that produces a focussed image of the telescope pupil on the focal plane (see Fig. 1, left, for the ghost image formation; see Fig. 2 for an example of an actual raw flat field imae of ODI affected by a pupil ghost image). 


![ODI pupil ghost formation and supression cartoon]({{Site.url}}/assets/images/2016/odishutterpupilghostsupression.png){: .center-image}
Fig. 1 - *Formation of the pupil ghost in ODI: a light component entering the instrument from the telescope (from the right) reflects of the concave dewar window, and the converging beam reflects of the filter and will create an in-focus iamge of the telescope pupil.*


![Example of ODI pupil ghost]({{Site.url}}/assets/images/2016/odi_pupilghost_layerII.png){: .center-image}
Fig. 2 - *Example of a flat field iamge taken with ODI in the UV.One can see the different sensitivities of small square iamge units (cells). Near the center is a donut-like structure that is an image of the telescope pupil. This additional pupil image is undesirable in a calibration image.*

The excess light of the pupil ghost is undesirable for several reasons: In night-sky observations it will produce an extra background component, but it can be subtracted out. More severely, the pupil ghost also produces an extra light component in a calibrating flat field, and if not treated, would lead to a wrong sensitivity calibration in the affected areas. 

The first method of choice to remove the pupil ghost out of calibration images was to model the ghost image and to then subtract it out of the flat field images. This approach was overall successful, but is is prone to adding noise and residual errors from fitting a template to data. 


Suppression of the pupil ghost using the shutter
===

The pupil ghost was found to be greatly suppressed by the ODI shutter[^2] when the exposure is tuned in a way where the shutter blades mostly obstruct the optical path in front of the dewar window, and expose only via a narrow slit that moves slowly over the focal plane. This suppression mechanism is illustrated by Fig. 1 (right). Note that, despite the shutter forming only a narrow slit, the direct illumination of the focal plane is identical to a flat field where the shutter completely opens.

This ghost-suppressing behavior of the shutter has been exploited already by using very short exposure times of order of 50ms for sky flat fields, and this new method has replaced the pupil ghost model subtraction method over the last half year. However, this method was applicable only for situations with a very bright flat field illumination that would support extremely short exposure times. By lowering the travel speed of the shutter blades, however, one can achieve the same ghost suppressing property at longer exposure times. The cost, however, is that each flat field will take about 27 seconds longer, as this is the travel time of the blades (the travel time at default speed is about 0.75 seconds). 

A good demonstration of the pupil ghost supression by the shutter is to divide a flat field where the shutter is operated conventionally by a flat field where the shutter was operated in the narrow-slit mode. Other than in the raw image of a flat field as in Fig. 1, the sensitivity variations between pixels and detectors should dive out. Only the extra stray light component should remain visible in the image. And voilà, Fig. 3 shows a well-defined ghosting component, demonstrating that we can now generate calibration flat fields that are free of internal reflections. 

![ODI Layer I pupil ghost]({{Site.url}}/assets/images/2016/odi_layeronepg.png){: .center-image}
Fig. 3 - *Ratio of a flat field taken with different shutter modes. The sensitivity variations between pixels and detectors cancel out, but the excess ghosting light remains. Note that this ratio shows the ghosting component created by filters that are at a different location than in Fig. 1, and the pupil ghost is largely out of focus.*


Footnotes:
===

[^1]: A flat field is an exposure of a homogeneously illuminated surface. In an ideal imaging system, that homogeneous surface will produce a flat  (hence the name "flat field") image without any structure. However, the image will not be perfectly flat in practice, as there are always some variations in sensitivity from pixel to pixel, from detector to detector, and variations in the throughput of the optical system (e.g., vignetting). By dividing a science image by a (normalized) flat field image, one can correct for such sensitivity variations.

[^2]: The shutter used in ODI is a [Bonn Shutter](http://www.bonn-shutter.de/). It has two blades that open and close in tandem, very much as a slit shutter in a SLR camera. However, the Bonn Shutter comes in much larger sizes than your average consumer camera.
