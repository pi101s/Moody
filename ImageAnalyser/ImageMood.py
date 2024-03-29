from threading import Thread
from threading import Lock
import ColorMood

from PIL import Image
import numpy

import time

number_of_threads = 1

class ImageMood:
    """This class is responsible for analyzing the images.
    """
    def __init__(self, image_path):
       
        """
            Arg:
                image_path: path of the image.

            Constructor of the class.
            Receives where is the path of the image that is going to be analyzed
            Saves the value taking into account the values in the file ColorMood.py
        """
        self._image_path = image_path
        self._image = None
        self._image_data = None
        self._colors = numpy.array([element["color"] for element in ColorMood.COLORS])
        self._valences = numpy.array([element["valence"] for element in ColorMood.COLORS])
        self._energies = numpy.array([element["energy"] for element in ColorMood.COLORS])
        self._valence = None
        self._energy = None
        self._lock = Lock()

    @property
    def valence(self):
        """property of the class

        Returns:
            Float: valence value
        """
        return self._valence

    @property
    def energy(self):
        """
        property of the class

        Returns:
            Float: Energy value
        """
        return self._energy

    def analyse_rows(self, start_row, end_row):
        """ This function calculates for a set of rows the value of valence and enery
            This value is calculated doing the cumsum of the value of valence and energy of
            each pixel.

        Args:
            start_row (integer): initial row for the analysis.
            end_row (integer): last row (this one is not analyzed).
        """        
        row_valence = 0
        row_energy = 0
    
        for i in range(start_row, end_row):
            row = numpy.array(self._image_data[i])
            sub = row[:, numpy.newaxis] - self._colors
            pow = numpy.power(sub, 2)
            sum = numpy.sum(pow, 2)
            indices = numpy.argmin(sum, 1)
            row_valence += numpy.sum(self._valences[indices])
            row_energy += numpy.sum(self._energies[indices])

        self._lock.acquire()
        self._valence += row_valence
        self._energy += row_energy
        self._lock.release()

    def analyse(self):
        """Analyse the whole image using the function written above with smaller sets of rows to be analyzed.
            Implement of threats to do it faster.

            The output/objective is calculate the final value of valence and energy of the picture.
        """        
        start_time = time.perf_counter()
        if not self._valence:
            self._image = Image.open(self._image_path)
            self._image_data = numpy.asarray(self._image)
            height = self._image_data.shape[0]
            width = self._image_data.shape[1]

            self._valence = 0
            self._energy = 0
            threads = []
            rows_per_thread = int((height / number_of_threads) + 1)
            sr = 0
            er = rows_per_thread

            for i in range(0, number_of_threads):
                sr = i * rows_per_thread
                er = min(((i + 1) * rows_per_thread), height)
                t = Thread(target=self.analyse_rows, args=(sr, er))
                t.start()
                threads.append(t)

            for thread in threads:
                thread.join()
                
            self._valence /= (height*width)
            self._energy /= (height*width)

        end_time = time.perf_counter()

        print('Analyse time: %.2fs' % (end_time - start_time))


if __name__ == "__main__":
    image_mood = ImageMood("../images/yellow.jpeg")
    image_mood.analyse()
    print(image_mood.valence)
    print(image_mood.energy)
