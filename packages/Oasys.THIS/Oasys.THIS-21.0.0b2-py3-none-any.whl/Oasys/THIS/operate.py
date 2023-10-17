import Oasys.gRPC


# Metaclass for static properties and constants
class OperateType(type):

    def __getattr__(cls, name):

        raise AttributeError


class Operate(Oasys.gRPC.OasysItem, metaclass=OperateType):


    def __del__(self):
        if not Oasys.THIS._connection:
            return

        Oasys.THIS._connection.destructor(self.__class__.__name__, self._handle)


    def __getattr__(self, name):
        raise AttributeError


    def __setattr__(self, name, value):
# Set the property locally
        self.__dict__[name] = value


# Static methods
    def Abs(input_curve, output_curve=Oasys.gRPC.defaultArg):
        """
        Convert a curve to absolute values

        Parameters
        ----------
        input_curve : Curve
            Input Curve
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Abs", input_curve, output_curve)

    def Acos(input_curve, output_curve=Oasys.gRPC.defaultArg):
        """
        Calculate Arc Cosine

        Parameters
        ----------
        input_curve : Curve
            Input Curve
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Acos", input_curve, output_curve)

    def Acu(input_curve, offset, time_period, output_curve=Oasys.gRPC.defaultArg):
        """
        Evaluates the integratal of a curve over a user defined period

        Parameters
        ----------
        input_curve : Curve
            Input Curve
        offset : float
            User defined offset
        time_period : float
            Time to integrate over
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Acu", input_curve, offset, time_period, output_curve)

    def Ad(input_curve, output_curve=Oasys.gRPC.defaultArg):
        """
        Convert acceleration spectrum to a displacment spectrum

        Parameters
        ----------
        input_curve : Curve
            Input Curve
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Ad", input_curve, output_curve)

    def Add(input_curve, second_curve_or_constant, output_curve=Oasys.gRPC.defaultArg):
        """
        Add Y axis values

        Parameters
        ----------
        input_curve : Curve
            Input Curve
        second_curve_or_constant : Curve or real
            Second Curve or constant
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Add", input_curve, second_curve_or_constant, output_curve)

    def Adx(first_curve, second_curve_or_constant, output_curve=Oasys.gRPC.defaultArg):
        """
        Add X axis values

        Parameters
        ----------
        first_curve : Curve
            First Curve
        second_curve_or_constant : Curve or real
            Second Curve or constant
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Adx", first_curve, second_curve_or_constant, output_curve)

    def Asi(x_acceleration, y_acceleration, z_acceleration, acceleration_conversion_factor, x_acceleration_limit, y_acceleration_limit, z_acceleration_limit, calculation_method, x_axis_interval=Oasys.gRPC.defaultArg, output_curve=Oasys.gRPC.defaultArg):
        """
        Acceleration Severity Index. This value is used to assess the performance of road side
        crash barriers. The calculation method can be set to 2010 (BS EN 1317-1:2010) or 1998 (BS EN 1317-1:1998)

        Parameters
        ----------
        x_acceleration : Curve
            X Acceleration Curve
        y_acceleration : Curve
            Y Acceleration Curve
        z_acceleration : Curve
            Z Acceleration Curve
        acceleration_conversion_factor : float
            Factor required to divide input acceleration curve by to convert to (G)
        x_acceleration_limit : float
            X direction acceleration limit
        y_acceleration_limit : float
            Y direction acceleration limit
        z_acceleration_limit : float
            Z direction acceleration limit
        calculation_method : string
            Either 2010 or 1998
        x_axis_interval : float
            If defined then T-HIS will automatically regularise the curve using this value first
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Asi", x_acceleration, y_acceleration, z_acceleration, acceleration_conversion_factor, x_acceleration_limit, y_acceleration_limit, z_acceleration_limit, calculation_method, x_axis_interval, output_curve)

    def Asin(input_curve, output_curve=Oasys.gRPC.defaultArg):
        """
        Calculate Arc Sine

        Parameters
        ----------
        input_curve : Curve
            Input Curve
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Asin", input_curve, output_curve)

    def Atan(input_curve, output_curve=Oasys.gRPC.defaultArg):
        """
        Calculate Arc Tangent

        Parameters
        ----------
        input_curve : Curve
            Input Curve
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Atan", input_curve, output_curve)

    def Atan2(first_input_curve, second_input_curve, output_curve=Oasys.gRPC.defaultArg):
        """
        Calculate Arc Tangent using atan2(y, x)

        Parameters
        ----------
        first_input_curve : Curve
            Input Curve
        second_input_curve : Curve
            Input Curve
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Atan2", first_input_curve, second_input_curve, output_curve)

    def Av(input_curve, output_curve=Oasys.gRPC.defaultArg):
        """
        Convert acceleration spectrum to a velocity spectrum

        Parameters
        ----------
        input_curve : Curve
            Input Curve
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Av", input_curve, output_curve)

    def Ave(curves, output_curve=Oasys.gRPC.defaultArg):
        """
        Average a group of curves

        Parameters
        ----------
        curves : Array of Curve objects
            Array of Curve objects
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Ave", curves, output_curve)

    def Bes(input_curve, frequency, order, x_axis_interval=Oasys.gRPC.defaultArg, output_curve=Oasys.gRPC.defaultArg):
        """
        Bessel Filter

        Parameters
        ----------
        input_curve : Curve
            Input Curve
        frequency : float
            Cut-off Frequency (Hz)
        order : integer
            Filter order
        x_axis_interval : float
            If defined then T-HIS will automatically regularise the curve using this value first
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Bes", input_curve, frequency, order, x_axis_interval, output_curve)

    def Blc(input_curve):
        """
        Carry out a baseline correction on an accleration time history

        Parameters
        ----------
        input_curve : Curve
            Moment / Time Curve

        Returns
        -------
        list
            List of Curve objects.
            1st curve : Corrected curve
            2nd curve : Integrated Velocity
            3rd curve : Integrated Displacement
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Blc", input_curve)

    def But(input_curve, frequency, order, x_axis_interval=Oasys.gRPC.defaultArg, output_curve=Oasys.gRPC.defaultArg):
        """
        Butterworth Filter

        Parameters
        ----------
        input_curve : Curve
            Input Curve
        frequency : float
            Cut-off Frequency (Hz)
        order : integer
            Filter order
        x_axis_interval : float
            If defined then T-HIS will automatically regularise the curve using this value first
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "But", input_curve, frequency, order, x_axis_interval, output_curve)

    def C1000(input_curve, x_axis_interval=Oasys.gRPC.defaultArg, output_curve=Oasys.gRPC.defaultArg):
        """
        SAE Class 1000 Filter

        Parameters
        ----------
        input_curve : Curve
            Input Curve
        x_axis_interval : float
            If defined then T-HIS will automatically regularise the curve using this value first
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "C1000", input_curve, x_axis_interval, output_curve)

    def C180(input_curve, x_axis_interval=Oasys.gRPC.defaultArg, output_curve=Oasys.gRPC.defaultArg):
        """
        SAE Class 180 Filter

        Parameters
        ----------
        input_curve : Curve
            Input Curve
        x_axis_interval : float
            If defined then T-HIS will automatically regularise the curve using this value first
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "C180", input_curve, x_axis_interval, output_curve)

    def C60(input_curve, x_axis_interval=Oasys.gRPC.defaultArg, output_curve=Oasys.gRPC.defaultArg):
        """
        SAE Class 60 Filter

        Parameters
        ----------
        input_curve : Curve
            Input Curve
        x_axis_interval : float
            If defined then T-HIS will automatically regularise the curve using this value first
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "C60", input_curve, x_axis_interval, output_curve)

    def C600(input_curve, x_axis_interval=Oasys.gRPC.defaultArg, output_curve=Oasys.gRPC.defaultArg):
        """
        SAE Class 600 Filter

        Parameters
        ----------
        input_curve : Curve
            Input Curve
        x_axis_interval : float
            If defined then T-HIS will automatically regularise the curve using this value first
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "C600", input_curve, x_axis_interval, output_curve)

    def Cat(first_curve, second_curve, output_curve=Oasys.gRPC.defaultArg):
        """
        Concatenate 2 curves together

        Parameters
        ----------
        first_curve : Curve
            First Curve
        second_curve : Curve or real
            Second Curve
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Cat", first_curve, second_curve, output_curve)

    def Clip(input_curve, x_min, x_max, y_min, y_max, output_curve=Oasys.gRPC.defaultArg):
        """
        Clip a curve

        Parameters
        ----------
        input_curve : Curve
            Input Curve
        x_min : float
            X minimum value
        x_max : float
            X maximum value
        y_min : float
            Y minimum value
        y_max : float
            Y maximum value
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Clip", input_curve, x_min, x_max, y_min, y_max, output_curve)

    def Com(first_curve, second_curve, output_curve=Oasys.gRPC.defaultArg):
        """
        Combine Y axis values from 2 curves together

        Parameters
        ----------
        first_curve : Curve
            First Curve
        second_curve : Curve or real
            Second Curve
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Com", first_curve, second_curve, output_curve)

    def Cor(first_curve, second_curve, correlation_type):
        """
        Curve Correlation function. 
        This Correlation function provides a measure of the degree to which two curves match.
        When comparing curves by eye, the quality of correlation may be judged on the basis
        of how well matched are the patterns of peaks, the overall shapes of the curves, etc,
        and can allow for differences of timing as well as magnitude. Thus a simple function
        based on the difference of Y-values (such as T/HIS ERR function) does not measure
        correlation in the same way as the human eye. The T/HIS correlation function attempts
        to include and quantify the more subtle ways in which the correlation of two curves
        may be judged.
        The correlation can be calculated using either a strict or loose set of input parameters.
        The degree of correlation is rated between 0 and 100

        Parameters
        ----------
        first_curve : Curve
            First Curve
        second_curve : Curve
            Second Curve
        correlation_type : string
            Correlation type, strict or loose

        Returns
        -------
        float
            float
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Cor", first_curve, second_curve, correlation_type)

    def Cor3(first_curve, second_curve, x_axis_factor=Oasys.gRPC.defaultArg, y_axis_factor=Oasys.gRPC.defaultArg):
        """
        Curve Correlation function.
        This function first normalises the curves using two factors either specified by the user
        or defaults calculated by the program (the maximum absolute X and Y values of both
        graphs). For each point on the first normalised curve, the shortest distance to the
        second normalised curve is calculated. The root mean square value of all these
        distances is subtracted from 1 and then multiplied by 100 to get an index between 0
        and 100. The process is repeated along the second curve and the two indices are
        averaged to get a final index. The higher the index the closer the correlation between
        the two curves.
        Note that the choice of normalising factors is important. Incorrect factors may lead to a
        correlation index outside the range of 0 to 100

        Parameters
        ----------
        first_curve : Curve
            First Curve
        second_curve : Curve
            Second Curve
        x_axis_factor : float
            Normalising factor used for X axis values
        y_axis_factor : float
            Normalising factor used for Y axis values

        Returns
        -------
        float
            float
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Cor3", first_curve, second_curve, x_axis_factor, y_axis_factor)

    def Cos(input_curve, output_curve=Oasys.gRPC.defaultArg):
        """
        Calculate Cosine

        Parameters
        ----------
        input_curve : Curve
            Input Curve
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Cos", input_curve, output_curve)

    def Da(input_curve, output_curve=Oasys.gRPC.defaultArg):
        """
        Convert displacment spectrum to an acceleration spectrum

        Parameters
        ----------
        input_curve : Curve
            Input Curve
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Da", input_curve, output_curve)

    def Dif(input_curve, output_curve=Oasys.gRPC.defaultArg):
        """
        Differentiate a curve

        Parameters
        ----------
        input_curve : Curve
            Input Curve
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Dif", input_curve, output_curve)

    def Div(first_curve, second_curve_or_constant, output_curve=Oasys.gRPC.defaultArg):
        """
        Divide Y axis values

        Parameters
        ----------
        first_curve : Curve
            First Curve
        second_curve_or_constant : Curve or real
            Second Curve or constant
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Div", first_curve, second_curve_or_constant, output_curve)

    def Dix(first_curve, second_curve_or_constant, output_curve=Oasys.gRPC.defaultArg):
        """
        Divide X axis values

        Parameters
        ----------
        first_curve : Curve
            First Curve
        second_curve_or_constant : Curve or real
            Second Curve or constant
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Dix", first_curve, second_curve_or_constant, output_curve)

    def Ds(input_curve, broadening_factor, redefine_frequencies, output_curve=Oasys.gRPC.defaultArg):
        """
        Generate a design spectrum from a reponse spectrum

        Parameters
        ----------
        input_curve : Curve
            Input Curve
        broadening_factor : float
            Spectrum broadening factor
        redefine_frequencies : string
            T-HIS selects a new set of frequencies for the output (yes or no)
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Ds", input_curve, broadening_factor, redefine_frequencies, output_curve)

    def Dv(input_curve, output_curve=Oasys.gRPC.defaultArg):
        """
        Convert displacment spectrum to a velocity spectrum

        Parameters
        ----------
        input_curve : Curve
            Input Curve
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Dv", input_curve, output_curve)

    def Env(curves, output_curve=Oasys.gRPC.defaultArg):
        """
        Generate an Envelope that bounds the min and max values of a group of curves

        Parameters
        ----------
        curves : Array of Curve objects
            Array of Curve objects
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Env", curves, output_curve)

    def Err(first_curve, second_curve, output_curve=Oasys.gRPC.defaultArg):
        """
        Calculate the degree of correlation between 2 curves

        Parameters
        ----------
        first_curve : Curve
            First Curve
        second_curve : Curve or real
            Second Curve
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Err", first_curve, second_curve, output_curve)

    def Exc(input_curve, output_option, output_curve=Oasys.gRPC.defaultArg):
        """
        Calculate and displays an EXCeedence plot. This is a plot of force (Y axis) versus 
        cumulative time (X axis) for which the force level has been exceeded. By default the Automatic option 
        will create an exceedence plot using either the +ve OR the -ve values depending on which the input 
        curve contains most of. 
        The Positive option will calculate the exceedence plot using only the points with +ve y values.
        The Negative option will calculate the exceedence plot using only the points with -ve y values

        Parameters
        ----------
        input_curve : Curve
            Input Curve
        output_option : string
            Select between automatic, positive or negative
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Exc", input_curve, output_option, output_curve)

    def Exp(input_curve, output_curve=Oasys.gRPC.defaultArg):
        """
        Calculate E to the power of Y axis values

        Parameters
        ----------
        input_curve : Curve
            Input Curve
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Exp", input_curve, output_curve)

    def Fft(input_curve, output_option, x_axis_interval=Oasys.gRPC.defaultArg, scaling_option=Oasys.gRPC.defaultArg):
        """
        Fast Fourier Transform

        Parameters
        ----------
        input_curve : Curve
            Input Curve
        output_option : string
            Generate magnitude, magnitude+phase or real+imaginary, (one of magnitude,phase,real)
        x_axis_interval : float
            If defined then T-HIS will automatically regularise the curve using this value first
        scaling_option : string
            Scaling option, (either one or two)

        Returns
        -------
        Curve
            Curve object/array or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Fft", input_curve, output_option, x_axis_interval, scaling_option)

    def Fir(input_curve, x_axis_interval=Oasys.gRPC.defaultArg, output_curve=Oasys.gRPC.defaultArg):
        """
        FIR Filter

        Parameters
        ----------
        input_curve : Curve
            Input Curve
        x_axis_interval : float
            If defined then T-HIS will automatically regularise the curve using this value first
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Fir", input_curve, x_axis_interval, output_curve)

    def Hic(input_curve, window, acceleration_factor):
        """
        HIC Calculation. After calculating the HIC value for a curve the value can also be obtained
        from the curve using the Curve.hic property. In addition to the HIC 
        value the start and end time for the time window can also be obtained using the Curve.hic_tmin
        and Curve.hic_tmax properties

        Parameters
        ----------
        input_curve : Curve
            Input Curve
        window : float
            Maximum time window
        acceleration_factor : float
            Factor required to divide input acceleration curve by to convert to (G)

        Returns
        -------
        float
            float
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Hic", input_curve, window, acceleration_factor)

    def Hicd(input_curve, window, acceleration_factor):
        """
        Modified HIC(d) Calculation for free motion headform. After calculating the HIC value for a curve 
        the value can also be obtained from the curve using the Curve.hicd property. 
        In addition to the HIC(d) value the start and end time for the time window can also be obtained using the 
        Curve.hicd_tmin and 
        Curve.hicd_tmax properties

        Parameters
        ----------
        input_curve : Curve
            Input Curve
        window : float
            Maximum time window
        acceleration_factor : float
            Factor required to divide input acceleration curve by to convert to (G)

        Returns
        -------
        float
            float
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Hicd", input_curve, window, acceleration_factor)

    def Ifft(first_curve, second_curve, input_type):
        """
        Inverse Fast Fourier Transform

        Parameters
        ----------
        first_curve : Curve
            First Curve
        second_curve : Curve
            Second Curve
        input_type : string
            Specifies if inputs are magnitude+phase or real+imaginary, (magnitude or real)

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Ifft", first_curve, second_curve, input_type)

    def Int(input_curve, output_curve=Oasys.gRPC.defaultArg):
        """
        Integrate a curve

        Parameters
        ----------
        input_curve : Curve
            Input Curve
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Int", input_curve, output_curve)

    def Log(input_curve, output_curve=Oasys.gRPC.defaultArg):
        """
        Calculate Natural Log of Y axis values

        Parameters
        ----------
        input_curve : Curve
            Input Curve
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Log", input_curve, output_curve)

    def Log10(input_curve, output_curve=Oasys.gRPC.defaultArg):
        """
        Calculate Log (base 10) of Y axis values

        Parameters
        ----------
        input_curve : Curve
            Input Curve
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Log10", input_curve, output_curve)

    def Log10x(input_curve, output_curve=Oasys.gRPC.defaultArg):
        """
        Calculate Log (base 10) of X axis values

        Parameters
        ----------
        input_curve : Curve
            Input Curve
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Log10x", input_curve, output_curve)

    def Logx(input_curve, output_curve=Oasys.gRPC.defaultArg):
        """
        Calculate Natural Log of X axis values

        Parameters
        ----------
        input_curve : Curve
            Input Curve
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Logx", input_curve, output_curve)

    def Lsq(input_curve, output_curve=Oasys.gRPC.defaultArg):
        """
        Calculate Least Squares Fit for a curve

        Parameters
        ----------
        input_curve : Curve
            Input Curve
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Lsq", input_curve, output_curve)

    def Map(first_curve, second_curve, output_curve=Oasys.gRPC.defaultArg):
        """
        Map Y axis values from one curve onto another curve

        Parameters
        ----------
        first_curve : Curve
            First Curve
        second_curve : Curve or real
            Second Curve
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Map", first_curve, second_curve, output_curve)

    def Max(curves, output_curve=Oasys.gRPC.defaultArg):
        """
        Maximum of a group of curves

        Parameters
        ----------
        curves : Array of Curve objects
            Array of Curve objects
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Max", curves, output_curve)

    def Min(curves, output_curve=Oasys.gRPC.defaultArg):
        """
        Minimum of a group of curves

        Parameters
        ----------
        curves : Array of Curve objects
            Array of Curve objects
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Min", curves, output_curve)

    def Mon(input_curve, output_curve=Oasys.gRPC.defaultArg):
        """
        Sort a curve into monotonically increasing X axis values

        Parameters
        ----------
        input_curve : Curve
            Input Curve
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Mon", input_curve, output_curve)

    def Mul(first_curve, second_curve_or_constant, output_curve=Oasys.gRPC.defaultArg):
        """
        Multiply Y axis values

        Parameters
        ----------
        first_curve : Curve
            First Curve
        second_curve_or_constant : Curve or real
            Second Curve or constant
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Mul", first_curve, second_curve_or_constant, output_curve)

    def Mux(first_curve, second_curve_or_constant, output_curve=Oasys.gRPC.defaultArg):
        """
        Multiply X axis values

        Parameters
        ----------
        first_curve : Curve
            First Curve
        second_curve_or_constant : Curve or real
            Second Curve or constant
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Mux", first_curve, second_curve_or_constant, output_curve)

    def Ncp(first_curve, second_curve):
        """
        Calculate a platic rotation curve for a beam from a moment/time and rotation/time

        Parameters
        ----------
        first_curve : Curve
            Moment / Time Curve
        second_curve : Curve
            Rotation /Time Curve

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Ncp", first_curve, second_curve)

    def Nij(shear_force, axial_force, moment, fzc_t, fzc_c, myc_f, myc_e, e):
        """
        Biomechanical neck injury predictor. Used as a measure of injury due to the 
        load transferred through the occipital condyles.
        This function returns an array containing 4 curve objects.
        Curve 1 - "Nte" is the tension-extension condition
        Curve 2 - "Ntf" is the tension-flexion condition
        Curve 3 - "Nce" is the compression-extension condition
        Curve 4 - "Ncf" is the compression-flexion condition

        Parameters
        ----------
        shear_force : Curve
            Shear Force Curve
        axial_force : Curve
            Axial Force Curve
        moment : Curve
            Moment Curve
        fzc_t : float
            Critical Axial Force (Tension)
        fzc_c : float
            Critical Axial Force (Compression)
        myc_f : float
            Critical bending moment (Flexion)
        myc_e : float
            Critical bending moment (Extension)
        e : float
            Distance

        Returns
        -------
        list
            List of Curve objects.
            1st curve : Nte curve, 
            2nd curve : Ntf curve, 
            3rd curve : Nce curve, 
            4th curve : Ncf curve
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Nij", shear_force, axial_force, moment, fzc_t, fzc_c, myc_f, myc_e, e)

    def Nor(input_curve, output_curve=Oasys.gRPC.defaultArg):
        """
        Normalise Y axis values between [-1,1]

        Parameters
        ----------
        input_curve : Curve
            Input Curve
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Nor", input_curve, output_curve)

    def Nor2(input_curve, y_min_value, y_max_value, lock_to_axis_y_min, lock_to_axis_y_max, output_curve=Oasys.gRPC.defaultArg):
        """
        Normalise Y axis values with manual settings. The operation takes 
        the absolute value of the user-specified Y Min and Y Max. It then finds the 
        maximum of these two numbers and divides all Y data by this number. There 
        are two locks which probe or "lock on to" the Y Max and Y Min axis values which offers 
        quick axis-normalizing

        Parameters
        ----------
        input_curve : Curve
            First Curve
        y_min_value : float
            The Minimum Y value
        y_max_value : float
            The Maximum Y value
        lock_to_axis_y_min : integer
            Set the Lock button for the Y Minimum textbox
        lock_to_axis_y_max : integer
            Set the Lock button for the Y Maximum textbox
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Nor2", input_curve, y_min_value, y_max_value, lock_to_axis_y_min, lock_to_axis_y_max, output_curve)

    def Nox(input_curve, output_curve=Oasys.gRPC.defaultArg):
        """
        Normalise X axis values between [-1,1]

        Parameters
        ----------
        input_curve : Curve
            Input Curve
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Nox", input_curve, output_curve)

    def Nox2(input_curve, x_min_value, x_max_value, lock_to_axis_x_min, lock_to_axis_x_max, output_curve=Oasys.gRPC.defaultArg):
        """
        Normalise X axis values with manual settings. The operation takes 
        the absolute value of the user-specified X Min and X Max. It then finds the 
        maximum of these two numbers and divides all X data by this number. There 
        are two locks which probe or "lock on to" the X Max and X Min axis values which offers 
        quick axis-normalizing

        Parameters
        ----------
        input_curve : Curve
            First Curve
        x_min_value : float
            The Minimum X value
        x_max_value : float
            The Maximum X value
        lock_to_axis_x_min : integer
            Set the Lock button for the X Minimum textbox
        lock_to_axis_x_max : integer
            Set the Lock button for the X Maximum textbox
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Nox2", input_curve, x_min_value, x_max_value, lock_to_axis_x_min, lock_to_axis_x_max, output_curve)

    def Octave(input_curve, band_type_to_convert_to, output_type, input_type, output_curve=Oasys.gRPC.defaultArg):
        """
        Coverts a narrow band curve to either Octave or 1/Third Octave bands

        Parameters
        ----------
        input_curve : Curve
            Input Curve
        band_type_to_convert_to : String
            Band type to convert to. Either "Octave" or "Third" Octave
        output_type : String
            Generate curve containing either "RMS" or "mean" values
        input_type : String
            Input curve contains either "Linear" or "dB" values
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Octave", input_curve, band_type_to_convert_to, output_type, input_type, output_curve)

    def Order(input_curve, output_curve=Oasys.gRPC.defaultArg):
        """
        Reverse the order of points in a curve

        Parameters
        ----------
        input_curve : Curve
            Input Curve
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Order", input_curve, output_curve)

    def Pbut(input_curve, frequency, order, x_axis_interval=Oasys.gRPC.defaultArg, output_curve=Oasys.gRPC.defaultArg):
        """
        Pure Butterworth Filter

        Parameters
        ----------
        input_curve : Curve
            Input Curve
        frequency : float
            Cut-off Frequency (Hz)
        order : integer
            Filter order
        x_axis_interval : float
            If defined then T-HIS will automatically regularise the curve using this value first
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Pbut", input_curve, frequency, order, x_axis_interval, output_curve)

    def Power(input_curve, power, output_curve=Oasys.gRPC.defaultArg):
        """
        Raise to the power

        Parameters
        ----------
        input_curve : Curve
            Input Curve
        power : float
            Power to raise Y axis values by
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Power", input_curve, power, output_curve)

    def Rave(input_curve, output_curve=Oasys.gRPC.defaultArg):
        """
        Calculate rolling average of a curve

        Parameters
        ----------
        input_curve : Curve
            Input Curve
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Rave", input_curve, output_curve)

    def Rec(input_curve, output_curve=Oasys.gRPC.defaultArg):
        """
        Calculate reciprocal

        Parameters
        ----------
        input_curve : Curve
            Input Curve
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Rec", input_curve, output_curve)

    def Reg(input_curve, x_axis_interval, output_curve=Oasys.gRPC.defaultArg):
        """
        Regularise X axis intervals for a curve

        Parameters
        ----------
        input_curve : Curve
            Input Curve
        x_axis_interval : float
            New X axis interval
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Reg", input_curve, x_axis_interval, output_curve)

    def Res(curves, output_curve=Oasys.gRPC.defaultArg):
        """
        Resultant of a group of curves

        Parameters
        ----------
        curves : Array of Curve objects
            Array of Curve objects
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Res", curves, output_curve)

    def Rev(input_curve, output_curve=Oasys.gRPC.defaultArg):
        """
        Reverse X and Y axis values

        Parameters
        ----------
        input_curve : Curve
            Input Curve
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Rev", input_curve, output_curve)

    def Rs(input_curve, damping_factor, sampling_points, x_axis_interval=Oasys.gRPC.defaultArg, output_curve=Oasys.gRPC.defaultArg):
        """
        Generate a reponse spectrum from input accelerations

        Parameters
        ----------
        input_curve : Curve
            Input Curve
        damping_factor : float
            Dammping factor
        sampling_points : int
            Number of points to sample over (30 or 70)
        x_axis_interval : float
            If defined then T-HIS will automatically regularise the curve using this value first
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        list
            List of Curve objects
            1st curve : Relative displacement, 
            2nd curve : Relative velocity, 
            3th curve : Pseudo relative velocity, 
            4th curve : Absolute acceleration, 
            5th curve : Pseudo absolute acceleration
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Rs", input_curve, damping_factor, sampling_points, x_axis_interval, output_curve)

    def Sin(input_curve, output_curve=Oasys.gRPC.defaultArg):
        """
        Calculate Sine

        Parameters
        ----------
        input_curve : Curve
            Input Curve
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Sin", input_curve, output_curve)

    def Smooth(input_curve, smoothing_factor, output_curve=Oasys.gRPC.defaultArg):
        """
        Apply a smoothing factor to a curve

        Parameters
        ----------
        input_curve : Curve
            Input Curve
        smoothing_factor : integer
            Number of points to average over
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Smooth", input_curve, smoothing_factor, output_curve)

    def Sqr(input_curve, output_curve=Oasys.gRPC.defaultArg):
        """
        Square root of a curve

        Parameters
        ----------
        input_curve : Curve
            Input Curve
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Sqr", input_curve, output_curve)

    def Stress(input_curve, convert_to, output_curve=Oasys.gRPC.defaultArg):
        """
        Convert between true and engineering stress

        Parameters
        ----------
        input_curve : Curve
            Input Curve
        convert_to : string
            Type to convert to (True or Engineering)
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Stress", input_curve, convert_to, output_curve)

    def Sub(first_curve, second_curve_or_constant, output_curve=Oasys.gRPC.defaultArg):
        """
        Subtract Y axis values

        Parameters
        ----------
        first_curve : Curve
            First Curve
        second_curve_or_constant : Curve or real
            Second Curve or constant
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Sub", first_curve, second_curve_or_constant, output_curve)

    def Sum(curves, output_curve=Oasys.gRPC.defaultArg):
        """
        Sum of a group of curves

        Parameters
        ----------
        curves : Array of Curve objects
            Array of Curve objects
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Sum", curves, output_curve)

    def Sux(first_curve, second_curve_or_constant, output_curve=Oasys.gRPC.defaultArg):
        """
        Subtract X axis values

        Parameters
        ----------
        first_curve : Curve
            First Curve
        second_curve_or_constant : Curve or real
            Second Curve or constant
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Sux", first_curve, second_curve_or_constant, output_curve)

    def Tan(input_curve, output_curve=Oasys.gRPC.defaultArg):
        """
        Calculate Tangent

        Parameters
        ----------
        input_curve : Curve
            Input Curve
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Tan", input_curve, output_curve)

    def Thiv(x_acceleration, y_acceleration, yaw_rate, dx, dy, x0):
        """
        Theoretical Head Impact Velocity and the Post Impact Head Deceleration.
        These values are used to assess the performance of road side crash barriers.
        This function returns an array containing 2 curve objects. The 1st curve is the THIV
        curve and the 2nd is the PHD curve. The peak values of these curves are the corresponding
        THIV and PHD values and can be obtained using the Curve.ymax
        property

        Parameters
        ----------
        x_acceleration : Curve
            X Acceleration Curve
        y_acceleration : Curve
            Y Acceleration Curve
        yaw_rate : Curve
            Yaw Rate Curve
        dx : float
            Horizontal distance between occupants head and vehicle
        dy : float
            Lateral distance between occupants head and vehicle
        x0 : float
            Horizontal distance between occupants head and vehicle CofG

        Returns
        -------
        list
            List of Curve objects.
            1st curve : THIV curve, 
            2nd curve : PHD curve
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Thiv", x_acceleration, y_acceleration, yaw_rate, dx, dy, x0)

    def Tms(input_curve, period):
        """
        3ms Clip Calculation. After calculating the 3ms clip value for a curve the value can also be obtained
        from the curve using the Curve.tms property. In addition to the 3ms clip value
        the start and end time for the time window can also be obtained using the Curve.tms_tmin
        and Curve.tms_tmax properties

        Parameters
        ----------
        input_curve : Curve
            Input Curve
        period : float
            Clip period

        Returns
        -------
        float
            float
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Tms", input_curve, period)

    def Translate(input_curve, x_value, y_value, output_curve=Oasys.gRPC.defaultArg):
        """
        Translate a curve

        Parameters
        ----------
        input_curve : Curve
            Input Curve
        x_value : float
            X translation value
        y_value : float
            Y translation value
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Translate", input_curve, x_value, y_value, output_curve)

    def Tti(upper_rib_acceleration, lower_rib_acceleration, t12_acceleration):
        """
        Thorax Trauma Index

        Parameters
        ----------
        upper_rib_acceleration : Curve
            Upper Rib Acceleration Curve
        lower_rib_acceleration : Curve
            Lower Rib Acceleration Curve
        t12_acceleration : Curve
            T12 Acceleration Curve

        Returns
        -------
        float
            float
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Tti", upper_rib_acceleration, lower_rib_acceleration, t12_acceleration)

    def Va(input_curve, output_curve=Oasys.gRPC.defaultArg):
        """
        Convert velocity spectrum to an acceleration spectrum

        Parameters
        ----------
        input_curve : Curve
            Input Curve
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Va", input_curve, output_curve)

    def Vc(input_curve, a, b, calculation_method, output_curve=Oasys.gRPC.defaultArg):
        """
        Viscous Criteria calculate. The VC calculation can be done using 2 different calculation 
        methods ECER95 and IIHS

        Parameters
        ----------
        input_curve : Curve
            Input Curve
        a : float
            Constant A
        b : float
            Constant B
        calculation_method : string
            Either ECER95 or IIHS
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Vc", input_curve, a, b, calculation_method, output_curve)

    def Vd(input_curve, output_curve=Oasys.gRPC.defaultArg):
        """
        Convert velocity spectrum to a displacment spectrum

        Parameters
        ----------
        input_curve : Curve
            Input Curve
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Vd", input_curve, output_curve)

    def Vec(first_curve, second_curve, third_curve, output_curve=Oasys.gRPC.defaultArg):
        """
        Vector magnitude of 3 curves

        Parameters
        ----------
        first_curve : Curve
            First Curve
        second_curve : Curve or real
            Second Curve
        third_curve : Curve or real
            Second Curve
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Vec", first_curve, second_curve, third_curve, output_curve)

    def Vec2d(first_curve, second_curve, output_curve=Oasys.gRPC.defaultArg):
        """
        Vector magnitude of 2 curves

        Parameters
        ----------
        first_curve : Curve
            First Curve
        second_curve : Curve or real
            Second Curve
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Vec2d", first_curve, second_curve, output_curve)

    def Wif(first_curve, second_curve):
        """
        Weigthed Integrated Factor (WIFAC) Correlation function

        Parameters
        ----------
        first_curve : Curve
            First Curve
        second_curve : Curve
            Second Curve

        Returns
        -------
        float
            float
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Wif", first_curve, second_curve)

    def Window(input_curve, window_type, percentage_lead_in=Oasys.gRPC.defaultArg, output_curve=Oasys.gRPC.defaultArg):
        """
        Apply a smoothing window to a curve

        Parameters
        ----------
        input_curve : Curve
            Input Curve
        window_type : string
            Window type to apply (Hanning, cosine or exponetial)
        percentage_lead_in : float
            percentage lead in for cosine window
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Window", input_curve, window_type, percentage_lead_in, output_curve)

    def Zero(input_curve, output_curve=Oasys.gRPC.defaultArg):
        """
        Translate curve to 0,0

        Parameters
        ----------
        input_curve : Curve
            Input Curve
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "Zero", input_curve, output_curve)

    def ZeroX(input_curve, output_curve=Oasys.gRPC.defaultArg):
        """
        Translate curve to X=0.0

        Parameters
        ----------
        input_curve : Curve
            Input Curve
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "ZeroX", input_curve, output_curve)

    def ZeroY(input_curve, output_curve=Oasys.gRPC.defaultArg):
        """
        Translate curve to Y=0.0

        Parameters
        ----------
        input_curve : Curve
            Input Curve
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "ZeroY", input_curve, output_curve)

    def dB(input_curve, reference_value, output_curve=Oasys.gRPC.defaultArg):
        """
        Converts a curve to dB (y = 20.0*log(y/yref))

        Parameters
        ----------
        input_curve : Curve
            Input Curve
        reference_value : float
            Reference value
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "dB", input_curve, reference_value, output_curve)

    def dBA(input_curve, weighting_type, output_curve=Oasys.gRPC.defaultArg):
        """
        Applies A-weighting to a curve (convert from dB to dBA)

        Parameters
        ----------
        input_curve : Curve
            Input Curve
        weighting_type : String
            Apply either Narrow band (narrow) or Octave band (octave) A weighting
        output_curve : Curve
            Curve to overwrite

        Returns
        -------
        Curve
            Curve object or None
        """
        return Oasys.THIS._connection.classMethod(__class__.__name__, "dBA", input_curve, weighting_type, output_curve)

