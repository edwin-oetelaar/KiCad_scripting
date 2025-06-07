# Edwin
# Try of KICAD footprint wizard for terminal block
# june 7 2025 updated
# MIT license

from __future__ import division
import sys
import os

import pcbnew
import FootprintWizardBase as FPWbase
import PadArray as PA


class PadStaggeredZGridArray(PA.PadArray):
    """Pad array arranged in staggered rows in Z pattern."""

    def __init__(self, aPad, aPadCount, aLineCount, aLinePitch,
                 aPadPitch, aStagger=0, aCentre=pcbnew.VECTOR2I(0, 0)):
        """Initialize pad array.
        
        Args:
            aPad: Template for all pads
            aPadCount: Overall pad count 
            aLineCount: Number of lines
            aLinePitch: Distance between lines
            aPadPitch: Distance between pads
            aStagger: X stagger value for odd lines
            aCentre: Center position
        """
        super(PadStaggeredZGridArray, self).__init__(aPad)
        self.padCount = int(aPadCount)
        self.lineCount = int(aLineCount)
        self.linePitch = aLinePitch
        self.padPitch = aPadPitch
        self.stagger = aStagger
        self.centre = aCentre

    def NamingFunction(self, aPadPos):
        """Right to left, top to bottom pad naming."""
        return self.firstPadNum + aPadPos

    def AddPadsToModule(self, dc):
        """Add pads to module at calculated positions."""
        pin1posX = (self.centre.x - ((self.padPitch * (self.padCount // 2 - 1)) +
                                     self.stagger) / 2)
        pin1posY = self.centre.y - self.linePitch * (self.lineCount - 1) / 2

        line = 0
        for padnum in range(self.padCount):
            if (line % 2) == 0:
                posX = pin1posX + ((padnum // 2) * self.padPitch)
            else:
                posX = pin1posX + self.stagger + ((padnum // 2) * self.padPitch)

            posY = pin1posY + (self.linePitch * line)
            pos = dc.TransformPoint(posX, posY)
            pad = self.GetPad(padnum == 0, pos)
            pad.SetName(1 + int(padnum // 2))
            self.AddPad(pad)

            line += 1
            if line >= self.lineCount:
                line = 0


class KF141RWizard(FPWbase.FootprintWizard):
    """
    Footprint wizard for PCB terminal blocks.

    Generates footprints for Cixi Kefa Elec KF141R-2.54 or Phoenix Contact 
    MFFKDSA1/H-2,54 series terminal blocks. Customizable parameters include
    pad configuration, row spacing, and silkscreen details.
    """

    padCountKey = "pad count"
    rowSpacingKey = "row spacing"
    padLengthKey = "pad length"
    padWidthKey = "pad width"
    padPitchKey = "pad pitch"
    staggerOffsetKey = "stagger_offset"
    withFlag = 'SimpleFlag'
    row_count_key = "row count"
    row_spacing_key = "row spacing"
    pad_length_key = "pad length"
    pad_width_key = "pad width"
    pad_pitch_key = "pad pitch"
    pad_drill_key = "drill size"
    silkscreen_inside_key = "silk screen inside"
    outline_x_margin_key = "outline x margin"
    outline_y_margin_key = "outline y margin"

    def GetName(self):
        return "KF141R-2.54"

    def GetDescription(self):
        return ("PCB terminal block Cixi Kefa Elec KF141R-2.54 or Phoenix Contact "
                "MFFKDSA1/H-2,54, footprint wizard")

    def GenerateParameterList(self):
        """Set default parameters for the footprint."""
        self.AddParam("Body", self.withFlag, self.uBool, True)
        self.AddParam("Pads", self.padCountKey, self.uInteger, 8, multiple=2)
        self.AddParam("Pads", self.padWidthKey, self.uMM, 1.5)
        self.AddParam("Pads", self.padLengthKey, self.uMM, 3.0)
        self.AddParam("Pads", self.padPitchKey, self.uMM, 2.54)
        self.AddParam("Pads", self.rowSpacingKey, self.uMM, 5.08)
        self.AddParam("Pads", self.staggerOffsetKey, self.uMM, 0.0)
        self.AddParam("Pads", self.pad_drill_key, self.uMM, 0.9)

    def CheckParameters(self):
        pass

    def GetValue(self):
        pad_count = self.parameters["Pads"][self.padCountKey]
        return f"KF141R-2.54-{pad_count // 2}"

    def GetPad(self):
        """Create pad with specified parameters."""
        pad_length = self.parameters["Pads"][self.pad_length_key]
        pad_width = self.parameters["Pads"][self.pad_width_key]
        drill = self.parameters["Pads"][self.pad_drill_key]

        shape = pcbnew.PAD_SHAPE_CIRCLE
        if pad_length != pad_width:
            shape = pcbnew.PAD_SHAPE_OVAL

        return PA.PadMaker(self.module).THPad(pad_length, pad_width, drill, shape=shape)

    def BuildThisFootprint(self):
        """Build the complete footprint."""
        # Get parameters
        pads = self.parameters["Pads"]
        body = self.parameters["Body"]
        numPads = pads[self.padCountKey]
        padLength = pads[self.padLengthKey]
        rowPitch = pads[self.rowSpacingKey]
        padPitch = pads[self.padPitchKey]
        staggerOffset = pads[self.staggerOffsetKey]
        numRows = 2

        # Set footprint properties
        self.module.SetLibDescription(self.GetValue())
        self.module.SetAttributes(pcbnew.FP_THROUGH_HOLE)

        # Add pad array
        array = PadStaggeredZGridArray(
            self.GetPad(), numPads, numRows, rowPitch, padPitch, staggerOffset
        )
        array.AddPadsToModule(self.draw)

        # Draw outline
        width = pcbnew.FromMM(2.54) + (padPitch * (numPads // 2))
        height = (rowPitch * (numRows - 1)) + pcbnew.FromMM(8.52)
        self.draw.SetLineThickness(pcbnew.FromMM(0.12))

        xoffset = pcbnew.FromMM(2.54 - 0.95)
        yoffset = pcbnew.FromMM((13.6 / 2.0) - 5.5)

        self.draw.Box(x=xoffset, y=yoffset, w=width, h=height)

        # Add vertical lines
        topx = xoffset - (width / 2.0)
        topy = yoffset - (height / 2.0)

        for i in range(numPads // 2):
            x1 = topx + ((i + 1) * padPitch)
            y1 = topy
            y2 = y1 + height
            self.draw.Line(x1=x1, y1=y1, x2=x1, y2=y2)

        # Draw courtyard
        self.draw.SetLayer(pcbnew.F_CrtYd)
        self.draw.SetLineThickness(pcbnew.FromMM(0.05))

        boxW = width + pcbnew.FromMM(0.5)
        boxH = height + pcbnew.FromMM(0.5)

        pcbnew.PutOnGridMM(boxW, pcbnew.FromMM(0.10))
        pcbnew.PutOnGridMM(boxH, pcbnew.FromMM(0.10))

        self.draw.Box(x=xoffset, y=yoffset, w=boxW, h=boxH)

        # Add text
        text_size = pcbnew.FromMM(1.0)
        text_offset = height / 2 + text_size

        self.draw.Value(0, text_offset, text_size)
        self.draw.Reference(0, -text_offset, text_size)

        # Add reference on fab layer
        extra_text = pcbnew.PCB_TEXT(self.module)
        extra_text.SetLayer(pcbnew.F_Fab)
        extra_text.SetPosition(pcbnew.VECTOR2I(0, 0))
        extra_text.SetTextSize(pcbnew.VECTOR2I(text_size, text_size))
        extra_text.SetText("${REFERENCE}")
        self.module.Add(extra_text)


KF141RWizard().register()
