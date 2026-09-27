<p align="center">
  <img src="assets/banner.svg" alt="Dan Sambold, marine scientist and research engineer" width="100%">
</p>

<p align="center">
  <a href="https://dbold23.github.io"><img alt="Website" src="https://img.shields.io/badge/site-dbold23.github.io-0b1f33?style=for-the-badge&labelColor=2bb3a9"></a>
  <a href="https://annotate.shark-id.org"><img alt="Live app" src="https://img.shields.io/badge/live-annotate.shark--id.org-0b1f33?style=for-the-badge&labelColor=f2a93b"></a>
  <a href="https://www.linkedin.com/in/daniel-sambold-620b37221"><img alt="LinkedIn" src="https://img.shields.io/badge/LinkedIn-Daniel%20Sambold-0b1f33?style=for-the-badge&logo=linkedin&labelColor=2bb3a9"></a>
</p>

I build the software and hardware that let a small lab measure wild animals it can
rarely touch: models that read 3D shape off underwater video, radio stations that
hear tagged animals from a solar panel on a pole, and the labelling tools that turn
a semester of student attention into data a paper can stand on.

B.S. Marine Science, CSU Monterey Bay (2026). FathomNet intern at MBARI, summer 2026.
White sharks with the Ocean Predator Ecology Lab. AAUS scientific diver.

<img src="assets/wave.svg" width="100%" alt="">

## What I'm building

<table>
<tr>
<td width="50%"><a href="#shark-pose-3d"><img src="assets/card-pose3d.svg" alt="shark-pose-3d"></a></td>
<td width="50%"><a href="https://annotate.shark-id.org"><img src="assets/card-annotator.svg" alt="Shark Scar Annotator"></a></td>
</tr>
<tr>
<td><a href="#relaystation"><img src="assets/card-relay.svg" alt="RelayStation"></a></td>
<td><a href="#anchor"><img src="assets/card-anchor.svg" alt="anchor"></a></td>
</tr>
<tr>
<td><a href="#shark-pose-3d"><img src="assets/card-morpho.svg" alt="shark-morphometrics"></a></td>
<td><a href="https://github.com/dbold23/TECAN-Growth-Curve-Analysis-Pipeline"><img src="assets/card-tecan.svg" alt="TECAN growth curves"></a></td>
</tr>
</table>

Every number on these cards is copied from the project's own measured results, with the
caveats kept below. Most of this code is private while the papers are in progress;
architecture notes and public skeletons are linked as they are released.

<img src="assets/wave.svg" width="100%" alt="">

### shark-pose-3d

White sharks cannot be weighed, so body condition has to come from video. A 16-keypoint
pose detector and SAM2 silhouettes drive a fit of a rigged 3D shark model over a window
of frames, and the fit is read as a girth field along the body.

<img src="assets/flow-pose3d.svg" width="100%" alt="shark-pose-3d pipeline: detect, segment, fit, measure, ledger">

Run over the archive: 1,011 single-window records on 250 individuals. Length proportions
and girth-profile shape are quotable per animal today. Absolute girth is not yet: on a
known-truth control the fitter reads 7 to 12 % wide, and certifying it needs an external
width measurement. The 2D pose model it builds on (shark-morphometrics v4, 689 training images) scores 0.978 box mAP50 and
0.578 pose mAP50; pose is the number that is still climbing.

### Shark Scar Annotator

Twenty years of footage from four California sites, and 10 to 20 undergraduates a
semester. The platform turns that into multi-rater labels: scar boxes and types, a
16-point skeleton, a prototype 3D pin on a shark model, and consensus that treats "I looked and
there is no scar" as a vote. Live at [annotate.shark-id.org](https://annotate.shark-id.org).

<img src="assets/flow-annotator.svg" width="100%" alt="Annotation flywheel: label, track, consensus, retrain, verify">

### RelayStation

Radio tags on animals beep once every 1.7 seconds at 151 MHz. A RelayStation is a
Raspberry Pi and a software-defined radio that listens for them all day, validates the
pulse pattern, and reports over WiFi or NB-IoT cellular to a central server that also
ships its code updates. A solar variant runs standalone with an e-ink display.

<img src="assets/flow-relay.svg" width="100%" alt="RelayStation detection chain">

<img src="assets/relay-sensitivity.svg" width="100%" alt="Detector sensitivity: Welch +9 dB, STFT -9 dB, matched filter -15 dB, with fold -18 dB and -21 dB">

The rebuilt detector hears a tag about 30 dB fainter than the old one on the bench. That
is a synthetic-noise measurement; real sites have heavier tails, and the outdoor range
walk that converts it into distance has not been redone yet.

### anchor

Accelerometer tags on leopard sharks and bat rays record how an animal moved but not
where. `anchor` dead-reckons the track and pins it at the two points we do know, release
and recovery, so the uncertainty is honest in the middle. Built with Dylan Moran.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/anchor-track-dark.png">
  <img src="assets/anchor-track.png" width="100%" alt="anchor: a synthetic leopard shark track with credible bands pinned at release and recovery, depth and behaviour timelines">
</picture>

<sub>Synthetic deployment, rendered by `anchor gallery`. No tag data shown.</sub>

<img src="assets/wave.svg" width="100%" alt="">

## Also

| Project | What it is | Status |
|---|---|---|
| [TECAN Growth Curve Analysis](https://github.com/dbold23/TECAN-Growth-Curve-Analysis-Pipeline) | Plate reader to Gompertz fits with a reasoned GOOD/BAD verdict; right on 87.6 % of 960 known-answer curves | public |
| [JueLab Toolbox](https://github.com/dbold23/JueLab_Toolbox) | Shared analysis scripts for the Jue lab (CSUMB) | public |
| [camwaveheight](https://github.com/dbold23/camwaveheight) | Wave height from a pier webcam, checked against CDIP buoys | public, archived |
| PorpoiseID | Harbor porpoise re-identification from dorsal fins; 198 individuals, 30.5 % rank-1 on a held-out future year | private |
| FathomNet | MBARI summer 2026 internship on the open ocean imagery database and its tools | [fathomnet-py fork](https://github.com/dbold23/fathomnet-py) |

## Tools I reach for

<p>
  <img alt="Python" src="https://img.shields.io/badge/Python-0b1f33?style=flat-square&logo=python&logoColor=2bb3a9">
  <img alt="PyTorch" src="https://img.shields.io/badge/PyTorch-0b1f33?style=flat-square&logo=pytorch&logoColor=f2a93b">
  <img alt="OpenCV" src="https://img.shields.io/badge/OpenCV-0b1f33?style=flat-square&logo=opencv&logoColor=2bb3a9">
  <img alt="NumPy" src="https://img.shields.io/badge/NumPy-0b1f33?style=flat-square&logo=numpy&logoColor=2bb3a9">
  <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-0b1f33?style=flat-square&logo=fastapi&logoColor=2bb3a9">
  <img alt="Flask" src="https://img.shields.io/badge/Flask-0b1f33?style=flat-square&logo=flask&logoColor=f2a93b">
  <img alt="SQLite" src="https://img.shields.io/badge/SQLite-0b1f33?style=flat-square&logo=sqlite&logoColor=2bb3a9">
  <img alt="Docker" src="https://img.shields.io/badge/Docker-0b1f33?style=flat-square&logo=docker&logoColor=2bb3a9">
  <img alt="Raspberry Pi" src="https://img.shields.io/badge/Raspberry%20Pi-0b1f33?style=flat-square&logo=raspberrypi&logoColor=f2a93b">
  <img alt="Blender" src="https://img.shields.io/badge/Blender-0b1f33?style=flat-square&logo=blender&logoColor=f2a93b">
  <img alt="AWS" src="https://img.shields.io/badge/AWS%20EC2-0b1f33?style=flat-square&logo=amazonwebservices&logoColor=2bb3a9">
</p>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/dbold23/dbold23/output/snake-dark.svg">
  <img alt="Contribution graph eaten by a snake" src="https://raw.githubusercontent.com/dbold23/dbold23/output/snake.svg" width="100%">
</picture>

<sub>Artwork in this README is generated by <code>tools/build_assets.py</code>; each number in it names its source.</sub>
