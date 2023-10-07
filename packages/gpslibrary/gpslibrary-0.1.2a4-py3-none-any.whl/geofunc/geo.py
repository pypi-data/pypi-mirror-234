#!/usr/bin/python3
"""
    loc_to_geod( loc_coord )
    geod_to_loc(pos_geod )
    gdatum(datum="IGS08")
    xyzell(datum,xyzcoor): 				XYZ -> llh using the datum designed for using 
    							datum() as input
    ellecc(llh,vector,optional)
    eccell(llh,vector, swich ):			        converting a vector in xyz coord. system to local                                                        enu system in m
    xyz2enumatr(refarray,swich):			rotation matrix to convert xyz coord. system to local enu system or vice versa:w
    greatcircd(coor1,coor2):				distance along great circle
    M:
    platePoles(plate,units="ry")
    rotpole(plate,xyz,swich):
    appendSpherical_np(xyz)
"""

import pyproj as proj
from pyproj import CRS, Transformer

import numpy as np
import scipy as sp

EARTH_ERAD = 6378137.0

# itrf2008=proj.Proj("+proj=geocent +ellps=GRS80 +units=m +no_defs") # itrf2008
# lonlat=proj.Proj(init="EPSG:4326")
# isn2004=proj.Proj("+proj=lcc +lat_1=64.25 +lat_2=65.75 +lat_0=65 +lon_0=-19 +x_0=1700000 +y_0=300000 +no_defs +a=6378137 +rf=298.257222101 +to_meter=1") #isnet 2004
itrf2008 = CRS("EPSG:5332")
wgs84 = CRS("EPSG:4326")
lonlat = CRS("EPSG:4326")
isn2004 = CRS("EPSG:5322")
isn93 = CRS("EPSG:3057")

itrf08towgs84 = Transformer.from_crs(itrf2008, wgs84)
itrf08toisn04 = Transformer.from_crs(itrf2008, isn2004)
itrf08toisn03 = Transformer.from_crs(itrf2008, isn93)


### core functions for manipulating and working with vectors on earth
def loc_to_geod(loc_coord):
    """
    colat           - Colatitude (used so that loc_coord and pos_geod
                    - can be the same arrays)
    colat_trun      - Coltitude truncated to the nearest 10 asecs
                    - Used to compute small circle radius
    loc_coord(3)    - longitude (rad), latitude (rad) and
                    - height (m)
    pos_geod(3)     - Distance from equator, distance from Greenwich
                    - meridian, and height above ellipsiod (all m)

    """
    pos_geod = np.zeros(3)

    #  Distance from equator
    colat = np.pi / 2 - loc_coord[1]
    # ! 20000 = 1/10 in radians
    colat_trun = np.round(colat * 20000) / 20000

    pos_geod[0] = loc_coord[1] * EARTH_ERAD

    # Distance from Greenwich meridian along small circle
    if loc_coord[0] < 0:
        pos_geod[1] = (2 * np.pi + loc_coord[0]) * EARTH_ERAD * np.sin(colat_trun)
    else:
        pos_geod[1] = loc_coord[0] * EARTH_ERAD * np.sin(colat_trun)

    # Height above ellipssiod

    pos_geod[2] = loc_coord[2]

    return pos_geod


def geod_to_loc(pos_geod):
    """
    colat           - Colatitude (used so that loc_coord and pos_geod
                    - can be the same arrays)
    colat_trun      - Coltitude truncated to the nearest 10 asecs
                    - Used to compute small circle radius
    loc_coord(3)    - longitude (rad), latitude (rad) and
                    - height (m)
    pos_geod(3)     - Distance from equator, distance from Greenwich
                    - meridian, and height above ellipsiod (all m)
    """

    loc_coord = np.zeros(3)

    #  Get the colat and loc_coord(1)
    loc_coord[1] = pos_geod[0] / EARTH_ERAD

    colat = np.pi / 2 - loc_coord[1]
    #   ! 20000 = 1/10" in radians
    colat_trun = np.round(colat * 20000) / 20000

    # Now get longitude
    loc_coord[0] = pos_geod[1] / (EARTH_ERAD * np.sin(colat_trun))
    if loc_coord[0] > np.pi:
        loc_coord[0] = loc_coord[0] - 2 * np.pi

    # Height above ellipssiod

    loc_coord[2] = pos_geod[2]

    return loc_coord


def gdatum(datum="IGS08"):
    """
    input:
        datum
    Extracts Datum information from bernese DATUM. file
    returns major axes ($ae), minor axes ($be), scale ($sc), shift (@dx), rotation (@rx)
    """
    raise NotImplemented


def xyzell(xyzcoor, datum=itrf2008, radians=True):
    """
    x,y,z => long,lat,height
    usage: xyzell(xyzcoor,datum)
    datum: reference to datum definition
    xyzcoor: reference to a xyz coordinates
    returns reference to a list
     ( LONGITUDE, LATITUDE, HEIGHT(over ellipsoid))
    """

    return np.array(proj.transform(datum, lonlat, *xyzcoor, radians=radians))


def ellecc(llh, vector):
    """
    enu displacement -> xyz displacement
    usage: &ellecc(llh,vector,optional)
    llh: reference to coordinates in ll or llh
    vector: reference to vector array in neu coor

    returns  displacement in

    """
    raise NotImplemented


def eccell(ll, vector):
    """
    xyz displacement -> enu displacement
    Converts a list of vetctors in ECEF coordinates to the local enu coordinate system at ll

    Asumes numpy array input.

    usage:
        input
            llh: list of coordinates in ll or llh line vector (long,lat,[height]): (rad,rad,m)
            vector: A list of vector in ECEF coordinates (m)

        ouput:
            returns a list of the vectors in vectors in a local enu reference system.
    """

    if len(ll) != len(vector):
        raise ValueError

    rmat = xyz2enumatr(ll)

    if len(vector.shape) == 1:  # has to be numpy array
        vector = np.expand_dims(vector, axis=0)

    return np.squeeze(
        [np.transpose(x * y.reshape(3, 1)) for (x, y) in zip(rmat, vector)]
    )


def xyz2enumatr(ll):
    """
    calculate tranformation matrix to convert  xyz to local enu coordinates system enu or vice versa

    usage:
        input:
            ll list of lon,lat (radians) locations to compute the transformation matrix
        output:
            return list of transformation matrixes for the corresponding ll values

    """

    f = lambda x: [
        np.sin(x),
        np.cos(x),
    ]  # For calculating sin(lambda),shi(phi),cos(lambda),cos(phi)

    # Creating the rotation matrix [ [-slmb, clmb, 0], [-sphi*clmb, -sphi*slmb, cphi], [cphi*clmb, cphi*slmb, sphi]]
    # a = (slmb, sphi, clmb, cphi)
    m = lambda x: [
        np.matrix(
            [
                [-a[0], a[2], 0],
                [-a[1] * a[2], -a[1] * a[0], a[3]],
                [a[3] * a[2], a[3] * a[0], a[1]],
            ]
        )
        for a in x
    ]

    if len(ll.shape) == 1:  # In case the array is only 1 demintion
        ll = np.expand_dims(ll, axis=0)

    # calculating
    [slmb, sphi], [clmb, cphi] = f(ll[:, 0:2].transpose())

    rmat = m(zip(slmb, sphi, clmb, cphi))
    return rmat


def greatcircd(coor1, coor2, ellps="GRS80"):
    """
    Calculate the  distance along great circle between two points
    on Earths surface
    usage:  &greatcircd(coor1,coor2)
    where coor1-2 are references to two points on earths
    surface given in long,lat radiance

    """

    geod = proj.Geod(ellps=ellps)

    print(geod)


def M():
    """
    Matrix of convinience i
    """

    M = np.matrix("1, 0, 0, -1, 0, 0; 0, 1, 0, 0, -1, 0; 0, 0, 1, 0, 0, -1")
    return M


def platePoles(plate, units="ry"):
    """
    Angular velocities of tectonic plates as published in altamimi etal2012
    """
    mas2dy = 1.0 / (60 * 60) / 1000  # converting mas/Y to deg/Y

    # The plate name
    plates = {
        "EURA": 0,
        "NOAM": 1,
        "NAZC": 2,
        "INDI": 3,
        "NUBI": 4,
    }

    # ITRIF2008 Absolute Plate rotation poles From Table 3 in altamimi etal2012
    poles = np.array(
        [
            [-0.083, -0.534, 0.750],
            [0.035, -0.662, -0.100],
            [-0.330, -1.551, 1.625],
            [1.232, 0.303, 1.540],
            [0.095, -0.598, 0.723],
        ]
    )  # [mas/y]

    pole = poles[plates[plate], :]

    if units == "masy":
        return pole

    # converting to deg/Y
    pole = pole * mas2dy
    if units == "degy":
        return pole
    if units == "degMy":
        return pole * 1000000

    if units == "ry":
        return np.radians(pole)  # to radians/year


def rotpole(wxwywz, xyz, plate=None):
    """
    If plate is passed
        Calculate the nnr-nuvela velocity of a given plate in geocentric coordinates.
    If plate is not passed
        Calculate the velocity  (cross product) in a given point in ECEF coordinates with for a given rotation pole wxwywz
    """
    if plate != None:
        pass
    else:
        if xyz is not None and wxwywz is not None:
            return sp.cross(wxwywz, xyz)
        else:
            print("you need to pass a location in rad and angular velocity")


def appendSpherical_np(xyz):
    ptsnew = np.hstack((xyz, np.zeros(xyz.shape)))
    xy = xyz[:, 0] ** 2 + xyz[:, 1] ** 2
    ptsnew[:, 3] = np.sqrt(xy + xyz[:, 2] ** 2)
    ptsnew[:, 4] = np.arctan2(
        np.sqrt(xy), xyz[:, 2]
    )  # for elevation angle defined from Z-axis down
    # ptsnew[:,4] = np.arctan2(xyz[:,2], np.sqrt(xy)) # for elevation angle defined from XY-plane up
    ptsnew[:, 5] = np.arctan2(xyz[:, 1], xyz[:, 0])
    return ptsnew
