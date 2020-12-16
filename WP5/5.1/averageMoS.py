import FunctionsBucklingAnalysis as FBA

consideredLengthHalfWingSpan = FBA.wingSpan /2 * 0.9


resolution = 100

for i in range(0, consideredLengthHalfWingSpan *resolution):
    frontWebMoS = FBA.Web_Margin_of_Safety_List_Front
    rearWebMoS = FBA.