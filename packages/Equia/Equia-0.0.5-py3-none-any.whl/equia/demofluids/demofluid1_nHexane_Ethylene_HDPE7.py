from equia.models import ApiFluid, ApiFluidStandardComponent,ApiFluidPolymerComponent,ApiFluidComponentBlock,ApiFluidPseudoComponent, ApiFluidKij

def demofluid1_nHexane_Ethylene_HDPE7() -> ApiFluid:
    '''Predefined fluid with 2 solvents and a HDPE polymer with 7 pseudo components'''   
    fluid = ApiFluid()
    fluid.name = "n-Hexane + Ethylene + HDPE(7)"
    fluid.eos = "PC-SAFT"
    fluid.solvent_cp = "DIPPR"
    fluid.polymer_cp = "Polynomial"

    fluid.standards = [
      ApiFluidStandardComponent(name="n-Hexane",is_alkane=True, molar_mass=86.17536,         
        acentric_factor = 0.301261,
        critical_pressure = 30.25,
        critical_temperature = 507.6,
        pc_saftdm = 0.03548,
        pc_saft_sigma_0 = 3.7983,
        pc_saft_epsilon = 236.77),
      ApiFluidStandardComponent(name="Ethylene", is_alkane=True, molar_mass=28.05316,         
        acentric_factor = 0.087,
        critical_pressure = 50.41,
        critical_temperature = 282.34,
        pc_saftdm = 0.0567914,
        pc_saft_sigma_0 = 3.445,
        pc_saft_epsilon = 176.47),
      ]

    fluid.polymers = [
        ApiFluidPolymerComponent(short_name="HDPE",
          blocks=[
            ApiFluidComponentBlock(block_massfraction=1, monomer_name="Ethylene", monomer_molar_mass=28.054, pc_saftdm = 0.0263, pc_saft_sigma_0 = 4.0217, pc_saft_epsilon = 252.0,
                                   sle_c=0.4, sle_hu=8220.0, sle_density_amorphous=0.853, sle_density_crystalline=1.004)
                                 ],
          pseudo_components=[
            ApiFluidPseudoComponent(name= "HDPE(17.3)", melting_temperature = 415.82, molar_mass = 17300,  massfraction = 0.00498),
            ApiFluidPseudoComponent(name= "HDPE(25.6)", melting_temperature = 416.38, molar_mass = 25600,  massfraction = 0.03067),
            ApiFluidPseudoComponent(name= "HDPE(36)",   melting_temperature = 416.72, molar_mass = 36000,  massfraction = 0.23902),
            ApiFluidPseudoComponent(name= "HDPE(50)",   melting_temperature = 416.95, molar_mass = 50000,  massfraction = 0.45515),
            ApiFluidPseudoComponent(name= "HDPE(69.2)", melting_temperature = 417.12, molar_mass = 69200,  massfraction = 0.23902),
            ApiFluidPseudoComponent(name= "HDPE(97.6)", melting_temperature = 417.24, molar_mass = 97600,  massfraction = 0.03067),
            ApiFluidPseudoComponent(name= "HDPE(144)",  melting_temperature = 417.34, molar_mass = 144000, massfraction = 0.0005)                                 ]                            
        )
      ]
    
    fluid.kij = [
      ApiFluidKij(index_i=0, index_j=1, kija=0.0001),
      ApiFluidKij(index_i=0, index_j=2, kija=0.0002),
      ApiFluidKij(index_i=1, index_j=2, kija=0.0003),
      ]

    return fluid
