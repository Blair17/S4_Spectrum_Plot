pcall(load(S4.arg))

local filedata = io.open("data.csv","w")
local fileeps = io.open("eps.csv", "w")

S = S4.NewSimulation()
S:SetLattice(period)
S:SetNumG(nharm)
S:UsePolarizationDecomposition()

S:AddMaterial("GratingMaterial", {gratingindex^2, loss^2})
S:AddMaterial("Cover", {coverindex^2,0})
S:AddMaterial("Glass", {glassindex^2,0})
S:AddMaterial("Alox", {aloxindex^2,0})

S:AddLayer('cover_region', 0, 'Cover') 
S:AddLayer('Grating', gratingthickness, 'Cover')
S:SetLayerPatternRectangle('Grating', 'GratingMaterial', {0,0}, 0, {ridgewidth*0.5,0})
S:AddLayer('Grating1', residual_layer_thickness, 'GratingMaterial')
S:AddLayer('Substrate', 0, 'Glass')

S:SetExcitationPlanewave({0,0},   -- incidence angles (spherical coords: theta [0,360], phi [0,180])
                        {TEamp,0},  -- TE-polarisation amplitude and phase (in degrees)
                        {TMamp,0})  -- TM-polarisation amplitude and phase

-- COMPUTE AND SAVE TRANSMISSION / REFLECTION
filedata:write("Lambda,Spectrum,Eyr,Eyi")
reflection_max = 0

for lambda = lambdain, lambdafin, deltalambda do
  freq = 1/lambda
  S:SetFrequency(freq)
  inc, back = S:GetPowerFlux('cover_region', 20)
  forward, backward = S:GetPowerFlux('Substrate', 20)
  refl = - back/inc
  inc,back = S:GetAmplitudes('Grating',0)
  filedata:write("\n", lambda, ",", refl, ",", back[1][1], ",", back[1][2])
              
  if refl > reflection_max then 
    reflection_max = refl
      lambda_max = lambda
  end 
end 

for x = -period/2, period/2, 2 do
  eps_r, eps_i = S:GetEpsilon({x, 0, 75})
  fileeps:write(x..','..eps_r..'\n')
end

print('lambda_max=', lambda_max)