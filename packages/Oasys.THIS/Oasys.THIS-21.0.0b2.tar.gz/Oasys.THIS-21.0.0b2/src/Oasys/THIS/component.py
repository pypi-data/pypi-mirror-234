import Oasys.gRPC


# Metaclass for static properties and constants
class ComponentType(type):
    _consts = {'A', 'AA', 'AC', 'ADT', 'AFM', 'AFX', 'AFY', 'AFZ', 'AIE', 'ALD', 'ALS', 'ALT', 'AM', 'AME', 'APR', 'AR', 'ARS', 'ATE', 'AVM', 'AVX', 'AVY', 'AVZ', 'AX', 'AY', 'AZ', 'BA', 'BACE', 'BDDX', 'BDDY', 'BDDZ', 'BDMA', 'BDMS', 'BDMT', 'BDNA', 'BDNS', 'BDNT', 'BDSX', 'BDSY', 'BDSZ', 'BDT', 'BDTX', 'BDTY', 'BDTZ', 'BDX', 'BDY', 'BDZ', 'BEAX', 'BED', 'BEP', 'BES', 'BET', 'BEX', 'BFDM', 'BFDX', 'BFDY', 'BFDZ', 'BFX', 'BFY', 'BFZ', 'BIE', 'BMXX', 'BMY1', 'BMY2', 'BMYY', 'BMZ1', 'BMZ2', 'BMZZ', 'BPE1', 'BPE2', 'BRXX', 'BRY', 'BRY1', 'BRY2', 'BRZ', 'BRZ1', 'BRZ2', 'BSAX', 'BSXX', 'BSXY', 'BSZX', 'BV', 'BX', 'BY', 'BZ', 'C10', 'C20', 'C30', 'CENM', 'CENS', 'CFL', 'CFM', 'CFMS', 'CFRI', 'CFX', 'CFXS', 'CFY', 'CFYS', 'CFZ', 'CFZS', 'CMM', 'CMS', 'CMX', 'CMXS', 'CMY', 'CMYS', 'CMZ', 'CMZS', 'CNM', 'COUT', 'CTEN', 'CV', 'CX', 'CY', 'CZ', 'D11', 'D12', 'D13', 'D21', 'D22', 'D23', 'D31', 'D32', 'D33', 'DE', 'DFP', 'DFR', 'DFX', 'DFY', 'DFZ', 'DM', 'DMP', 'DP', 'DPDT', 'DPFX', 'DPFY', 'DPFZ', 'DPIE', 'DPPR', 'DPTE', 'DR', 'DRCE', 'DRCO', 'DRDT', 'DRKE', 'DRMX', 'DVO', 'DX', 'DXDT', 'DY', 'DYDT', 'DZ', 'DZDT', 'EAV', 'EBA', 'EBC', 'EBV', 'ECC', 'ECCE', 'ECCT', 'ECDC', 'ECDE', 'ECDT', 'ECDV', 'ECE', 'ECI', 'ECJH', 'ECM', 'ECM1', 'ECM2', 'ECM3', 'ECME', 'ECP', 'ECRA', 'ECRC', 'ECRD', 'ECRJ', 'ECRR', 'ECT', 'ECV', 'ECX', 'ECY', 'ECZ', 'EDEN', 'EFM', 'EFS', 'EFX', 'EFY', 'EFZ', 'EICT', 'EIV', 'EMAX', 'EMIN', 'EMS', 'EN', 'ENE', 'EPL', 'EPS', 'ERD', 'ERSC', 'ERVC', 'ERVM', 'ERXX', 'ERXY', 'ERYY', 'ERYZ', 'ERZX', 'ERZZ', 'ESE', 'EV', 'EVON', 'EXX', 'EXY', 'EYY', 'EYZ', 'EZX', 'EZZ', 'FM', 'FN', 'FPM', 'FPX', 'FPY', 'FPZ', 'FR', 'FVM', 'FVX', 'FVY', 'FVZ', 'FX', 'FY', 'FZ', 'GA', 'GAM', 'GAS', 'GCM', 'GDE', 'GDIE', 'GDKE', 'GDT', 'GEHG', 'GEIE', 'GEKE', 'GEN', 'GER', 'GEW', 'GHG', 'GI1', 'GI11', 'GI12', 'GI13', 'GI2', 'GI21', 'GI22', 'GI23', 'GI3', 'GI31', 'GI32', 'GI33', 'GIE', 'GIR', 'GJE', 'GKE', 'GKR', 'GMADD', 'GMASS', 'GMDE', 'GMEE', 'GMPE', 'GMX', 'GMY', 'GMZ', 'GP11', 'GP12', 'GP13', 'GP21', 'GP22', 'GP23', 'GP31', 'GP32', 'GP33', 'GPM', 'GRBE', 'GRFM', 'GRFX', 'GRFY', 'GRFZ', 'GSDE', 'GSF', 'GSIE', 'GSPE', 'GSTP', 'GSWE', 'GTE', 'GTER', 'GTZC', 'GVX', 'GVY', 'GVZ', 'GXCM', 'GYCM', 'GZCM', 'HCE', 'HTC', 'IE', 'IFE', 'IN', 'JHR', 'LAX', 'LAY', 'LAZ', 'LDX', 'LDY', 'LDZ', 'LE', 'LFM', 'LFX', 'LFY', 'LFZ', 'LK', 'LKE', 'LMX', 'LMY', 'LMZ', 'LOFM', 'LOFX', 'LOFY', 'LOFZ', 'LRAX', 'LRAY', 'LRAZ', 'LRDX', 'LRDY', 'LRDZ', 'LRVX', 'LRVY', 'LRVZ', 'LS', 'LVX', 'LVY', 'LVZ', 'MAF', 'MASS', 'MAV', 'MIN', 'MJH', 'ML', 'MM', 'MME', 'MOF', 'MOU', 'MOV', 'MP', 'MPM', 'MPX', 'MPY', 'MPZ', 'MSR', 'MUR', 'MVM', 'MVX', 'MVY', 'MVZ', 'MX', 'MXR', 'MY', 'MZ', 'NP', 'NSC', 'OCV', 'OHE', 'OHP', 'OIE', 'OTE', 'OU', 'PA', 'PEMAG', 'PHA', 'PHD', 'PHDT', 'PHS', 'PHT', 'PJHE', 'PKIN', 'PLFM', 'PLFX', 'PLFY', 'PLFZ', 'PL_AN', 'PL_FT', 'PL_SL', 'PL_SR', 'PMAG', 'POW', 'PP', 'PPLA', 'PR', 'PRN', 'PRP', 'PR_FI', 'PSA', 'PSD', 'PSDT', 'PSS', 'PST', 'PTE', 'PVO', 'QC', 'R10', 'R20', 'R30', 'RAM', 'RAX', 'RAY', 'RAZ', 'RBC', 'RCT', 'RDM', 'RDX', 'RDY', 'RDZ', 'RFM', 'RFX', 'RFXY', 'RFY', 'RFZ', 'RHE', 'RHP', 'RMX', 'RMXY', 'RMY', 'RPR', 'RQX', 'RQY', 'RR0', 'RT_F', 'RT_FP', 'RT_P', 'RUN', 'RV', 'RVM', 'RVX', 'RVY', 'RVZ', 'S', 'SA', 'SAV', 'SB_F', 'SB_FS', 'SB_L', 'SB_S', 'SFP', 'SFR', 'SFX', 'SFY', 'SFZ', 'SHC', 'SHX', 'SM', 'SMAX', 'SMIN', 'SMS', 'SO', 'SOC', 'SOF', 'SOM', 'SOS', 'SOX', 'SPC_FM', 'SPC_FX', 'SPC_FY', 'SPC_FZ', 'SPC_MM', 'SPC_MX', 'SPC_MY', 'SPC_MZ', 'SPC_RF', 'SPC_RMF', 'SPC_XMF', 'SPC_XTF', 'SPC_YMF', 'SPC_YTF', 'SPC_ZMF', 'SPC_ZTF', 'SP_E', 'SP_EN', 'SP_F', 'SP_FE', 'SP_FX', 'SP_FY', 'SP_FZ', 'SP_M', 'SP_MR', 'SP_MX', 'SP_MY', 'SP_MZ', 'SP_R', 'SR_B1', 'SR_B2', 'SR_F', 'SR_N', 'SR_P', 'SR_S', 'SR_W', 'STR', 'SVON', 'SW_AREA', 'SW_BF', 'SW_F', 'SW_FAIL', 'SW_FF', 'SW_LE', 'SW_MF', 'SW_MM', 'SW_NF', 'SW_S', 'SW_SF', 'SW_TIME', 'SW_TO', 'SXX', 'SXY', 'SYY', 'SYZ', 'SZX', 'SZZ', 'TAA', 'TBOT', 'TC', 'TEE', 'TEH', 'TEM', 'TEMP', 'TFM', 'TFP', 'TFR', 'TFX', 'TFY', 'TFZ', 'THA', 'THD', 'THDT', 'THK', 'THS', 'THT', 'TKE', 'TNC', 'TOC', 'TOR', 'TPE', 'TRE', 'TSA', 'TSR', 'TTOP', 'TVO', 'UN', 'VC', 'VC2', 'VC3', 'VEL', 'VM', 'VOL', 'VT', 'VTM', 'VTX', 'VTY', 'VTZ', 'VX', 'VY', 'VZ', 'X', 'XSEC_A', 'XSEC_CX', 'XSEC_CY', 'XSEC_CZ', 'XSEC_FM', 'XSEC_FX', 'XSEC_FY', 'XSEC_FZ', 'XSEC_MM', 'XSEC_MX', 'XSEC_MY', 'XSEC_MZ', 'Y', 'Z'}

    def __getattr__(cls, name):
        if name in ComponentType._consts:
            return Oasys.THIS._connection.classGetter(cls.__name__, name)

        raise AttributeError


class Component(Oasys.gRPC.OasysItem, metaclass=ComponentType):


    def __del__(self):
        if not Oasys.THIS._connection:
            return

        Oasys.THIS._connection.destructor(self.__class__.__name__, self._handle)


    def __getattr__(self, name):
        raise AttributeError


    def __setattr__(self, name, value):
# Set the property locally
        self.__dict__[name] = value
