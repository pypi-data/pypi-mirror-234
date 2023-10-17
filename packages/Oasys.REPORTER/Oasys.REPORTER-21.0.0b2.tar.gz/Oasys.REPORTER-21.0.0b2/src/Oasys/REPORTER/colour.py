import Oasys.gRPC


# Metaclass for static properties and constants
class ColourType(type):

    def __getattr__(cls, name):

        raise AttributeError


class Colour(Oasys.gRPC.OasysItem, metaclass=ColourType):
    _rprops = {'blue', 'green', 'name', 'red'}


    def __del__(self):
        if not Oasys.REPORTER._connection:
            return

        Oasys.REPORTER._connection.destructor(self.__class__.__name__, self._handle)


    def __getattr__(self, name):
# If one of the read only properties we define then get it
        if name in Colour._rprops:
            return Oasys.REPORTER._connection.instanceGetter(self.__class__.__name__, self._handle, name)

        raise AttributeError


    def __setattr__(self, name, value):
# If one of the read only properties we define then error
        if name in Colour._rprops:
            raise AttributeError

# Set the property locally
        self.__dict__[name] = value


# Static methods
    def Black():
        """
        Creates a black colour

        Returns
        -------
        Colour
            Colour object
        """
        return Oasys.REPORTER._connection.classMethod(__class__.__name__, "Black")

    def Blue():
        """
        Creates a blue colour

        Returns
        -------
        Colour
            Colour object
        """
        return Oasys.REPORTER._connection.classMethod(__class__.__name__, "Blue")

    def Cyan():
        """
        Creates a cyan colour

        Returns
        -------
        Colour
            Colour object
        """
        return Oasys.REPORTER._connection.classMethod(__class__.__name__, "Cyan")

    def Green():
        """
        Creates a green colour

        Returns
        -------
        Colour
            Colour object
        """
        return Oasys.REPORTER._connection.classMethod(__class__.__name__, "Green")

    def Grey10():
        """
        Creates a 10% grey colour

        Returns
        -------
        Colour
            Colour object
        """
        return Oasys.REPORTER._connection.classMethod(__class__.__name__, "Grey10")

    def Grey20():
        """
        Creates a 20% grey colour

        Returns
        -------
        Colour
            Colour object
        """
        return Oasys.REPORTER._connection.classMethod(__class__.__name__, "Grey20")

    def Grey30():
        """
        Creates a 30% grey colour

        Returns
        -------
        Colour
            Colour object
        """
        return Oasys.REPORTER._connection.classMethod(__class__.__name__, "Grey30")

    def Grey40():
        """
        Creates a 40% grey colour

        Returns
        -------
        Colour
            Colour object
        """
        return Oasys.REPORTER._connection.classMethod(__class__.__name__, "Grey40")

    def Grey50():
        """
        Creates a 50% grey colour

        Returns
        -------
        Colour
            Colour object
        """
        return Oasys.REPORTER._connection.classMethod(__class__.__name__, "Grey50")

    def Grey60():
        """
        Creates a 60% grey colour

        Returns
        -------
        Colour
            Colour object
        """
        return Oasys.REPORTER._connection.classMethod(__class__.__name__, "Grey60")

    def Grey70():
        """
        Creates a 70% grey colour

        Returns
        -------
        Colour
            Colour object
        """
        return Oasys.REPORTER._connection.classMethod(__class__.__name__, "Grey70")

    def Grey80():
        """
        Creates a 80% grey colour

        Returns
        -------
        Colour
            Colour object
        """
        return Oasys.REPORTER._connection.classMethod(__class__.__name__, "Grey80")

    def Grey90():
        """
        Creates a 90% grey colour

        Returns
        -------
        Colour
            Colour object
        """
        return Oasys.REPORTER._connection.classMethod(__class__.__name__, "Grey90")

    def Magenta():
        """
        Creates a magenta colour

        Returns
        -------
        Colour
            Colour object
        """
        return Oasys.REPORTER._connection.classMethod(__class__.__name__, "Magenta")

    def NoColour():
        """
        No colour

        Returns
        -------
        Colour
            Colour object
        """
        return Oasys.REPORTER._connection.classMethod(__class__.__name__, "None")

    def RGB(red, green, blue):
        """
        Creates a colour from red, green and blue components

        Parameters
        ----------
        red : integer
            red component of colour (0-255)
        green : integer
            green component of colour (0-255)
        blue : integer
            blue component of colour (0-255)

        Returns
        -------
        Colour
            Colour object
        """
        return Oasys.REPORTER._connection.classMethod(__class__.__name__, "RGB", red, green, blue)

    def Red():
        """
        Creates a red colour

        Returns
        -------
        Colour
            Colour object
        """
        return Oasys.REPORTER._connection.classMethod(__class__.__name__, "Red")

    def White():
        """
        Creates a white colour

        Returns
        -------
        Colour
            Colour object
        """
        return Oasys.REPORTER._connection.classMethod(__class__.__name__, "White")

    def Yellow():
        """
        Creates a yellow colour

        Returns
        -------
        Colour
            Colour object
        """
        return Oasys.REPORTER._connection.classMethod(__class__.__name__, "Yellow")

