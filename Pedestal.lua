pcall(load(S4.arg))

local filedata = io.open("data.csv","w")
local fileeps = io.open("eps.csv", "w")

S = S4.NewSimulation()
S:SetLattice(period)
S:SetNumG(nharm)
S:UsePolarizationDecomposition()

S:AddMaterial("GratingMaterial", {gratingindex^2, 0})
S:AddMaterial("Air", {1.33^2,0})
S:AddMaterial("Glass", {subindex^2,0})

S:AddLayer('AirAbove', 0, 'Air')
S:AddLayer('Grating', gratingthickness, 'Air') -- Air inbetween
S:SetLayerPatternRectangle('Grating', 'GratingMaterial', {0,0}, 0, {ridgewidth*0.5,0})
S:AddLayer('Grating1', pedestal_thickness, 'GratingMaterial') 
S:AddLayer('GlassSubstrate', 0, 'Glass')

S:SetExcitationPlanewave({0,0},   -- incidence angles (spherical coords: theta [0,360], phi [0,180], )
                        {TEamp,0},  -- TE-polarisation amplitude and phase (in degrees)
                        {TMamp,0})  -- TM-polarisation amplitude and phase

-- COMPUTE AND SAVE TRANSMISSION / REFLECTION
filedata:write("Lambda,Spectrum,Eyr,Eyi")
reflection_max = 0

for lambda = lambdain, lambdafin, deltalambda do
  freq = 1/lambda
  S:SetFrequency(freq)
  inc, back = S:GetPowerFlux('AirAbove', 20)
  forward, backward = S:GetPowerFlux('GlassSubstrate', 20)
  refl = - back/inc

  filedata:write("\n", lambda, ",", refl)
              
  if refl > reflection_max then 
    reflection_max = refl
      lambda_max = lambda
  end 
          
end 

print('lambda_max=', lambda_max)