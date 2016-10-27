# include utility functions
import os
import sys
import ROOT

def Fun_deltaR(eta1,eta2,phi1,phi2):
    result = ((eta1-eta2)**2+(phi1-phi2)**2)**0.5
    return result
