#! /usr/bin/env python
import sys
from collections import defaultdict

import ROOT as r

file_name_stem = "{m}/{d}/CLs_asymptotic_TS3_{m}_lo_RQcdFallingExpExt_fZinvTwo_55_0b-1hx2p_55_1b-1hx2p_55_2b-1hx2p_55_gt2b-1h_effHad.root"
outfile_stem  = "reweight_over_noreweight_{m}.pdf"

btags = [ "0b", "1b", "2b" , "gt2b" ]

histos = ["55_{b}_effHadSum_2D".format(b=b) for b in btags]

numDir = "reweight"
denomDir = "noreweight"

min_max = defaultdict(dict)
min_max["T2bb"] = {"gt2b": (0.,10.)}
#min_max["T2tt"] = {"gt2b": (0.,10.)}
min_max["T1"] = {
        "1b": (0.,10.),
        "2b": (0.,10.),
        "gt2b": (0.,10.),
        }
min_max["T2"] = {
        "1b": (0.,10.),
        "2b": (0.,10.),
        "gt2b": (0.,10.),
        }

def get_hist(filename, histname):
    f = r.TFile(filename)
    h = f.Get(histname).Clone()
    h.SetDirectory(0)
    f.Close()
    return h


for model in sys.argv[1:]:
    outfile = outfile_stem.format(m=model)

    c = r.TCanvas()
    c.Print(outfile+"[")
    for b,hist in zip(btags,histos):
        d_file_name = file_name_stem.format(m=model,d=denomDir)
        n_file_name = file_name_stem.format(m=model,d=numDir)
        min,max = min_max[model].get(b,(0.5,1.5))
        h1d = r.TH1D(hist,model+" "+b+";Reweighted/Unreweighted;Count",100,min,max)
        nHist = get_hist(n_file_name, hist)
        dHist = get_hist(d_file_name, hist)


        nHist.Divide(dHist)
        nHist.Draw("colz")
        for ibinx in range(1,1+nHist.GetNbinsX()):
            for ibiny in range(1,1+nHist.GetNbinsY()):
                content = nHist.GetBinContent(ibinx,ibiny)
                if content:
                    h1d.Fill(content)

        h1d.Draw()
        c.Print(outfile)
    c.Print(outfile+"]")
